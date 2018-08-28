# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json

import urllib2

class BrgovscrapyPipeline(object):

    def __init__(self):
        self.file = open('items.json','wb')
        requrl = 'http://127.0.0.1:8080/gov.html'
        headerdata = {"Content-type": "application/json"}

    def process_item(self, item, spider):

        line = json.dumps(dict(item))

        request = urllib2.Request(url=self.requrl, headers=self.headerdata, data=line)
        response = urllib2.urlopen(request)




        return item