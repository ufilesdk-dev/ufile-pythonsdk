本源码包含使用Python对UCloud的对象存储业务进行空间和内容管理的API，适用于Python 2和Python 3

## 依赖的Python Package

* **requests**

## 文件目录说明

* ucloud文件夹：              SDK的具体实现
* setup.py:                   package安装文件
* test_ufile文件夹:           测试文件以及demo示例

## 使用方法

> `python setup.py install`

## 功能说明

### 公共参数说明

~~~~~~~~~~~~~~~{.py}
public_key = ''			#账户公私钥中的公钥
private_key = ''		#账户公私钥中的私钥
~~~~~~~~~~~~~~~

### 设置参数

~~~~~~~~~~~~~~~{.py}
from ucloud.ufile import config

#设置上传host后缀,外网可用 .ufile.ucloud.cn
config.set_default(uploadsuffix='YOUR_UPLOAD_SUFFIX')
#设置下载host后缀，比如CDN下载 .ufile.ucloud.com.cn
config.set_default(downloadsuffix='YOUR_DOWNLOAD_SUFFIX')
#设置请求连接超时时间，单位为秒
config.set_default(connection_timeout=60)
#设置私有bucket下载链接有效期,单位为秒
config.set_default(expires=60)
~~~~~~~~~~~~~~~

### 设置日志文件

~~~~~~~~~~~~~~~{.py}
from ucloud import logger

locallogname = '' #完整本地日志文件名
logger.set_log_file(locallogname)
~~~~~~~~~~~~~~~

### 支持普通上传

* demo 程序

~~~~~~~~~~~~~~~{.py}
public_bucket = ''		#公共空间名称
private_bucket = ''		#私有空间名称
localfile = ''			#本地文件名
put_key = ''			#上传文件在空间中的名称

from ucloud.ufile import putufile

putufile_handler = putufile.PutUFile(public_key, private_key)

# 普通上传文件至公共空间
ret, resp = putufile_handler.putfile(public_bucket, put_key, localfile, header=None)
assert rest.status_code == 200

# 普通上传文件至私有空间
ret, resp = putufile_handler.putfile(private_bucket, put_key, localfile, header=None)
assert resp.status_code == 200

# 普通上传二进制数据流至公共空间
from io import BytesIO
bio = BytesIO(u'你好'.encode('utf-8'))  #二进制数据流
stream_key = ''                         #上传数据流在空间中的名称
ret, resp = putufile_handler.putfile(public_bucket, stream_key, bio)
~~~~~~~~~~~~~~~

* HTTP 返回状态码

| 状态码 | 描述 |
| -----  | ---- |
| 200 | 文件或者数据上传成功 |
| 400 | 上传到不存在的空间 |
| 403 | API公私钥错误 |
| 401 | 上传凭证错误 |

### 支持表单上传

* demo程序

~~~~~~~~~~~~~~~{.py}
public_bucket = ''		#公共空间名称
private_bucket = ''		#私有空间名称
localfile = ''			#本地文件名
post_key = ''			#上传文件在空间中的名称

from ucloud.ufile import postufile

postufile_handler = postufile.PostUFile(public_key, private_key)

# 表单上传至公共空间
ret, resp = postufile_handler.postfile(public_bucket, post_key, localfile)
assert resp.status_code == 200

# 表单上传至私有空间
ret, resp = postufile_handler.postfile(private_bucket, post_key, localfile)
assert resp.status_code == 200
~~~~~~~~~~~~~~~

* HTTP 返回状态码

| 状态码 | 描述 |
| -----  | ---- |
| 200 | 文件或者数据上传成功 |
| 400 | 上传到不存在的空间 |
| 403 | API公私钥错误 |
| 401 | 上传凭证错误 |

### 支持秒传

* demo程序

~~~~~~~~~~~~~~~{.py}
public_bucket = ''		#公共空间名称
private_bucket = ''		#私有空间名称
localfile = ''			#本地文件名
nonexistfile = ''		#本地文件名
uploadhit_key = ''		#上传文件在空间中的名称
nonexistkey = ''		#上传文件在空间中的名称

from ucloud.ufile import uploadhitufile

uploadhitufile_handler = uploadhitufile.UploadHitUFile(public_key, private_key)

# 秒传已存在文件
ret, resp = uploadhitufile_handler.uploadhit(public_bucket, uploadhit_key, localfile)
assert resp.status_code == 200

# 秒传不存在文件
ret, resp = uploadhitufile_handler.uploadhit(public_bucket, nonexistkey, nonexistfile)
assert resp.status_code == 404
~~~~~~~~~~~~~~~

* HTTP 状态返回码

| 状态码 | 描述 |
| ------ | ---- |
| 200 | 文件秒传成功 |
| 400 | 上传到不存在的空间 |
| 403 | API公私钥错误 |
| 401 | 上传凭证错误 |
| 404 | 文件秒传失败 |

### 支持文件下载

* demo程序

