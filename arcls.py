#!/bin/python3

from os import getuid
from sys import argv
from pymongo import MongoClient

# readonly
m=MongoClient("mongodb://hpcuser:12345@127.0.0.1/arcdb")

if getuid() == 0:
    doc=m.arcdb.obj.find({},{"_id":0})
else:
    doc=m.arcdb.obj.find({"uid":getuid()},{"_id":0})

print(*list(doc), sep="\n")

