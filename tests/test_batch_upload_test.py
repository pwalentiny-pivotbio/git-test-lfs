import boto3
import configparser
import hashlib
import os
import random
import shutil
import subprocess
import unittest


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

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree('test-repo')
        shutil.rmtree('test-remote')

    def test_batch1_upload(self):
        hash = hashlib.new('sha256')
        with open(os.path.join('test-repo', 'binaryFile'), 'wb') as fp:
            binaryData = bytes([random.randint(0, 127) for n in range(1024)])
            hash.update(binaryData)
            fp.write(binaryData)

        run_process('git', 'add', 'binaryFile')
        run_process(
            'git', 'commit', '-m', 'Adding binary file for a test upload')
        run_process('git', 'push', timeout=10)
        s3 = boto3.client('s3')
        print(f'pwalentiny/repo.git/{hash.hexdigest()}')
        response = s3.get_object(
            Bucket = config['stack']['s3objectstore'],
            Key = f'pwalentiny/repo.git/{hash.hexdigest()}',
        )
        h2 = hashlib.new('sha256')
        h2.update(response['Body'].read())

        self.assertEqual(hash.hexdigest(), h2.hexdigest())

    def test_batch2_download(self):
        run_process('git', 'clone', './test-remote', 'test-repo2', cwd='.')
        hash_results = []
        for repo in ['test-repo', 'test-repo2']:
            with open(os.path.join(repo, 'binaryFile'), 'rb') as fp:
                h = hashlib.new('sha256')
                h.update(fp.read())
                hash_results.append(h.hexdigest())
        
        self.assertEqual(hash_results[0], hash_results[1])


def run_process(*cmd, **addl_args):
    kwargs = {
        'cwd': 'test-repo',
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
        'check': True
    }
    return subprocess.run(cmd, **(kwargs | addl_args))


if __name__ == '__main__':
    unittest.main()
