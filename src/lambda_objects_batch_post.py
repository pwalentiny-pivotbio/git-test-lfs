import boto3

s3 = boto3.client('s3')


def handler(event, context):
    print(event)
    bucket = event['bucket']
    project = event['project']
    repo = event['repo']
    event = event['request']

    response = {
        'transfer': 'basic',
        'objects': [],
        'hash_algo': event.get('hash_algo', 'sha256')
    }

    if event['operation'] == 'upload':
        client_method = 'put_object'
    
    elif event['operation'] == 'download':
        client_method = 'get_object'
    
    else:
        raise Exception("event['operation'] needs to be either 'upload' or 'download'.")
    
    for object in event['objects']:
        Params = {
            'Bucket': bucket,
            'Key': f"{project}/{repo}/{object['oid']}"
        }

        # Git LFS includes a Content-Type header when it uses the basic
        # trasfer protocol for uplaod operations.  S3 presigned urls consider
        # this header in the signature so we need to include it in the
        # parameters.
        if event['operation'] == 'upload':
            Params['ContentType'] = 'application/octet-stream'

        url = s3.generate_presigned_url(
            client_method,
            Params=Params,
            ExpiresIn=3600
        )

        response['objects'].append(
            {
                'oid': object['oid'],
                'size': object['size'],
                'authenticated': True,
                'actions': {
                    event['operation']: {
                        'href': url,
                        # 'header': {},
                        # 'expires_at': '2016-11-10T15:29:07Z'
                    }
                }
            }
        )

    return response
