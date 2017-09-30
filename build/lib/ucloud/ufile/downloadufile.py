# -*- coding: utf-8 -*-

import os
import time
from .baseufile import BaseUFile
from ucloud.ufile import config
from .httprequest import ResponseInfo, _download_file
from ucloud.util import _check_dict
from ucloud.logger import logger
from ucloud.compact import s
import urllib


class DownloadUFile(BaseUFile):
    """
    UCloud UFile 文件下载类
    """

    def __init__(self, public_key, private_key):
        """
        初始化 DownloadUFile 实例

        @param public_key: string类型, 账户API公私钥中的公钥
        @param private_key: string类型, 账户API公私钥中的私钥
        @return None，如果为非法的公私钥，则抛出ValueError异常
        """
        super(DownloadUFile, self).__init__(public_key, private_key)


    def download_file(self, bucket, key, localfile, isprivate=True, expires=config.get_default('expires'), content_range=None, header=None):
        """
        下载UFile文件并且保存为本地文件

        @param bucket: string类型, UFile空间名称
        @param key: string类型， 下载文件在空间中的名称
        @param localfile: string类型，要保存的本地文件名称
        @param isprivate: boolean类型，如果为私有空间则为True
        @param expires: integer类型，私有文件链接有效时间
        @param content_range: tuple类型，元素为两个整型
        @param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        @return ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        @return  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """
        if header is None:
            header = dict()
        else:
            _check_dict(header)
        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')

        if isinstance(content_range, tuple) and len(content_range) == 2:
            header['Range'] = 'bytes=' + '-'.join(map(lambda x: str(x), content_range))

        if not isprivate:
            url = self.public_download_url(bucket, key)
        else:
            url = self.private_download_url(bucket, key, expires, header, True)

        logger.info('get ufile url:{0}'.format(url))

        return _download_file(url, header, localfile)

    def public_download_url(self, bucket, key):
        """
        从公共空间下载文件的url

        @param bucket: string类型, 空间名称
        @param key: string类型，下载数据在空间中的名称
        @return string类型，下载数据的url
        """
        return 'http://{0}{1}/{2}'.format(bucket, config.get_default('download_suffix'), key)

    def private_download_url(self, bucket, key, expires=config.get_default('expires'), header=None, internal=False):
        """
        从私有空间下载文件的url

        @param bucket: string类型, 空间名称
        @param key: string类型，下载数据在空间中的名称
        @param expires:  integer类型, 下载链接有效时间，单位为秒
        @param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        @return string, 从私有空间下载文件和数据的url
        """
        if header is None:
            header = dict()
        else:
            _check_dict(header)
        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')
        if expires is not None:
            expires += int(time.time())
            header['Expires'] = s(str(expires))
        signature = self.signature(bucket, key, 'get', header)
        query = { 'UCloudPublicKey': self._public_key(),
                  'Expires': str(expires),
                  'Signature': signature }
        query_str = urllib.urlencode(query)
        if internal:
            return 'http://{0}{1}/{2}?{3}'.format(bucket, config.get_default('download_suffix'), key, query_str)
        else:
            return 'http://{0}{1}/{2}?UCloudPublicKey={3}&Expires={4}&Signature={5}'.format(bucket, config.get_default('download_suffix'), key, self._public_key(), str(expires), signature)

    def private_head_url(self, bucket, key, expires=config.get_default('expires'), header=None):
        """
        从私有空间下载文件的url

        @param bucket: string类型, 空间名称
        @param key: string类型，下载数据在空间中的名称
        @param expires:  integer类型, 下载链接有效时间，单位为秒
        @param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        @return string, 从私有空间下载文件和数据的url
        """
        if header is None:
            header = dict()
        else:
            _check_dict(header)
        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')

        if expires is not None:
            expires += int(time.time())
            header['Expires'] = s(str(expires))
        signature = self.signature(bucket, key, 'head', header)
        return 'http://{0}{1}/{2}?UCloudPublicKey={3}&Expires={4}&Signature={5}'.format(bucket, config.get_default('download_suffix'), key, self._public_key(), str(expires), signature)
