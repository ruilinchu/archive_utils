#!/bin/python3

# delete object from tape
# verify data ownership
# ask for confirm
# send filepath to arcput redis dataset

from redis import Redis
from pymongo import MongoClient

r=Redis(host='127.0.0.1')
m=MongoClient("mongodb://hpcuser:12345@127.0.0.1/arcdb")

