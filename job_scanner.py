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
from arc_utils import put2tape,getfromtape,delfromtape

r=Redis(host='127.0.0.1')
m=MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")
qput=Queue("phobosput",connection=r)
qget=Queue("phobosget",connection=r)
qdel=Queue("phobosdel",connection=r)

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
        logging.error("PUT: "+fpath)

# get scanner
while True:
    filepath=r.spop("arcget")
    if filepath is None:
        break
    else:
        fpath=filepath.decode("utf-8")
        print(fpath)

        # send job to rq-worker-get
        qget.enqueue(getfromtape, fpath)
        logging.error("GET: "+fpath)

# delete scanner
while True:
    filepath=r.spop("arcdel")
    if filepath is None:
        break
    else:
        fpath=filepath.decode("utf-8")
        print(fpath)

        # send job to rq-worker-delete
        qdel.enqueue(delfromtape, fpath)
        logging.error("DEL: "+fpath)


# use another periodic quota_updater for gid 

## end while true sleep loop

