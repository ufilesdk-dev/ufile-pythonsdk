# -*- coding: utf-8 -*-


import os
import json
from .baseufile import BaseUFile
from .magicwrapper import Mimetype
from .httprequest import ResponseInfo
from ucloud.util import _check_dict
from ucloud.logger import logger
from ucloud.compact import s
from ucloud.ufile import config


class GetFileList(BaseUFile):
    """
    UCloud UFile 获取文件列表类
    """
    def __init__(self, public_key, private_key):
        """
        初始化 GetFileList 实例

        @param public_key: string类型, 账户API公私钥中的公钥
        @param private_key: string类型, 账户API公私钥中的私钥
        @return None，如果为非法的公私钥，则抛出ValueError异常
        """
        super(PutUFile, self).__init__(public_key, private_key)

    def list(self, bucket, marker, limit, header=None):
        """

        @param bucket: string类型，上传空间名称
        @param marker: string类型，上一次查找返回的位置信息,本次列表起始查找的文件名,默认为空
        @param limit:  integer类型, 每次列表返回的最大文件个数,服务端限制为1000,最新限制值请参考官方文档
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
        mime_type = s(Mimetype.from_file(localfile))
        file_size = os.path.getsize(localfile)
        header['Content-Type'] = mime_type
        authorization = self.authorization('put', bucket, key, header)
        header['Authorization'] = authorization
        header['Content-Length'] = file_size
        url = ufile_put_url(bucket, key)
        logger.info('start put file {0} to bucket {1} as {2}'.format(localfile, bucket, key))
        logger.info('put UFile url: {0}'.format(url))
        logger.info('request header:\n{0}'.format(json.dumps(header, indent=4)))
        return _put_file(url, header, localfile)
