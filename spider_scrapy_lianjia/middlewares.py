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
        #request.headers.setdefault('User-Agent', random.choice(self.agents))
        ua =  random.choice(self.agents)
        request.headers.setdefault('User-Agent', ua)

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        # 阿布云
        request.meta['proxy'] = "http://http-dyn.abuyun.com:9020"
        # 添加账号密码，如果不用账号密码，则下面的代码删除即可
        proxy_user_pass = "HX4OS8905X90183D:C3127131D399C059"
        encoded_user_pass = base64.encodestring(proxy_user_pass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        #print "proxy = %s" (request.meta['proxy'])

        return



