# -*- coding: utf-8 -*-

import unittest
import os
from ucloud.ufile import uploadhitufile
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

wrong_bucket = 'david-wrong'

instead_key = 'instead'
nonexistfile = './nonexist.log'
existfile = './Wildlife.wmv'

class UploadHitUFileTestCase(unittest.TestCase):
    uploadhitufile_handler = uploadhitufile.UploadHitUFile(public_key, private_key)

    def test_uploadhitexistfile(self):
        self.uploadhitufile_handler.set_keys(public_key, private_key)
        logger.info('start uploadhit existfile')
        ret, resp = self.uploadhitufile_handler.uploadhit(public_bucket, instead_key, existfile)
        assert resp.status_code == 200

    def test_uploadhitunexistfile(self):
        self.uploadhitufile_handler.set_keys(public_key, private_key)
        logger.info('start uploadhit nonexistfile')
        ret, resp = self.uploadhitufile_handler.uploadhit(public_bucket, instead_key, nonexistfile)
        assert resp.status_code == 404

    def test_uploadhittowrongbucket(self):
        self.uploadhitufile_handler.set_keys(public_key, private_key)
        logger.info('start uploadhit to wrong bucket')
        ret, resp = self.uploadhitufile_handler.uploadhit(wrong_bucket, instead_key, existfile)
        assert resp.status_code == 400

    def test_uploadhitwithwrongkeys(self):
        self.uploadhitufile_handler.set_keys(wrong_public_key, wrong_private_key)
        logger.info('start uploadhit with wrong api keys')
        ret, resp = self.uploadhitufile_handler.uploadhit(public_bucket, instead_key, existfile)
        assert resp.status_code == 403

if __name__ == '__main__':
    unittest.main()
