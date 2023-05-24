#!/bin/python3

# update quota for gid from redis dataset arcgid accumulated during phobos put

from redis import Redis
from pymongo import MongoClient

m=MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")
r=Redis(host='127.0.0.1',password='aabbccddeeffgg')

# start while true sleep loop

while True:
    gido=r.spop("arcgid")
    if gido is None:
        break
    else
        gid=gido.decode("utf-8")
        NumFile=list(m.arcdb.obj.aggregate([{"$match":{"gid":gid}},{"$group": {"_id":"$gid", "NumFile":{"$sum":1}}}]))[0]['NumFile']
        Size=list(m.arcdb.obj.aggregate([{"$match":{"gid":gid}},{"$group": {"_id":"$gid", "Size":{"$sum":"$size"}}}]))[0]['Size']


#end while true loop
