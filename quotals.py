#!/bin/python3

from pymongo import MongoClient
#import logging
 
m=MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")

doc=m.arcdb.quotagroup.find({},{"_id":0})
print(*list(doc), sep="\n")
