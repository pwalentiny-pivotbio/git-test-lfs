import boto3
import configparser
import hashlib
import os
import random
import shutil
import subprocess
import unittest

s3 = boto3.client('s3')
config = configparser.ConfigParser()
config.read("../config.ini")


class TestBatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.mkdir('test-remote')
        run_process('git', 'init', '--bare', cwd='test-remote')

        os.mkdir('test-repo')
        run_process('git', 'init')
        run_process('git', 'remote', 'add', 'origin', '../test-remote')
        run_process('git', 'lfs', 'install')
        run_process('git', 'lfs', 'track', 'binaryFile')

        url = f"{config['stack']['apistageurl']}/project/repo.git/info/lfs"
        run_process(
            'git', 'config', '-f', '.lfsconfig', '--add', 'lfs.url', url)
        run_process('git', 'add', '.')
        run_process('git', 'commit', '-m', 'Initial commit')
        run_process('git', 'push', '--set-upstream', 'origin', 'main')
        shutil.rmtree('test-repo')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree('test-remote')

    def setUp(self):
        run_process('git', 'clone', './test-remote', 'test-repo', cwd='.')

    def tearDown(self):
        shutil.rmtree('test-repo')

    def test_batch1_upload(self):
        hash = hashlib.new('sha256')
        with open(os.path.join('test-repo', 'binaryFile'), 'wb') as fp:
            fp.write(_file_data)

        run_process('git', 'add', 'binaryFile')
        run_process(
            'git', 'commit', '-m', 'Adding binary file for a test upload')
        run_process('git', 'push', timeout=10)
        key = f'project/repo.git/{_file_data_hash}'
        response = s3.get_object(
            Bucket=config['stack']['s3objectstore'],
            Key=key,
        )
        s3_file_hash = hashlib.new('sha256')
        s3_file_hash.update(response['Body'].read())

        self.assertEqual(_file_data_hash, s3_file_hash.hexdigest())

    def test_batch2_download(self):
        h = hashlib.new('sha256')
        with open(os.path.join('test-repo', 'binaryFile'), 'rb') as fp:
            h.update(fp.read())

        self.assertEqual(h.hexdigest(), _file_data_hash)


def generate_file():
    file_data = bytes(
        [random.randint(0, 127) for n in range(1024)])
    hash = hashlib.new('sha256')
    hash.update(file_data)
    file_data_hash = hash.hexdigest()
    return file_data, file_data_hash


def run_process(*cmd, **addl_args):
    kwargs = {
        'cwd': 'test-repo',
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
        'check': True
    }
    return subprocess.run(cmd, **(kwargs | addl_args))


_file_data, _file_data_hash = generate_file()
if __name__ == '__main__':
    unittest.main()
