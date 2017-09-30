#-*- coding: utf-8 -*-

import os
import json
from .baseufile import BaseUFile
from .httprequest import _getfilelist, ResponseInfo
from ucloud.util import _check_dict, ufile_getfilelist_url
from ucloud.logger import logger
from ucloud.ufile import config
from ucloud.compact import s

class GetFileList(BaseUFile):
    """
    UCloud UFile获取文件列表类
    """
    def __init__(self, public_key, private_key):
        """
        初始化 GetFileList 实例

        @param public_key: string 类型，账户API公私钥中的公钥
        @param private_key: string 类型，账户API公私钥中的私钥
        @return None, 如果为非法的公私钥，则抛出ValueError异常
        """
        super(GetFileList, self).__init__(public_key, private_key)

    def getfilelist(self, bucket, prefix=None, marker=None, limit=None, header=None):
        """
        获取bucket下的文件列表

        @param bucket: string 类型，空间名称
        @param prefix: string 类型，文件前缀, 默认为空字符串
        @param marker: string 类型，文件列表起始位置, 默认为空字符串
        @param limit: integer 类型，文件列表数目, 默认为20
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

        header['Content-Length'] = 0
        authorization = self.authorization('get', bucket, '', header)
        header['Authorization'] = authorization
        param = dict()
        if marker is not None and (isinstance(marker, str) or isinstance(marker, unicode)):
            param['marker'] = s(marker)
        if prefix is not None and (isinstance(prefix, str) or isinstance(prefix, unicode)):
            param['prefix'] = s(prefix)
        if limit is not None and isinstance(limit, int):
            param['limit'] = s(str(limit))
        info_message = ''.join(['start get file list from bucket {0}'.format(bucket), '' if marker is None else ', marker: {0}'.format(marker if isinstance(marker, str) else marker.encode('utf-8')), '' if limit is None else ', limit: {0}'.format(limit), '' if prefix is None else ', prefix: {0}'.format(prefix)])
        logger.info(info_message)
        url = ufile_getfilelist_url(bucket)
        return _getfilelist(url, header, param)
