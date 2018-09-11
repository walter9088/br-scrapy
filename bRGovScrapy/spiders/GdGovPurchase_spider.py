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
    name = "gd_gov_purchase"
    allowed_domains = ["gdgpo.gov.cn"]
    start_urls = ["http://www.gdgpo.gov.cn/queryMoreInfoList/channelCode/0005.html"]


    def parse(self,response):

        dome_url = 'http://www.gdgpo.gov.cn/'
        data = response.body

        soup = BeautifulSoup(data)


        list_box = soup.find_all("ul", class_='m_m_c_list')


        print len(list_box),'============'

        a_list = list_box[0].find_all('a')



        yesterday_str = '2018-09-11'


        for a in a_list:

            #每天爬取前一天数据，对日期做一个限色
            date_web = a.find_next("em").string

            #这里是测试使用，可自行修改
            date_web = '2018-09-11'

            item = BrgovscrapyItem()

            print a['href']

            if date_web == yesterday_str:

                if a['href'] == 'javascript:void(0);':
                    continue

                URL = dome_url +a['href']


                page = urllib2.urlopen(URL)


                d_soup = BeautifulSoup(page)

                qd_tables = d_soup.find_all("table")

                if len(qd_tables)>0:
                    qd_table = qd_tables[0]

                    key = jieba.analyse.extract_tags(qd_table.getText(), topK=50, withFlag=False,
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





