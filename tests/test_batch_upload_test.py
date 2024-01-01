import configparser
import os
import random
import shutil
import subprocess
import unittest


config = configparser.ConfigParser()
config.read("../config.ini")


def run_process(*cmd, **addl_args):
    kwargs = {
        'cwd': 'test-repo',
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
        'check': True
    }
    subprocess.run(cmd, **(kwargs | addl_args))


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
        url = f"{config['stack']['apistageurl']}/pwalentiny/repo.git/info/lfs"
        run_process(
            'git', 'config', '-f', '.lfsconfig', '--add', 'lfs.url', url)
        run_process('git', 'add', '.')
        run_process('git', 'commit', '-m', 'Initial commit')
        run_process('git', 'push', '--set-upstream', 'origin', 'main')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree('test-repo')
        shutil.rmtree('test-remote')

    def test_upload(self):
        with open(os.path.join('test-repo', 'binaryFile'), 'wb') as fp:
            binaryData = bytes([random.randint(0, 127) for n in range(1024)])
            fp.write(binaryData)

        run_process('git', 'add', 'binaryFile')
        run_process(
            'git', 'commit', '-m', 'Adding binary file for a test upload')
        run_process('git', 'push', timeout=10)

    def test_download(self):
        raise NotImplementedError
