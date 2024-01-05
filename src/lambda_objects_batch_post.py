''' API Gateway Integration that implements the LFS Batch API '''
import base64
import boto3
import botocore.exceptions

s3 = boto3.client('s3')


def handler(event, context):
    ''' API Gateway Integration that implements the LFS Batch API

    Read more here:
        https://github.com/git-lfs/git-lfs/blob/main/docs/api/batch.md

    :param event: The a dictionary representation of the JSON sent as part of
        the LFS Batch API request.
    :type event: dict
    :param context: The AWS Lambda context
        https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
    :type context: LambdaContext
    '''
    print(event)
    bucket = event['bucket']
    project = event['project']
    repo = event['repo']
    operation = event['request']['operation']
    objects = event['request']['objects']

    response = {
        'transfer': 'basic',
        'objects': [],
        'hash_algo': event['request'].get('hash_algo', 'sha256')
    }

    for _object in objects:
        key = f"{project}/{repo}/{_object['oid']}"
        # Git uses sha256 in hex format and S3 uses base64
        b64_object_oid = _hex_to_base64(_object['oid'])
        response_object = {
            'oid': _object['oid'],
            'size': _object['size'],
            'authenticated': True
        }

        # Check if the object already exists in the S3 object store
        object_exists = _object_exists(bucket, key)

        if operation == 'download' and object_exists:
            url = s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': bucket,
                    'Key': key
                },
                ExpiresIn=3600
            )
            response_object['actions'] = {
                operation: {
                    'href': url,
                    'expires_in': 3600
                }
            }
            response['objects'].append(response_object)
            continue

        elif operation == 'download' and not object_exists:
            # Return an error
            pass

        elif operation == 'upload' and object_exists:
            response['objects'].append(response_object)
            continue

        elif operation == 'upload' and not object_exists:
            url = s3.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': bucket,
                    'Key': key,

                    # Git LFS includes a Content-Type header when it uses the basic
                    # trasfer protocol for upload operations.  S3 presigned urls
                    # consider this header in the signature so we need to include
                    # it in the parameters.
                    'ContentType': 'application/octet-stream',

                    # This adds the x-amz-checksum-sha256 header, which tells
                    # S3 to compute the sha256 checksum when the object
                    # is uploaded.
                    'ChecksumSHA256': b64_object_oid
                },
                ExpiresIn=3600
            )
            response_object['actions'] = {
                operation: {
                    'href': url,
                    'header': {'x-amz-checksum-sha256': b64_object_oid},
                    'expires_in': 3600
                }
            }
            response['objects'].append(response_object)
            continue

        else:
            raise Exception(
                "event['operation'] needs to be either 'upload' or 'download'."
                )

        response['objects'].append(response_object)

    return response


def _hex_to_base64(hex):
    return base64.b64encode(
        bytes.fromhex(hex)).decode('utf-8')


def _object_exists(bucket, key):
    ''' Check if this bucket/key combo exists on the datastore

        :param bucket: The name of the S3 bucket
        :type bucket: str
        :param key: The key we're testing
        :type key: str
        :returns: True if the object exists, False if the object doesn't
            exist.
        :rtype: boolean
    '''
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True

    except botocore.exceptions.ClientError as e:
        if 'Error' in e.response and 'Code' in e.response['Error']:
            if e.response['Error']['Code'] != '404':
                raise

            return False
