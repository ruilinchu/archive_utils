#!/bin/python3

# scans for redis dataset for data actions: put, get, delete
# send job to rq-worker-put,get 

import redis
import pymongo

r=redis.Redis(host='127.0.0.1')
m=pymongo.MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")
print(m.list_database_names())

# put dummy data in arcput,arcget dataset
for x in range(10):
    filename="file"+str(x)
    r.sadd("arcput","/put/some/"+filename)
    r.sadd("arcget","/get/some/"+filename)
    r.sadd("arcdel","/del/some/"+filename)


print(r.smembers("arcput"))
print(r.smembers("arcget"))
print(r.smembers("arcdel"))

## start while true, sleep(60) loop
# put scanner

while True:
    filepath=r.spop("arcput")
    if filepath is None:
        break
    else:
        print(filepath.decode("utf-8"))
        # send job to rq-worker-put

# get scanner

while True:
    filepath=r.spop("arcget")
    if filepath is None:
        break
    else:
        print(filepath.decode("utf-8"))
        # send job to rq-worker-get

# delete scanner
while True:
    filepath=r.spop("arcdel")
    if filepath is None:
        break
    else:
        print(filepath.decode("utf-8"))
        # delete file entry in arcdb.obj, data on tape remain until overwritten

## end while true sleep loop

