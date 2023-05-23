#!/bin/python3

from redis import Redis
from pymongo import MongoClient
from os import stat, path, getuid
from sys import argv

# check argument, print usage
if len(argv) > 1:
    filename=argv[1]
    fullpath=path.abspath(filename)
else:
    print("Error: Please input file name!")
    print("Usage: arcput filename")
    quit()

# check if abspath contains space
if ' ' in fullpath:
    print("Error: File full path contains space!")
    quit()

# validate file
if path.isfile(fullpath):
    ost=stat(fullpath)
    uid=ost.st_uid
    gid=ost.st_gid
else:
    print("Error: input is not a file!")
    quit()

# verify ownership
if uid != getuid():
    print("Error: "+fullpath+" is not owned by you!")
    quit()

r=Redis(host='127.0.0.1')
m=MongoClient("mongodb://hpcuser:12345@127.0.0.1/arcdb")

# check if objname already in arcdb
if len(list(m.arcdb.obj.find({"filename": fullpath}))) != 0:
    print("Error: "+fullpath+" already exists on tape!")
    quit()

# check if already working on it
if r.sismember("workingput",fullpath):
    print("Error: already working on it")
    quit()

# check if over group quota, check num of file and size

# send abspath to putdb redis dataset
r.sadd("arcput",fullpath)

# message wait
print("Sending file "+fullpath+" to archive tape library, wait and check back later with arcls")
