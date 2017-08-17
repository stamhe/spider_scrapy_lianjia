#!/usr/bin/python
#coding=utf-8

import redis
import requests
import simplejson

from time import ctime,sleep

r=redis.Redis(host='127.0.0.1',port=6379,db=1)


while True:
    #ret = requests.get('http://proxy.mimvp.com/api/fetch.php?orderid=860170816220507267&num=5000&http_type=1&anonymous=3,5&check_success_count=10&result_format=json')
    ret = requests.get('http://proxy.mimvp.com/api/fetch.php?orderid=860170816220507267&num=5000&http_type=1&anonymous=3,5&ping_time=1&transfer_time=5&check_success_count=100&result_format=json')
    if ret.status_code != 200:
        print "no data 1"
        continue

    data_json = ret.text
    data_arr = simplejson.loads(data_json)
    if len(data_arr['result']) < 1:
        print "no data 2"
        sleep(10)
        continue

    ip_json=simplejson.dumps(data_arr['result']) 
    r.set("ip_list", ip_json)
    print "ip_json = %s" % (ip_json)
    sleep(120)

    


