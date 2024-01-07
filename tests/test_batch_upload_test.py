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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = 'project'
        self.repo = 'test-repo'

    def setUp(self):
        _init_repo('test-remote', bare=True)
        _clone_repo('./test-remote', 'test-repo')
        _setup_lfs('test-repo', 'project')

    def tearDown(self):
        shutil.rmtree('test-remote')
        shutil.rmtree('test-repo')

    def test_batch1_upload(self):
        filename = os.path.join('test-repo', 'file1.lfs')
        file_data_hash = _create_random_file(filename)
        _commit_file(filename)

        key = f'{self.project}/{self.repo}.git/{file_data_hash}'
        response = s3.get_object(
            Bucket=config['stack']['s3objectstore'],
            Key=key,
        )
        s3_file_hash = hashlib.new('sha256')
        s3_file_hash.update(response['Body'].read())

        self.assertEqual(file_data_hash, s3_file_hash.hexdigest())

    def test_batch2_download(self):
        filename = os.path.join('test-repo', 'file1.lfs')
        file_data_hash = _create_random_file(filename)
        _commit_file(filename)
        shutil.rmtree('test-repo')
        _clone_repo('./test-remote', 'test-repo')

        h = hashlib.new('sha256')
        with open(os.path.join('test-repo', 'file1.lfs'), 'rb') as fp:
            h.update(fp.read())

        self.assertEqual(h.hexdigest(), file_data_hash)

    def test_batch3_upload_duplicate(self):
        # project = 'project'
        # repo = 'test-repo'
        filename = os.path.join('test-repo', 'file1.lfs')
        _create_random_file(filename)
        _commit_file(filename)
        with open(filename, 'rb') as fp:
            file_data = fp.read()
        shutil.rmtree('test-repo')
        shutil.rmtree('test-remote')

        _init_repo('test-remote', bare=True)
        _clone_repo('./test-remote', 'test-repo')
        _setup_lfs('test-repo', 'project')
        with open(filename, 'wb') as fp:
            fp.write(file_data)
        _commit_file(filename)
        # Ugh, manually check the debug output from the git command?
        # Maybe check the last update time on the s3 key?
        #   - Really we should just do an API test using the requests library to see what we're after.
        #   - But we also need to know if this will work with the CLI anyway, right?!

    def test_batch4_download_missing(self):
        filename = os.path.join('test-repo', 'file1.lfs')
        file_data_hash = _create_random_file(filename)
        _commit_file(filename)

        version_id = s3.head_object(
            Bucket=config['stack']['s3objectstore'],
            Key=f"project/test-repo.git/{file_data_hash}",
        )['VersionId']

        response = s3.delete_object(
            Bucket=config['stack']['s3objectstore'],
            Key=f"project/test-repo.git/{file_data_hash}",
            VersionId=version_id
        )

        shutil.rmtree('test-repo')
        _clone_repo('./test-remote', 'test-repo')


def _clone_repo(remote, repo):
    return _run_process('git', 'clone', remote, repo, cwd='.')


def _commit_file(filename, timeout=10):
    basename = os.path.basename(filename)
    repo_dir = os.path.dirname(filename)
    _run_process('git', 'add', basename, cwd=repo_dir)
    _run_process(
        'git', 'commit', '-m', f'Adding {basename}.', cwd=repo_dir)
    _run_process('git', 'push', timeout=timeout, cwd=repo_dir)


def _create_random_file(filename, size=1024):
    file_data = bytes(
        (random.randint(0, 127) for n in range(size)))

    with open(filename, 'wb') as fp:
        fp.write(file_data)

    hash = hashlib.new('sha256')
    hash.update(file_data)
    file_data_hash = hash.hexdigest()
    return file_data_hash


def _init_repo(repo, bare=False):
    os.mkdir(repo)
    cmd = ['git', 'init']
    if bare:
        cmd.append('--bare')

    _run_process(*cmd, cwd=repo)


def _run_process(*cmd, **addl_args):
    kwargs = {
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
        'check': True
    }
    return subprocess.run(cmd, **(kwargs | addl_args))


def _setup_lfs(repo, project):
    _run_process('git', 'lfs', 'install', cwd=repo)
    _run_process('git', 'lfs', 'track', '*.lfs', cwd=repo)
    url = f"{config['stack']['apistageurl']}/{project}/{repo}.git/info/lfs"
    _run_process(
        'git', 'config', '-f', '.lfsconfig', '--add', 'lfs.url', url, cwd=repo)
    _run_process('git', 'add', '.', cwd=repo)
    _run_process('git', 'commit', '-m', 'Initial commit', cwd=repo)
    _run_process('git', 'push', '--set-upstream', 'origin', 'main', cwd=repo)


if __name__ == '__main__':
    unittest.main()
