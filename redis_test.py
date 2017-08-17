#!/usr/bin/python
#coding=utf-8

import redis
import requests
import simplejson
import random

from time import ctime,sleep

r=redis.Redis(host='127.0.0.1',port=6379,db=1)

ip_json = r.get("ip_list")
ip_list = simplejson.loads(ip_json)

ip_count = len(ip_list)

ip_info = random.choice(ip_list)
print ip_info
print ip_info['ip:port']

