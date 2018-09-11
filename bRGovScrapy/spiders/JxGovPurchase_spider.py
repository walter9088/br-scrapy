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
    name = "jx_gov_purchase"
    allowed_domains = ["jxsggzy.cn"]
    start_urls = ["http://www.jxsggzy.cn/web/jyxx/002006/002006001/jyxx.html"]


    def parse(self,response):

        dome_url = 'http://www.jxsggzy.cn'
        data = response.body

        soup = BeautifulSoup(data)


        list_box = soup.find_all("div", class_='ewb-infolist')

        a_list = list_box[0].find_all('a')

        yesterday_str = '2018-09-11'


        for a in a_list:

            #每天爬取前一天数据，对日期做一个限色
            date_web = a.find_next("span",class_='ewb-list-date').string

            item = BrgovscrapyItem()

            if date_web == yesterday_str:

                URL = dome_url +a['href']


                page = urllib2.urlopen('http://www.jxsggzy.cn/web/jyxx/002006/002006001/20180911/fc08669a-caa0-4965-82df-5a46b1c31c1f.html')


                d_soup = BeautifulSoup(page)

                qd_tables = d_soup.find_all("table")

                if len(qd_tables)>0:
                    qd_table = qd_tables[0]
                else:
                    continue

                key = jieba.analyse.extract_tags(qd_table.getText(), topK=50, withFlag=False, allowPOS=('n', 'vn', 'v', 'brn'))

                keywords = ''

                for k in key:
                    keywords = keywords + k + ' '

                print keywords
                item['keywords'] = key
                item['url'] = URL
                item['title'] = yesterday_str
                yield item



