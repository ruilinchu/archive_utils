#!/bin/python3

# scans for redis dataset for data actions: put, get, delete
# send job to rq-worker-put,get 

from redis import Redis
from pymongo import MongoClient
from rq import Queue
import os
import traceback
import logging

r=Redis(host='127.0.0.1')
m=MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")
qput=Queue("phoboput",connection=r)
qget=Queue("phoboget",connection=r)

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
        fpath=filepath.decode("utf-8")
        filename=os.path.basename(fpath)
        parent=os.path.dirname(fpath)
        objname=fpath
        # stat
        try:
            ost=os.stat(fpath)
        except Exception as e:
            logging.error(traceback.format_exc())

        uid=ost.st_uid
        gid=ost.st_gid
        fsize=ost.st_size
        ftime=ost.st_ctime
        # insert mongodb record
        try:
            m.arcdb.obj.insert_one("filename": filename, "parent": parent, "objname": objname, "uid": uid, "gid": gid, size: fsize, "timestamp": ftime)
        except Exception as e:
            logging.error(traceback.format_exc())

        # send job to rq-worker-put, original file removed after job finish
        qput.enqueue(putfile, fpath)

        # queue up gid for quota_updater after this round of scan
        r.sadd("arcgid",gid)

# get scanner
while True:
    filepath=r.spop("arcget")
    if filepath is None:
        break
    else:
        print(filepath.decode("utf-8"))
        # send job to rq-worker-get
        # qget.enqueue(getfile, filepath.decode("utf-8"))

# delete scanner
while True:
    filepath=r.spop("arcdel")
    if filepath is None:
        break
    else:
        print(filepath.decode("utf-8"))
        # delete file entry in arcdb.obj
        # call phobos delete, data on tape remain until overwritten

        # queue up gid for quota_updater
        # query arcdb for uid gid
        # r.sadd("arcgid",gid)

# call quota_updater for gid saved in this scan

## end while true sleep loop

