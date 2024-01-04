import boto3
import botocore.exceptions

s3 = boto3.client('s3')


def handler(event, context):
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

    if operation == 'upload':
        client_method = 'put_object'

    elif operation == 'download':
        client_method = 'get_object'

    else:
        raise Exception(
            "event['operation'] needs to be either 'upload' or 'download'.")

    for _object in objects:
        key = f"{project}/{repo}/{_object['oid']}"
        Params = {
            'Bucket': bucket,
            'Key': key
        }

        if operation == 'upload':
            # Git LFS includes a Content-Type header when it uses the basic
            # trasfer protocol for uplaod operations.  S3 presigned urls
            # consider this header in the signature so we need to include
            # it in the parameters.
            Params['ContentType'] = 'application/octet-stream'

        url = s3.generate_presigned_url(
            client_method,
            Params=Params,
            ExpiresIn=3600
        )

        response_object = {
            'oid': _object['oid'],
            'size': _object['size'],
            'authenticated': True
        }

        if operation == 'download' or not _object_exists(bucket, key):
            response_object['actions'] = {
                operation: {
                    'href': url,
                    # 'header': {},
                    # 'expires_at': '2016-11-10T15:29:07Z',
                    'expires_in': 3600
                }
            }

        response['objects'].append(
            response_object
        )

    return response


def _object_exists(bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True

    except botocore.exceptions.ClientError as e:
        if 'Error' in e.response and 'Code' in e.response['Error']:
            if e.response['Error']['Code'] != '404':
                raise

            return False
