''' API Gateway Integration that implements the LFS Batch API

    Read more here:
        https://github.com/git-lfs/git-lfs/blob/main/docs/api/batch.md
'''
import base64
import boto3
import botocore.exceptions
import json
from typing import Optional

s3 = boto3.client('s3')


def handler(event, context):
    print(json.dumps(event))
    bucket = event['bucket']
    project = event['project']
    repo = event['repo']
    operation = event['request']['operation']
    objects = event['request']['objects']
    hash_algo = event['request'].get('hash_algo', 'sha256')

    response = {
        'transfer': 'basic',
        'objects': [],
        'hash_algo': hash_algo
    }

    for _object in objects:
        oid = _object['oid']
        size = _object['size']

        if hash_algo != 'sha256':
            response_object = create_response_object_error(
                oid, size, error_code=409, error_message=(
                    "The specified hash algorithm disagrees with the server's"
                    " acceptable options."))
            response['objects'].append(response_object)
            continue

        key = f"{project}/{repo}/{oid}"
        object_exists = check_object_existence(bucket, key)

        if operation == 'download' and not object_exists:
            response_object = create_response_object_error(
                oid, size, 404, "Object does not exist")
            response['objects'].append(response_object)
            continue

        if (operation == 'download' and object_exists) or \
                (operation == 'upload' and not object_exists):
            create_action = True

        elif operation == 'upload' and object_exists:
            create_action = False

        else:
            raise Exception(
                "event['operation'] needs to be either 'upload' or 'download'")

        response_object = create_response_object(
            bucket, key, operation, oid, size, create_action=create_action)

        response['objects'].append(response_object)

    return response


def create_presigned_url(bucket: str, key: str, operation: str, oid: str):
    ''' Create a presigned URL for uploading or downloading objects from S3

    :bucket:    The S3 bucket name
    :key:       The object's key
    :operation: The Git LFS Batch API operation.  Either "upload" or "download"
    :oid:       The Git LFS object id

    :return:    The signed URL
    '''
    params = {
        'Bucket': bucket,
        'Key': key
    }
    if operation == 'download':
        client_method = 'get_object'
    elif operation == 'upload':
        client_method = 'put_object'
        # Git LFS includes a Content-Type header when it uses the
        # basictrasfer protocol for upload operations.  S3
        # presigned urls consider this header in the signature so
        # we need to include it in the parameters.
        params['ContentType'] = 'application/octet-stream'
        # This adds the x-amz-checksum-sha256 header, which tells
        # S3 to compute the sha256 checksum when the object
        # is uploaded.
        params['ChecksumSHA256'] = hex_to_base64(oid)
    else:
        raise Exception('This shouldn\'t happen.')
    return s3.generate_presigned_url(
        client_method, Params=params, ExpiresIn=3600)


def create_response_object(bucket: str, key: str, operation: str, oid: str,
                           size: int, create_action=False):
    ''' Create an object for the response['objects'] list.

    :bucket:        The S3 bucket name
    :key:           The object's key
    :operation:     The Git LFS Batch API operation.  Either "upload" or
                        "download"
    :oid:           The Git LFS object id
    :size:          The size of the LFS object to be uploaded or downloaded
    :create_action: A boolean that tells the funciton if it needs to include
                        an action (a presigned url to upload or download an
                        object)

    :return:    A response object for the response['objects'] list
    '''
    response_object = {
        'oid': oid,
        'size': size
    }

    if create_action:
        response_object['authenticated'] = True
        url = create_presigned_url(bucket, key, operation, oid)
        action = {
            operation: {
                'href': url,
                'expires_in': 3600
            }
        }
        if operation == 'upload':
            action[operation]['header'] = {
                'x-amz-checksum-sha256': hex_to_base64(oid)}
        response_object['actions'] = action
    return response_object


def create_response_object_error(oid: str, size: int,
                                 error_code: Optional[int] = None,
                                 error_message: Optional[str] = None):
    ''' Create an object error for the response['objects'] list.

    :oid:           The Git LFS object id
    :size:          The size of the LFS object to be uploaded or downloaded
    :error_code:    The object error code (see the Git LFS API Spec link)
    :error_message: The error message to include in the response

    :return:    A response object error for the response['objects'] list
    '''
    return {
        'oid': oid,
        'size': size,
        'error': {
            "code": error_code,
            "message": error_message
        }
    }


def hex_to_base64(hex: str):
    ''' Convert a hexidecimal string into a base64 string.

        This is used to convert the objects sha256 hash from hex to base64.
        AWS S3 uses base64 signatures, but the Git LFS API Spec uses
        hexidecimal.

    :hex:   The hexidecimal string (probably a sha256 hash)

    :return:    The base64 equivalent of the hex string
    '''
    return base64.b64encode(
        bytes.fromhex(hex)).decode('utf-8')


def check_object_existence(bucket: str, key: str):
    ''' Check the existence of a specified AWS S3 bucket/key

    :bucket:        The S3 bucket name
    :key:           The S3 key

    :return:    True of the bucket/key exist, or False if they don't.
    '''
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True

    except botocore.exceptions.ClientError as e:
        if 'Error' in e.response and 'Code' in e.response['Error']:
            if e.response['Error']['Code'] != '404':
                raise

            return False
