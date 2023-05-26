#!/bin/python3

from pymongo import MongoClient

m=MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")

TB=1099511627776 #byte

filt={}
NumFile=list(m.arcdb.obj.aggregate([{"$match":filt},{"$group": {"_id":"", "NumFile":{"$sum":1}}}]))[0]['NumFile']
Size=list(m.arcdb.obj.aggregate([{"$match":filt},{"$group": {"_id":"","Size":{"$sum":"$size"}}}]))[0]['Size']

print("Numfile         Size(TB)")
print(NumFile,Size/TB)
