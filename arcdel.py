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
    print("Usage: arcdel fullpath_filename")
    quit()

r=Redis(host='127.0.0.1')
m=MongoClient("mongodb://hpcuser:12345@127.0.0.1/arcdb")

# verify ownership
docl=list(m.arcdb.obj.find({"filename":fullpath},{"uid":1,"gid":1,"_id":0}))
if len(docl) == 0:
    print("Error: "+fullpath+" does not exist on tape")
    quit()

doc=docl[0]
uid=doc['uid']

if uid != getuid():
    print("Error: "+fullpath+" is not owned by you!")
    quit()

# ask to confirm
if input("are you sure to delete this file from tape? (y/n)") == "y":
    # send abspath to putdb redis dataset   
    r.sadd("arcdel",fullpath)

    # message 
    print("Deleted file "+fullpath+" from archive tape library")


