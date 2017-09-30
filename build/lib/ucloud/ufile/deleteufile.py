# -*- coding: utf-8 -*-

from .baseufile import BaseUFile
from ucloud.util import _check_dict, ufile_put_url
from .httprequest import ResponseInfo, _delete_file
from ucloud.logger import logger
from ucloud.ufile import config


class DeleteUFile(BaseUFile):
    """
    UCloud UFile 删除文件类
    """

    def __init__(self, public_key, private_key):
        """
        初始化 DeleteUFile 实例

        @param public_key: string类型, 账户API公私钥中的公钥
        @param private_key: string类型, 账户API公私钥中的私钥
        @return None，如果为非法的公私钥，则抛出ValueError异常
        """
        super(DeleteUFile, self).__init__(public_key, private_key)

    def deletefile(self, bucket, key, header=None):
        """
        删除空间中文件方法

        @param bucket: string类型, 空间名称
        @param key:  string类型, 被删除文件在空间中的名称
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

        authorization = self.authorization('delete', bucket, key, header)
        header['Authorization'] = authorization

        logger.info('start delete file {0} in bucket {1}'.format(key, bucket))
        url = ufile_put_url(bucket, key)

        return _delete_file(url, header)
