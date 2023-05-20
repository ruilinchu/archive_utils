from os import stat, system, path
from datetime import datetime
import traceback
import logging
from pymongo import MongoClient
from redis import Redis

def put2tape(filepath):
    m=MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")
    r=Redis(host='127.0.0.1')

    # stat
    try:
        ost=stat(filepath)
        uid=ost.st_uid
        gid=ost.st_gid
        fsize=ost.st_size
        ftime=datetime.fromtimestamp(ost.st_ctime)
    except Exception as e:
        logging.error(traceback.format_exc())
    
    #x=system('/bin/phobos put -f tape '+filepath+' '+filepath)
    x=system('/bin/phobos put -f dir '+filepath+' '+filepath)
    
    # insert mongodb record
    try:
        # queue up gid for quota_updater
        r.sadd("arcgid",gid)
        m.arcdb.obj.insert_one({"filename": fpath, "uid": uid, "gid": gid, size: fsize, "timestamp": ftime})
    except Exception as e:
        logging.error(traceback.format_exc())

    return x

def getfromtape(objname):
    # filename = objname
    targetdir=path.dirname(objname)
    x=system('mkdir -p '+targetdir+ ' && /bin/phobos get '+objname+' '+targetdir)
    return x
