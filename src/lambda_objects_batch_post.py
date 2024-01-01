import boto3

s3 = boto3.client('s3')

def handler(event: dict, context):
    print(event)
    # TODO Validate that event['transfers'] actually has 'basic' in the list.
    response = {
        'transfer': 'basic',
        'objects': [],
        'hash_algo': event.get('hash_algo', 'sha256')
    }

    for object in event['objects']:
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': 'git-lfs-api-s3objectstore-tpdyb5s7c34i',
                'Key': f"pwalentiny/repo.git/{object['oid']}",
                'ContentType': 'application/octet-stream'
            },
            ExpiresIn=3600,

        )
        url = presigned_url
        response['objects'].append(
            {
                'oid': object['oid'],
                'size': object['size'],
                'authenticated': True,
                'actions': {
                    event['operation']: {
                        'href': url,
                        # 'header': {},
                        # 'expires_at': ''
                    }
                }
            }
        )

    return response

    # return {
    #     "transfer": "basic",
    #     "objects": [
    #         {
    #         "oid": "1111111",
    #         "size": 123,
    #         "authenticated": True,
    #         "actions": {
    #             "download": {
    #             "href": "https://some-download.com",
    #             "header": {
    #                 "Key": "value"
    #             },
    #             "expires_at": "2016-11-10T15:29:07Z"
    #             }
    #         }
    #         }
    #     ],
    #     "hash_algo": "sha256"
    #     }