~~~~~~~~~~~~~~~{.py}
public_bucket = ''			#公共空间名称
private_bucket = ''			#私有空间名称
public_savefile = ''		#保存文件名
private_savefile = ''		#保存文件名
range_savefile = ''			#保存文件名
put_key = ''				#文件在空间中的名称
stream_key = ''				#文件在空间中的名称

from ucloud.ufile import downloadufile

downloadufile_handler = downloadufile.DownloadUFile(public_key, private_key)

# 从公共空间下载文件
ret, resp = downloadufile_handler.download_file(public_bucket, put_key, public_savefile, isprivate=False)
assert resp.status_code == 200

# 从私有空间下载文件
ret, resp = downloadufile_handler.download_file(private_bucket, put_key, private_savefile)
assert resp.status_code == 200

# 下载包含文件范围请求的文件
ret, resp = downloadufile_handler.download_file(public_bucket, put_key, range_savefile, isprivate=False, expires=300, content_range=(0, 50))
assert resp.status_code == 206
~~~~~~~~~~~~~~~

* HTTP 返回状态码

| 状态码 | 描述 |
| -----  | ---- |
| 200 | 文件或者数据下载成功 |
| 206 | 文件或者数据范围下载成功 |
| 400 | 不存在的空间 |
| 403 | API公私钥错误 |
| 401 | 下载签名错误 |
| 404 | 下载文件或数据不存在 |
| 416 | 文件范围请求不合法 |

### 支持删除文件

* demo程序

~~~~~~~~~~~~~~~{.py}
public_bucket = ''				#公共空间名称
private_bucekt = ''				#私有空间名称
delete_key = ''					#文件在空间中的名称

from ucloud.ufile import deleteufile

deleteufile_handler = deleteufile.DeleteUFile(public_key, private_key)

# 删除公共空间的文件
ret, resp = deleteufile_handler.deletefile(public_bucket, delete_key)
assert resp.status_code == 204

# 删除私有空间的文件
ret, resp = deleteufile_handler.deletefile(private_bucket, delete_key)
assert resp.status_code == 204
~~~~~~~~~~~~~~~

* HTTP 返回状态码

| 状态码 | 描述 |
| -----  | ---- |
| 204 | 文件或者数据删除成功 |
| 403 | API公私钥错误 |
| 401 | 签名错误 |

### 支持分片上传和断点续传

* demo程序

~~~~~~~~~~~~~~~{.py}
public_bucket = ''		#公共空间名称
sharding_key = ''		#上传文件在空间中的名称
localfile = ''			#本地文件名

from ucloud.ufile import multipartuploadufile

multipartuploadufile_handler = multipartuploadufile.MultipartUploadUFile(public_key, private_key)

# 分片上传一个全新的文件
ret, resp = multipartuploadufile_handler.uploadfile(public_bucket, sharding_key, localfile)
while True:
if resp.status_code == 200: # 分片上传成功
    break
elif resp.status_code == -1:    # 网络连接问题，续传
    ret, resp = multipartuploadufile_handler.resumeuploadfile()
else:   # 服务或者客户端错误
    print(resp.error)
    break

# 分片上传一个全新的二进制数据流
from io import BytesIO
bio = BytesIO(u'你好'.encode('utf-8'))
ret, resp = multipartuploadufile_handler.uploadstream(public_bucket, sharding_key, bio)
while True:
if resp.status_code == 200:     # 分片上传成功
    break
elif resp.status_code == -1:    # 网络连接问题，续传
    ret, resp = multipartuploadufile_handler.resumeuploadstream()
else:   # 服务器或者客户端错误
    print(resp.error)
    break
~~~~~~~~~~~~~~~

* HTTP 返回状态码

| 状态码 | 描述 |
| -----  | ---- |
| 200 | 文件或者数据上传成功 |
| 400 | 上传到不存在的空间 |
| 403 | API公私钥错误 |
| 401 | 上传凭证错误 |

### 空间管理

~~~~~~~~~~~~~~~{.py}
from ucloud.ufile import bucketmanager

bucketmanager_handler = bucketmanager.BucketManager(public_key, private_key)

# 创建新的bucket
bucketname = '' #创建的空间名称
ret, resp = bucketmanager_handler.createbucket(bucketname, 'public')
assert resp.status_code == 200

# 删除bucket
bucketname = '' #待删除的空间名称
ret, resp = bucketmanager.deletebucket(bucketname)
print(ret)

# 获取bucket信息
bucketname = '' # 待查询的空间名称
ret, resp = bucketmanager.describebucket(public_bucket)
print(ret)

# 更改bucket属性
bucketname = '' # 待更改的私有空间名称
bucketmanager.updatebucket(bucketname, 'public'):

# 获得空间文件列表
bucketname = '' #待查询的空间名称
offset = 0      #文件列表起始位置
limit = 20      #获取文件数量
ret, resp = bucketmanager.getfilelist(bucketname, offset, limit)
print(ret)
~~~~~~~~~~~~~~~
