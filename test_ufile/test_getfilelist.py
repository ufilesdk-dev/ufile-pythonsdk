# -*- coding: utf-8

import unittest
from ucloud.ufile import getufilelist
from ucloud.logger import logger, set_log_file
from ucloud.ufile.config import get_default


public_key = ''
private_key = ''
bucket = ''


class GetFileListTestCase(unittest.TestCase):
    getfilelist_hander = getufilelist.GetFileList(public_key, private_key)

    def test_getfilelist(self):
        self.getfilelist_hander.set_keys(public_key, private_key)
        prefix = ''
        limit = 100
        marker = ''
        ret, resp = self.getfilelist_hander.getfilelist(bucket, prefix=prefix, limit=limit, marker=marker)
        assert resp.status_code == 200
        for item in ret['DataSet']:
            key = item['FileName'].encode('utf-8')
            logger.info(key)
        nextMarker = ret['NextMarker']
        logger.info('NextMarker is {0}'.format(nextMarker))

if __name__ == '__main__':
    unittest.main()
