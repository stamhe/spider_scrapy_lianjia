#!/usr/bin/python
#coding=utf-8

import random
import base64
import requests
import simplejson
import redis

from settings import PROXIES
from time import ctime,sleep

class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        #print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = "http://http-dyn.abuyun.com:9020"
        # 添加账号密码，如果不用账号密码，则下面的代码删除即可
        proxy_user_pass = "HX4OS8905X90183D:C3127131D399C059"
        encoded_user_pass = base64.encodestring(proxy_user_pass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

        return

        proxy = random.choice(PROXIES)
        request.meta['proxy'] = "http://%s" % proxy
        return

        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**************ProxyMiddleware have pass************" + proxy['ip_port']
        else:
            print "**************ProxyMiddleware no pass************" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']

        return



