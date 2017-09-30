# -*- coding: utf-8 -*-

import os
from .baseufile import BaseUFile
from ucloud.util import file_etag, _check_dict, ufile_uploadhit_url
from ucloud.ufile.config import BLOCKSIZE
from .httprequest import ResponseInfo, _uploadhit_file
from ucloud.logger import logger
from .magicwrapper import Mimetype
from ucloud.compact import s
from ucloud.ufile import config


class UploadHitUFile(BaseUFile):
    """
    UCloud UFile 秒传文件类
    """

    def __init__(self, public_key, private_key):
        """
        初始化 UploadHitUFile 对象

        @param public_key: string类型, 账户API公私钥中的公钥
        @param private_key: string类型, 账户API公私钥中的私钥
        @return None，如果为非法的公私钥，则抛出ValueError异常
        """
        super(UploadHitUFile, self).__init__(public_key, private_key)

    def uploadhit(self, bucket, key, localfile, header=None):
        """
        尝试秒传文件到UFile空间

        @param bucket: string类型，上传空间名称
        @param key:  string 类型，上传文件在空间中的名称
        @param localfile: string类型，本地文件名称
        @param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
        @return ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
        @return  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
        """

        if header is None:
            header = dict()
        _check_dict(header)
        if 'User-Agent' not in header:
            header['User-Agent'] = config.get_default('user_agent')

        filesize = os.path.getsize(localfile)
        fileetags = file_etag(localfile, BLOCKSIZE)
        mimetype = s(Mimetype.from_file(localfile))

        # update request header
        header['Content-Type'] = mimetype
        header['Content-Length'] = 0
        authorization = self.authorization('post', bucket, key, header)
        header['Authorization'] = authorization

        # parameter

        params = {'Hash': fileetags,
                  'FileName': key,
                  'FileSize': filesize}

        url = ufile_uploadhit_url(bucket)

        logger.info('start upload hit localfile {0} as {1} in bucket {2}'.format(localfile, key, bucket))
        logger.info('request url: {0}'.format(url))

        return _uploadhit_file(url, header, params)
