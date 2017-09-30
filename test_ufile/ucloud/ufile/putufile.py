# -*- coding: utf-8 -*-


import os
import json
from .baseufile import BaseUFile
from .magicwrapper import Mimetype
from .httprequest import _put_stream, _put_file, ResponseInfo
from ucloud.util import _check_dict, ufile_put_url
from ucloud.logger import logger
from ucloud.compact import s
from ucloud.ufile import config


class PutUFile(BaseUFile):
    """
    UCloud UFile普通上传文件类
    """
    def __init__(self, public_key, private_key):
        """
        初始化 PutUFile 实例

        @param public_key: string类型, 账户API公私钥中的公钥
        @param private_key: string类型, 账户API公私钥中的私钥
        @return None，如果为非法的公私钥，则抛出ValueError异常
        """
        super(PutUFile, self).__init__(public_key, private_key)

    def putstream(self, bucket, key, stream, mime_type=None, header=None):
        """
        上传二进制流到空间

        @param bucket: string类型，上传空间名称
        @param key:  string 类型，上传文件在空间中的名称
        @param stream: 二进制数据流,从文件指针位置开始发送数据,在调用时需调用者自己调整文件指针位置
        @param mime_type: 二进制数据流的MIME类型
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

        if mime_type is None:
            mime_type = 'application/octet-stream'
        header['Content-Type'] = mime_type
        authorization = self.authorization('put', bucket, key, header)
        header['Authorization'] = authorization
        url = ufile_put_url(bucket, key)
        logger.info('start put stream to bucket {0} as {1}'.format(bucket, key))
        logger.info('put UFile url: {0}'.format(url))
        logger.info('request header:\n{0}'.format(json.dumps(header, indent=4)))
        return _put_stream(url, header, stream)

    def putfile(self, bucket, key, localfile, header=None):
        """
        upload localfile to bucket as key

        @param bucket: string类型，上传空间名称
        @param key:  string 类型，上传文件在空间中的名称
        @param localfile: string类型，本地文件名称
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
