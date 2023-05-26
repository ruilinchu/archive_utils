#!/bin/python3

from pymongo import MongoClient

m=MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")

TB=1099511627776 #byte

filt={}
NumFile=list(m.arcdb.obj.aggregate([{"$match":filt},{"$group": {"_id":"$gid", "NumFile":{"$sum":1}}}]))
Size=list(m.arcdb.obj.aggregate([{"$match":filt},{"$group": {"_id":"$gid","Size":{"$sum":"$size"}}}]))

N=0
S=0
for n in NumFile:
    N=N + n['NumFile']

for s in Size:
    S=S + s['Size']

print("Numfile         Size(TB)")
print(N,S/TB)
