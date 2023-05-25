#!/bin/python3

from pymongo import MongoClient
import argparse, sys

parser=argparse.ArgumentParser()

parser.add_argument("--size", help="total file size in byte", type=int, default=21990232555520)
parser.add_argument("--num",  help="total file num", type=int, default=10000)
parser.add_argument("--gid",  help="set quota for gid, '--gid all' apply to all account", type=str, default='666')
args=parser.parse_args()

m=MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")

if args.gid == '666':
    print(parser.format_help())
elif args.gid == 'all':
    # apply to all account
elif:
    # apply to one gid


