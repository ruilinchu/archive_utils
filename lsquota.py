#!/bin/python3

from redis import Redis
from pymongo import MongoClient
#import logging
 
m=MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")
r=Redis(host='127.0.0.1',password='aabbccddeeffgg')

doc=m.arcdb.quotagroup.find({},{"_id":0})
print(*list(doc), sep="\n")
