#!/bin/python3

from pymongo import MongoClient
from os import path, getuid, system
from sys import argv

# check argument, print usage
if len(argv) > 1:
    filename=argv[1]
    fullpath=path.abspath(filename)
else:
    print("Error: Please input file name!")
    print("Usage: arcget fullpath_filename")
    quit()

m=MongoClient("mongodb://hpcuser:12345@127.0.0.1/arcdb")

if path.isfile(fullpath):
    print("Error: File already exists locally")
    quit()

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

system('/bin/sendit get '+fullpath)

# message wait
print("Retreiving file "+fullpath+" from archive tape library, wait and check back later")

