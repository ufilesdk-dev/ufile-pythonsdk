# -*- coding: utf-8 -*-

import os
import time
import hashlib
from .baseufile import BaseUFile
from .magicwrapper import Mimetype
from .httprequest import ResponseInfo, _post_file
from ucloud.util import _check_dict, ufile_post_url
from ucloud.logger import logger
from ucloud.compact import b, s, u
from ucloud.ufile import config

class PostUFile(BaseUFile):
    """
    UCloud UFile 表单上传类

    用于计算上传凭证的MIME类型是文件或者二进制数据流的MIME类型
    HTTP请求头中的Content-Type鼻血为'multipart/form-data'
    """

    def __init__(self, public_key, private_key):
        """
        初始化 PostUFile 实例

        @param public_key: string类型, 账户API公私钥中的公钥
        @param private_key: string类型, 账户API公私钥中的私钥
        @return None，如果为非法的公私钥，则抛出ValueError异常
        """
        super(PostUFile, self).__init__(public_key, private_key)

    def postfile(self, bucket, key, localfile, header=None):
        """
        表单上传文件到UFile空间

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
        mime_type = s(Mimetype.from_file(localfile))

        # update the request header content-type
        boundary = self.__make_boundary()
        header['Content-Type'] = 'multipart/form-data; boundary={0}'.format(boundary)

        # form fields
        authorization = self.authorization('post', bucket, key, header, mime_type)
        fields = dict()
        fields['FileName'] = key
        fields['Authorization'] = authorization
        with open(localfile, 'rb') as stream:
            postdata = self.__make_postbody(boundary, fields, stream, mime_type, localfile)

        # update the request header content-length
        header['Content-Length'] = len(postdata)

        # post url
        url = ufile_post_url(bucket)

        # start post file
        logger.info('start post file {0} to bucket {1} as {2}'.format(localfile, bucket, key))
        logger.info('post url is {0}'.format(url))

        return _post_file(url, header, postdata)

    def __make_boundary(self):
        """
        生成post内容主体的限定字符串

        @return: string类型
        """
        t = time.time()
        m = hashlib.md5()
        m.update(b(str(t)))
        return m.hexdigest()

    def __make_postbody(self, boundary, fields, stream, mime_type, localfile):
        """
        生成post请求内容主体

        @param boundary: string类型，post内容主体的限定字符串
        @param fields: ditc类型，键值对类型分别为string类型
        @param stream: 可读的file-like object(file object 或者BytesIO)
        @param mime_type: string类型，上传文件或数据的MIME类型
        @param localfile: string类型，上传文件或数据的本地名称
        @return 二进制数据流
        """

        binarystream = b''
        for (key, value) in fields.items():
            binarystream += b('--{0}\r\n'.format(boundary))
            binarystream += b('Content-Disposition: form-data; name="{0}"\r\n'.format(key))
            binarystream += b('\r\n')
            binarystream += b('{0}\r\n'.format(value))

        binarystream += b('--{0}\r\n'.format(boundary))
        binarystream += b('Content-Disposition: form-data; name="file"; filename="{0}"\r\n'.format(localfile))
        binarystream += b('Content-Type: {0}\r\n'.format(mime_type))
        binarystream += b('\r\n')

        binarystream += stream.read()
        binarystream += b('\r\n')
        binarystream += b('--{0}\r\n'.format(boundary))

        return binarystream
