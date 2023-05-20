#!/bin/python3

import os
import sys
import pymongo

## readonly
##client=pymongo.MongoClient("mongodb://hpcuser:12345@127.0.0.1/arcdb")

## readwrite
client=pymongo.MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")

db=client.arcdb

doc=db.obj.find({"uid": 0},{"_id":0})
#doc=db.obj.find({"parent": parent})
print(*list(doc), sep="\n")

