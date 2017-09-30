# -*- coding: utf-8 -*-

import unittest
import os
from ucloud.ufile import postufile
from ucloud.compact import b
from ucloud.logger import logger, set_log_file
from ucloud.ufile.config import BLOCKSIZE, get_default
from ucloud.compact import BytesIO

set_log_file()
public_key = '' #添加自己的账户公钥
private_key = '' #添加自己的账户私钥
public_bucket = '' #公共空间名称
private_bucket = '' #私有空间名称

wrong_public_key = 'dfajlkfladjfa'
wrong_private_key = 'fajdlfjkkkkkk'

small_local_file = './small.jpg'
post_small_key = 'post_small'

big_local_file = './Wildlife.wmv'
post_big_key = 'post_big'

bio = BytesIO(u'你好'.encode('utf-8'))
post_stream_key = 'post_stream'

wrong_bucket = 'david-wrong'
wrong_key = 'wrong'

class PostUFileTestCase(unittest.TestCase):
    postfile_handler = postufile.PostUFile(public_key, private_key)

    def test_postufile(self):
        self.postfile_handler.set_keys(public_key, private_key)
        # post small file to public bucket
        logger.info('\nstart post small file to public bucket')
        ret, resp = self.postfile_handler.postfile(public_bucket, post_small_key, small_local_file)
        logger.error(resp.error)
        assert resp.status_code == 200
        # post big file to public bucket
        logger.info('\nstart post big file to public bucket')
        ret, resp = self.postfile_handler.postfile(public_bucket, post_big_key, big_local_file)
        logger.error(resp.error)
        assert resp.status_code == 200
        # post small file to private bucket
        logger.info('\nstart post small file to private bucket')
        ret, resp = self.postfile_handler.postfile(private_bucket, post_small_key, small_local_file)
        logger.error(resp.error)
        assert resp.status_code == 200
        # post big file to private bucket
        logger.info('\nstart post big file to private bucket')
        ret, resp = self.postfile_handler.postfile(private_bucket, post_big_key, big_local_file)
        logger.error(resp.error)
        assert resp.status_code == 200

    def test_postufiletowrongbucket(self):
        self.postfile_handler.set_keys(public_key, private_key)
        # post file to wrong bucket
        logger.info('\nstart post small file to wrong bucket')
        ret, resp = self.postfile_handler.postfile(wrong_bucket, post_small_key, small_local_file)
        logger.error(resp.error)
        assert resp.status_code == 400

    def test_postufilewithwrongkey(self):
        # set the wrong api keys
        self.postfile_handler.set_keys(wrong_public_key, wrong_private_key)
        # post small file with the wrong api keys
        logger.info('\nstart post small file to public bucket with wrong api keys pair')
        ret, resp = self.postfile_handler.postfile(public_bucket, post_small_key, small_local_file)
        logger.error(resp.error)
        assert resp.status_code == 403

if __name__ == '__main__':
    unittest.main()
