#!/bin/python3

from pymongo import MongoClient
from os import stat, path, getuid, system
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

m=MongoClient("mongodb://hpcuser:12345@127.0.0.1/arcdb")

# check if objname already in arcdb
if len(list(m.arcdb.obj.find({"filename": fullpath}))) != 0:
    print("Error: "+fullpath+" already exists on tape!")
    quit()

# check if over group quota, inc num of file and size

# send abspath to putdb redis dataset
system('/bin/sendit put '+fullpath)

# message wait
print("Sending file "+fullpath+" to archive tape library, wait and check back later with arcls")
