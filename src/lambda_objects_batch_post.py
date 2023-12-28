def handler(event: dict, context):
    # TODO Validate that event['transfers'] actually has 'basic' in the list.
    response = {
        'transfer': 'basic',
        'objects': [],
        'hash_algo': event.get('hash_algo', 'sha256')
    }

    for object in event['objects']:
        # generate an presigned URL
        url = f'https://ffylsca8bj.execute-api.us-east-1.amazonaws.com/dev/pwalentiny/repo.git/object/{object["oid"]}'
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
