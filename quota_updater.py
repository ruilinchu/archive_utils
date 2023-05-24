#!/bin/python3

from redis import Redis
from pymongo import MongoClient
import logging

m=MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")
r=Redis(host='127.0.0.1',password='aabbccddeeffgg')

logging.basicConfig(filename='/var/log/archive/quota.log', format='%(asctime)s %(message)s', \
                    filemode='a', level=logging.ERROR)

# default quotas
NumQ=10000
#20TB 1099511627776*20 byte
SizeQ=21990232555520


# start while true sleep loop

while True:
    gido=r.spop("arcgid")
    if gido is None:
        break
    else:
        gid=int(gido.decode("utf-8"))
        filt={"gid": gid}
        try:
            NumFile=list(m.arcdb.obj.aggregate([{"$match":{"gid":gid}},{"$group": {"_id":"$gid", "NumFile":{"$sum":1}}}]))[0]['NumFile']
            Size=list(m.arcdb.obj.aggregate([{"$match":{"gid":gid}},{"$group": {"_id":"$gid", "Size":{"$sum":"$size"}}}]))[0]['Size']
            newvalue={"$set": {"size":Size, "num":NumFile}}
        except:
            logging.error("Error: Quota aggregate for GID "+str(gid)+" failed")
            continue
        
        doc=list(m.arcdb.quotagroup.find(filt))
        if len(doc) == 0:
            #insert one 
            setvalue={"gid":gid, "size":Size, "num":NumFile, "sizelimit":SizeQ, "numlimit":NumQ }
            m.arcdb.quotagroup.insert_one(setvalue)
        elif len(doc) == 1:
            #update one
            m.arcdb.quotagroup.update_one(filt, newvalue)
        elif len(doc) > 1:
            #multi record
            logging.error("Error: multiple records exist for GID "+str(gid))
            #update many
            m.arcdb.quotagroup.update_many(filt, newvalue)

#end while true loop
