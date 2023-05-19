#!/bin/python3

from redis import Redis
from pymongo import MongoClient
import os
import sys
import traceback

# check argument, print usage
if len(sys.argv) > 1:
    filename=sys.argv[1]
    fullpath=os.path.abspath(filename)
else:
    print("Error: Please input file name")
    quit()

# check if abspath contains space
if ' ' in fullpath:
    print("Error: File full path contains space!")
    quit()

# validate file
ost=os.stat(fullpath)
uid=ost.st_uid
gid=ost.st_gid

# verify ownership
if uid != os.getuid():
    print("Error: "+fullpath+" is not owned by you")
    quit()

r=Redis(host='127.0.0.1')
m=MongoClient("mongodb://hpcuser:12345@127.0.0.1/arcdb")

# check if objname already in arcdb

# check if over group quota

# send abspath to putdb redis dataset

# message wait
