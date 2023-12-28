import argparse
import configparser
import boto3
# import hashlib
# import os
# import os.path
# import shutil
# import sys


# def build(args):
#     try:
#         os.mkdir('build')
#     except FileExistsError:
#         pass

#     # m = hashlib.sha256()
#     m = hashlib.sha1()
#     with open(args.function, 'rb') as fp:
#         m.update(fp.read())
#     file_hash = m.hexdigest()
#     shutil.copy(args.function, os.path.join('build', file_hash))
#     print(args.function)
#     print(args.parameter)
#     print(file_hash)


# def deploy(args):
#     print('deploy')


def generate(args):
    cloudformation = boto3.client('cloudformation')
    response = cloudformation.describe_stacks(StackName=args.stack_name)

    args.config['stack'] = {
        'stack-name': args.stack_name
    }

    for output in response['Stacks'][0]['Outputs']:
        args.config['stack'][output['OutputKey']] = output['OutputValue']

    with open('config.ini', 'w') as fp:
        args.config.write(fp)


def get(args):
    pass


def put(args):
    pass


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")
    parser = argparse.ArgumentParser(description="")
    subparsers = parser.add_subparsers(required=True)
    generate_parser = subparsers.add_parser('generate')
    generate_parser.set_defaults(func=generate, config=config)
    generate_parser.add_argument('--config-file', '-c', action='store', default='config.ini')
    generate_parser.add_argument('--stack-name', '-s', action='store', default='git-lfs-api')
    
    get_parser = subparsers.add_parser('get')
    get_parser.set_defaults(func=get)

    put_parse = subparsers.add_parser('put')
    put_parse.set_defaults(func=put)

    args = parser.parse_args()
    args.func(args)

    # parser = argparse.ArgumentParser(description="")
    # subparsers = parser.add_subparsers()
    # build_parser = subparsers.add_parser('build')
    # build_parser.set_defaults(func=build)
    # build_parser.add_argument('--function', '-f', action='store', required=True)
    # build_parser.add_argument('--parameter', '-p', action='store', required=True)

    # deploy_parser = subparsers.add_parser('deploy')
    # deploy_parser.set_defaults(func=deploy)

    # args = parser.parse_args()
    # args.func(args)

    # s3 = boto3.client('s3')
    # print(config['build']['artifact-bucket'])
    # print(config['build']['stack-name'])
    # s3.upload_file('', '', '')
    # print("Hello world!")