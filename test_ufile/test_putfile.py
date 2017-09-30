# -*- coding: utf-8 -*-

import unittest
import os
from ucloud.ufile import putufile
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
put_small_key = 'put_small'

big_local_file = './Wildlife.wmv'
put_big_key = 'put_big'

bio = BytesIO(u'你好'.encode('utf-8'))
put_stream_key = 'put_stream'

wrong_bucket = 'david-wrong'
wrong_key = 'wrong'

class PutUFileTestCase(unittest.TestCase):
    putufile_handler = putufile.PutUFile(public_key, private_key)

    def test_putufile(self):
        self.putufile_handler.set_keys(public_key, private_key)
        # put small file to public bucket
        logger.info('\nput small file to public bucket')
        ret, resp = self.putufile_handler.putfile(public_bucket, put_small_key, small_local_file)
        assert resp.status_code == 200
        # put big file to public bucket
        logger.info('\nput big file to public bucket')
        ret, resp = self.putufile_handler.putfile(public_bucket, put_big_key, big_local_file)
        assert resp.status_code == 200
        # put small file to private bucket
        logger.info('\nput small file to private bucket')
        ret, resp = self.putufile_handler.putfile(private_bucket, put_small_key, small_local_file)
        assert resp.status_code == 200
        # put big file to private bucket
        logger.info('\nput big file to private bucket')
        ret, resp = self.putufile_handler.putfile(private_bucket, put_big_key, big_local_file)
        assert resp.status_code == 200

    def test_putstream(self):
        self.putufile_handler.set_keys(public_key, private_key)
        logger.info('\nput stream to public bucket')
        ret, resp = self.putufile_handler.putstream(public_bucket, put_stream_key, bio)
        assert resp.status_code == 200
        bio.seek(0, os.SEEK_SET)
        logger.info('\nput stream to private bucket')
        ret, resp = self.putufile_handler.putstream(private_bucket, put_stream_key, bio)
        assert resp.status_code == 200

    def test_putfiletowrongbucket(self):
        self.putufile_handler.set_keys(public_key, private_key)
        # put file to wrong bucket
        logger.info('\nput file to wrong bucket')
        ret, resp = self.putufile_handler.putfile(wrong_bucket, put_small_key, small_local_file)
        assert resp.status_code == 400
        logger.info(resp.error)

    def test_putufilewithwrongkey(self):
        self.putufile_handler.set_keys(wrong_public_key, wrong_private_key)
        logger.info('\nput small file to public bucket with wrong api keys pair')
        # put small file to public bucket with wrong api keys pair
        ret, resp = self.putufile_handler.putfile(public_bucket, put_small_key, small_local_file)
        assert resp.status_code == 403
        logger.info(resp.error)

        # put small file to private bucket with wrong api keys pair
        logger.info('\nput small file to private bucket with wrong api keys pair')
        ret, resp = self.putufile_handler.putfile(private_bucket, put_small_key, small_local_file)
        logger.error('status_code:{0}'.format(resp.status_code))
        assert resp.status_code == 403
        logger.info(resp.error)

if __name__ == '__main__':
    unittest.main()
