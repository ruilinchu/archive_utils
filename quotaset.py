#!/bin/python3

from pymongo import MongoClient
import argparse, sys

parser=argparse.ArgumentParser()

parser.add_argument("--size", help="total file size in byte, default 20TB", type=int, default=21990232555520)
parser.add_argument("--num",  help="total file num, default 10k", type=int, default=10000)
parser.add_argument("--gid",  help="set quota for gid, '--gid all' apply to all account", type=str, default='None')
args=parser.parse_args()

m=MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")

newvalue={"$set": {"sizelimit":args.size, "numlimit":args.num}}

if args.gid == 'None':
    print(parser.format_help())
    quit()
elif args.gid == 'all':
    # apply to all account
    print("Setting quota for ALL accounts, size: "+str(args.size)+", num: "+str(args.num))
    m.arcdb.quotagroup.update_many({}, newvalue)
else:
    # apply to one gid
    print("Setting quota for GID: "+args.gid+", size: "+str(args.size)+", num: "+str(args.num))
    m.arcdb.quotagroup.update_many({"gid": int(args.gid)}, newvalue)



