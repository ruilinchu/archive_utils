#!/bin/python3

# scans for redis dataset for data actions: put, get, delete
# send job to rq-worker-put,get 

from redis import Redis
from pymongo import MongoClient
from rq import Queue

r=Redis(host='127.0.0.1')
m=MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")
q=Queue(connection=r)

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

## start while true, sleep(60) loop, will run as systemd service

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

