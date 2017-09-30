# -*- coding: utf-8 -*-
 
import os
from ucloud.ufile import downloadufile
from ucloud.compact import b
from ucloud.logger import logger, set_log_file
import ucloud.ufile.config as config
from ucloud.compact import BytesIO
import requests
 
set_log_file()
public_key = '7JiqyvdFlW+ndx4pDJn4jaTmaPZPspfxlQjdu4pckND79ek40gyTog==' #添加自己的账户公钥
private_key = 'd415161591de2730cf118c3cd8b1ff25cb1ffc64' #添加自己的账户私钥
 
if __name__ == '__main__':
 
    # 构造下载对象，并设置公私钥
    handler = downloadufile.DownloadUFile(public_key, private_key)
 
    # 目标空间
    bucket = "donaldtest-bj"
    # 目标空间内要下载的文件名
    key = "test_file"
 
    # 获取文件的访问url
    #url = handler.public_download_url(bucket, key)
    # 上一行代码示例为公开空间，可使用私有空间对应方法并设置url过期时间
    url = handler.private_head_url(bucket, key, expires=60)
    print(url)
    ret = requests.head(url)
    print ret.status_code
    #assert ret.status_code == 200
    print ret.headers
    # 之后根据实际的业务逻辑处理返回结果的Header
