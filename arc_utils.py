from os import stat, system, path
from datetime import datetime
from pymongo import MongoClient
from redis import Redis

def put2tape(filepatho):
    m=MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")
    r=Redis(host='127.0.0.1',password='aabbccddeeffgg')
    
    x=1
    filepath=path.dirname(filepatho)
    uido=path.basename(filepatho)

    # check if already in mongodb, repeat action
    if len(list(m.arcdb.obj.find({"filename": filepath}))) != 0:    
        print("Error: "+filepath+" aready on Tape")
        return 1

    # check if is already working on it
    if r.sismember("workingput",filepath):
        print("Error: already working on a put file")
        return 1
    else:
        r.sadd("workingput",filepath)
    
    try:
        # stat
        ost=stat(filepath)
        uid=ost.st_uid
        gid=ost.st_gid
        fsize=ost.st_size
        ftime=str(datetime.fromtimestamp(ost.st_ctime))
        
        if uid != int(uido):
            print("Alert: someone is sending redis key manually for other user's data !!!")
            return 1

        #x=system('/bin/phobos put -f tape '+filepath+' '+filepath)
        x=system('/bin/phobos put -f dir '+filepath+' '+filepath)
        
        # insert mongodb record
        # queue up gid for quota_updater
        r.sadd("arcgid",gid)
        m.arcdb.obj.insert_one({"filename": filepath, "uid": uid, "gid": gid, "size": fsize, "timestamp": ftime})
    except:
        pass

    # remove from working on list
    r.srem("workingput",filepath)

    return x

def getfromtape(objnameo):
    # filename = objname
    m=MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")
    r=Redis(host='127.0.0.1',password='aabbccddeeffgg')

    x=1
    objname=path.dirname(objnameo)
    uido=path.basename(objnameo)
    
    docl=list(m.arcdb.obj.find({"filename":objname},{"uid":1,"gid":1,"_id":0}))
    if len(docl) == 0:
        print("Error: "+objname+" does not exist on tape")
        return 1

    doc=docl[0]


    # check if is already working on it
    if r.sismember("workingget",objname):
        print("Error: already working on a get file")
        return 1
    else:
        r.sadd("workingget",objname)
        
    try:
        uid=str(doc['uid'])
        gid=str(doc['gid'])
        if uid != uido:
            print("Alert: someone is sending redis key manually to get other user's data !!!")
            return 1

        targetdir=path.dirname(objname)
        x=system('mkdir -p '+targetdir+ ' && /bin/phobos get '+objname+' '+objname)

        # restore ownership
        system('chown '+uid+':'+gid+' '+objname)
    except:
        pass

    # remove from working on list
    r.srem("workingget",objname)

    return x

def delfromtape(objnameo):
    #data on tape remain until overwritten, filename = objname
    m=MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")
    r=Redis(host='127.0.0.1',password='aabbccddeeffgg')

    x=1
    objname=path.dirname(objnameo)
    uido=path.basename(objnameo)

    docl=list(m.arcdb.obj.find({"filename":objname},{"uid":1,"gid":1,"_id":0}))
    if len(docl) == 0:
        print("Error: "+objname+" does not exist on tape")
        return 1

    doc=docl[0]
    uid=str(doc['uid'])
    if uid != uido:
        print("Alert: someone is sending redis key manually to delete other user's data !!!")
        return 1

    x=system('/bin/phobos delete '+objname)

    # queue up gid for quota_updater, query arcdb for gid
    gid=doc['gid']
    r.sadd("arcgid",gid)
    
    # delete file entry in arcdb.obj
    m.arcdb.obj.delete_one({"filename": objname})

    return x


