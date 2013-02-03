# coding: utf-8

import os
import json
import pymongo

# mongo config
local = os.environ.get("MONGODB",None)
services = json.loads(os.environ.get("VCAP_SERVICES","{}"))
if services:
    creds = services["mongodb-1.8"][0]["credentials"]
    mongo_uri = "mongodb://%s:%s@%s:%d/%s" % (
        creds["username"],
        creds["password"],
        creds["hostname"],
        creds["port"],
        creds["db"])
else:
    # local mongo
    mongo_uri =  None

reply = pymongo.Connection(mongo_uri).db["reply"]
post = pymongo.Connection(mongo_uri).db["post"]

# site info
SECRET_KEY = "sadk@1jsj&^%%hd(*&"
BLOG_TITLE = u"樱宝宝のBlog"
BLOG_URL ="http://www.xuanmingyi.com"
BLOG_NAME = u""
BLOG_PERPAGE = 8
BLOG_PERARCHIVE = 20

# admin info
ADMIN_INFO = u""
ADMIN_EMAIL = "xuanmingyi@qq.com"
ADMIN_USERNAME = u"樱宝宝"

# login in user and password
ADMIN_USER = "xuanmingyi"
ADMIN_PASSWORD = "123456"
DEFAULT_TIMEZONE = "Asia/Shanghai"
