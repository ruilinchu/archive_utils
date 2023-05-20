#!/bin/python3

# scans for redis dataset for data actions: put, get, delete
# send job to rq-worker-put,get 

from redis import Redis
from pymongo import MongoClient
from rq import Queue
import os
import traceback
import logging
import datetime
from arc_utils import put2tape
from arc_utils import getfromtape

r=Redis(host='127.0.0.1')
m=MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")
qput=Queue("phobosput",connection=r)
qget=Queue("phobosget",connection=r)

logging.basicConfig(filename='/var/log/archive/scanner.log', format='%(asctime)s %(message)s', \
                    filemode='a', level=logging.ERROR)

## start while true, sleep(60) loop, will run as systemd service

# put scanner
while True:
    filepath=r.spop("arcput")
    if filepath is None:
        break
    else:
        ## input is a full abspath
        fpath=filepath.decode("utf-8")
        print(fpath)

        # send job to rq-worker-put, original file stays
        qput.enqueue(put2tape, fpath)
        logging.error(fpath)
        

# get scanner
while True:
    filepath=r.spop("arcget")
    if filepath is None:
        break
    else:
        print(filepath.decode("utf-8"))
        # send job to rq-worker-get
        qget.enqueue(getfromtape, filepath.decode("utf-8"))

# delete scanner
while True:
    filepath=r.spop("arcdel")
    if filepath is None:
        break
    else:
        print(filepath.decode("utf-8"))
        fpath=filepath.decode("utf-8")


        # call phobos delete, data on tape remain until overwritten
        os.system('/bin/phobos delete '+fpath)
        # queue up gid for quota_updater, query arcdb for gid

        r.sadd("arcgid",gid)
        # delete file entry in arcdb.obj

# call quota_updater for gid saved in this scan

## end while true sleep loop

