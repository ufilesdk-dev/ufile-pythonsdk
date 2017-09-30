# -*- coding: utf-8 -*-

import unittest
import os
from ucloud.ufile import multipartuploadufile
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
sharding_small_key = 'sharding_small'

big_local_file = './Wildlife.wmv'
sharding_big_key = 'sharding_big'

bio = BytesIO(u'你好'.encode('utf-8'))
sharding_stream_key = 'sharding_stream'

wrong_bucket = 'david-wrong'
wrong_key = 'wrong'

class MultipartUploadUFileTestCase(unittest.TestCase):
    multipartuploadufile_handler = multipartuploadufile.MultipartUploadUFile(public_key, private_key)

    def test_uploadfile(self):
        self.multipartuploadufile_handler.set_keys(public_key, private_key)

        # upload small file to public bucket
        logger.info('start sharding small file to public bucket')
        ret, resp = self.multipartuploadufile_handler.uploadfile(public_bucket, sharding_small_key, small_local_file)
        print(resp.error)
        assert resp.status_code == 200
        # upload big file to public bucket
        logger.info('start sharding upload big file to public bucket')
        ret, resp = self.multipartuploadufile_handler.uploadfile(public_bucket, sharding_big_key, big_local_file)
        print(resp.error)
        assert resp.status_code == 200
        # upload small file to private bucket
        logger.info('start sharding upload small file to private bucket')
        ret, resp = self.multipartuploadufile_handler.uploadfile(private_bucket, sharding_small_key, small_local_file)
        print(resp.error)
        assert resp.status_code == 200
        # upload big file to private bucket
        logger.info('start sharding upload big file to private bucket')
        ret, resp = self.multipartuploadufile_handler.uploadfile(private_bucket, sharding_big_key, big_local_file)
        print(resp.error)
        assert resp.status_code == 200

    def test_uploadstream(self):
        self.multipartuploadufile_handler.set_keys(public_key, private_key)

        # upload binary data stream to public bucket
        logger.info('start upload stream to public bucket')
        ret, resp = self.multipartuploadufile_handler.uploadstream(public_bucket, sharding_stream_key, bio)
        print(resp.error)
        assert resp.status_code == 200
        # upload binary data stream to private bucket
        logger.info('start upload stream to private bucket')
        bio.seek(0, os.SEEK_SET)
        ret, resp = self.multipartuploadufile_handler.uploadstream(private_bucket, sharding_stream_key, bio)
        print(resp.error)
        assert resp.status_code == 200

    def test_uploadtowrongbucket(self):
        self.multipartuploadufile_handler.set_keys(public_key, private_key)

        # upload file to wrong bucket
        logger.info('start upload file to wrong bucket')
        ret, resp = self.multipartuploadufile_handler.uploadfile(wrong_bucket, sharding_small_key, small_local_file)
        assert resp.status_code == 400
        print(resp.error)

    def test_uploadwithwrongkeys(self):
        self.multipartuploadufile_handler.set_keys(wrong_public_key, wrong_private_key)

        # upload file to public bucket with wrong api keys
        logger.info('start upload file to bucket with wrong api keys')
        ret, resp = self.multipartuploadufile_handler.uploadfile(public_bucket, sharding_small_key, small_local_file)
        assert resp.status_code == 403
        print(resp.error)

        # upload filet to private bucket with wrong api keys
        logger.info('start upload file to private bucket with wrong api keys')
        ret, resp = self.multipartuploadufile_handler.uploadfile(private_bucket, sharding_small_key, small_local_file)
        assert resp.status_code == 403
        print(resp.error)

if __name__ == '__main__':
    unittest.main()
