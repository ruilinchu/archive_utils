#!/bin/python3

# update quota for gid from redis dataset arcgid accumulated during phobos put

from redis import Redis
from pymongo import MongoClient

m=MongoClient("mongodb://phobos:phobos@127.0.0.1/arcdb")
r=Redis(host='127.0.0.1')
