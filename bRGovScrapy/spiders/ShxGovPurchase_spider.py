# -*- coding: utf-8 -*-
import scrapy
import urllib2
import jieba.analyse
import datetime
from datetime import timedelta


from bs4 import BeautifulSoup

#import html5lib
from bRGovScrapy.items import BrgovscrapyItem

jieba.load_userdict('data/dict.txt')
jieba.analyse.set_stop_words('data/stopword.txt')

date = datetime.date.today()
yesterday = date + timedelta(days = -1)

yesterday_str = str(yesterday)

class NcGovPurchase(scrapy.Spider):
    name = "shx_gov_purchase"
    allowed_domains = ["ccgp-shaanxi.gov.cn"]
    start_urls = ["http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3&province=province&isgovertment="]


    def parse(self,response):


        data = response.body

        soup = BeautifulSoup(data)


        list_box = soup.find_all("table", class_='table table-no tab-striped tab-hover')

        a_list = list_box[0].find_all('a')



        yesterday_str = '2018-09-11'


        for a in a_list:

            #每天爬取前一天数据，对日期做一个限色
            date_web = a.find_next("td").string

            item = BrgovscrapyItem()

            print a['href']

            if date_web == yesterday_str:

                URL = a['href']

                page = urllib2.urlopen(URL)


                d_soup = BeautifulSoup(page)

                qd_tables = d_soup.find_all("p",class_='title1')



                if len(qd_tables)>0:

                    for p in qd_tables:
                        if p.getText().find(u'五、采购内容和需求：') > -1:
                            st =  p.find_next("p").string
                            qd_table = qd_tables[0]

                            key = jieba.analyse.extract_tags(st, topK=50, withFlag=False,
                                                             allowPOS=('n', 'vn', 'v', 'brn'))

                            keywords = ''

                            print key

                            for k in key:
                                keywords = keywords + k + ' '

                            print keywords
                            item['keywords'] = key
                            item['url'] = URL
                            item['title'] = yesterday_str
                            yield item

                        else:
                            continue





