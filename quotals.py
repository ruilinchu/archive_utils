#!/bin/python3

from os import getuid, getgid, getgroups
from pymongo import MongoClient
#import logging
 
m=MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")
uid=getuid()

if uid == 0:
    # root show all account
    filt={}
else:
    lst=getgroups()
    #{"$or":[ {"vals":1700}, {"vals":100}]}
    aa=[{"gid":lst[i]} for i in range(0, len(lst))]
    filt={"$or": aa }

doc=m.arcdb.quotagroup.find(filt,{"_id":0})
print(*list(doc), sep="\n")
