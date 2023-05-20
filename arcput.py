#!/bin/python3

from redis import Redis
from pymongo import MongoClient
import os
import sys

# check argument, print usage
if len(sys.argv) > 1:
    filename=sys.argv[1]
    fullpath=os.path.abspath(filename)
else:
    print("Error: Please input file name!")
    quit()

# check if abspath contains space
if ' ' in fullpath:
    print("Error: File full path contains space!")
    quit()

# validate file
if os.path.isfile(fullpath):
    ost=os.stat(fullpath)
    uid=ost.st_uid
    gid=ost.st_gid
else:
    print("Error: input is not a file!")
    quit()

# verify ownership
if uid != os.getuid():
    print("Error: "+fullpath+" is not owned by you!")
    quit()

r=Redis(host='127.0.0.1')
m=MongoClient("mongodb://hpcuser:12345@127.0.0.1/arcdb")

# check if objname already in arcdb
if len(list(m.arcdb.obj.find({"filename": fullpath}))) != 0:
    print("Error: "+fullpath+" already exists on tape!")
    quit()

# check if over group quota

# send abspath to putdb redis dataset
r.sadd("arcput",fullpath)

# message wait
print("Sending file "+fullpath+" to archive tape library, wait and check back later with arcls")
