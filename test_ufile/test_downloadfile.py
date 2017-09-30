# -*- coding: utf-8 -*-

import unittest
from ucloud.ufile import downloadufile
from ucloud.logger import logger, set_log_file
from ucloud.ufile.config import BLOCKSIZE, get_default


public_key = '' #添加自己的账户公钥
private_key = '' #添加自己的账户私钥
public_bucket = '' #公共空间名称
private_bucket = '' #私有空间名称

wrong_public_key = 'dfajlkfladjfa'
wrong_private_key = 'fajdlfjkkkkkk'

put_small_key = 'put_small'
put_big_key = 'put_big'
put_range_key = 'put_stream'

public_small_download = 'public_small_download'
public_big_download = 'public_big_download'
public_range_download = 'public_range_download'
private_small_download = 'private_small_download'
private_big_download = 'private_big_download'
private_range_download = 'private_range_download'

wrong_bucket = 'david-wrong'
wrong_key = 'wrong'
set_log_file()


class DownloadUFileTestCase(unittest.TestCase):
    downloadufile_handler = downloadufile.DownloadUFile(public_key, private_key)

    def test_downloadpublic(self):
        self.downloadufile_handler.set_keys(public_key, private_key)
        # download the small file
        logger.info('\nstart download small file from public bucket')
        ret, resp = self.downloadufile_handler.download_file(public_bucket, put_small_key, public_small_download, isprivate=False)
        assert resp.status_code == 200

        # download the big file
        logger.info('\nstart download big file from public bucket')
        ret, resp = self.downloadufile_handler.download_file(public_bucket, put_big_key, public_big_download, isprivate=False)
        assert resp.status_code == 200

    def test_downloadprivate(self):
        self.downloadufile_handler.set_keys(public_key, private_key)
        # download the small file
        logger.info('start download small file from private bucket')
        ret, resp = self.downloadufile_handler.download_file(private_bucket, put_small_key, private_small_download)
        assert resp.status_code == 200
        # download the big file
        logger.info('start download big file from pirvate bucket')
        ret, resp = self.downloadufile_handler.download_file(private_bucket, put_big_key, private_big_download)
        assert resp.status_code == 200

    def test_downloadwithrange(self):
        self.downloadufile_handler.set_keys(public_key, private_key)
        logger.info('start download with range condition from public bucket')
        ret, resp = self.downloadufile_handler.download_file(public_bucket, put_range_key, public_range_download, isprivate=False, expires=get_default('expires'), content_range=(0, 5), header=None)
        assert resp.status_code == 206
        logger.info('start download with range condition from private bucket')
        ret, resp = self.downloadufile_handler.download_file(public_bucket, put_range_key, private_range_download, isprivate=True, expires=get_default('expires'), content_range=(0, 5), header=None)
        assert resp.status_code == 206

    def test_downloadwrongkey(self):
        # download the wrong key file
        self.downloadufile_handler.set_keys(public_key, private_key)
        logger.info('start download with nonexist key')
        ret, resp = self.downloadufile_handler.download_file(public_bucket, wrong_key, public_small_download, isprivate=False)
        assert resp.status_code == 404

    def test_downloadfromwrongbucket(self):
        # download from the wrong bucket
        self.downloadufile_handler.set_keys(public_key, private_key)
        logger.info('start download from wrong bucket')
        ret, resp = self.downloadufile_handler.download_file(wrong_bucket, put_small_key, public_small_download, isprivate=False)
        assert resp.status_code == 400

    def test_downloadwithwrongapikeys(self):
        self.downloadufile_handler.set_keys(wrong_public_key, wrong_private_key)
        # download from the private bucket
        logger.info('start download from private bucket with wrong api keys')
        ret, resp = self.downloadufile_handler.download_file(private_bucket, put_small_key, private_small_download)
        assert resp.status_code == 403

if __name__ == '__main__':
    unittest.main()
