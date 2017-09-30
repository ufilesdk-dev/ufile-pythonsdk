# -*- coding: utf-8 -*-

"""
test bucket
"""

from ucloud.ufile import bucketmanager


public_key = '' #添加自己的账户公钥
private_key = '' #添加自己的账户私钥
public_bucket = '' #公共空间名称
private_bucket = '' #私有空间名称

# create public bucket
bucketmanager = bucketmanager.BucketManager(public_key, private_key)
ret, resp = bucketmanager.createbucket(public_bucket, 'public')
print(ret)
# create private bucket
ret, resp = bucketmanager.createbucket(private_bucket, 'private')
print(ret)
# delete public bucket
ret, resp = bucketmanager.deletebucket(public_bucket)
print(ret)
# delete private bucket
ret, resp = bucketmanager.deletebucket(private_bucket)
print(ret)
# describle public bucket
ret, resp = bucketmanager.describebucket(public_bucket)
print(ret)
# describe private bucket
ret, resp = bucketmanager.describebucket(private_bucket)
print(ret)
# get a list of files from a bucket
ret, resp = bucketmanager.getfilelist(public_bucket, projectid='org-5150')
print(ret)
