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
    name = "nc_gov_purchase"
    allowed_domains = ["ncszfcg.gov.cn"]
    start_urls = ["http://www.ncszfcg.gov.cn/more2018.cfm?sid=100002003&c_code=&area="]


    def parse(self,response):

        dome_url = 'http://www.ncszfcg.gov.cn/'
        data = response.body

        soup = BeautifulSoup(data)


        list_box = soup.find_all("ul", class_='listbox')

        a_list = list_box[0].find_all('a')

        yesterday_str = '2018-03-16'


        for a in a_list:

            #每天爬取前一天数据，对日期做一个限色
            date_web = a.find_next("div",class_='date').string

            item = BrgovscrapyItem()

            if date_web == yesterday_str:

                URL = dome_url +a['href']

                page = urllib2.urlopen(URL)

                d_soup = BeautifulSoup(page)

                qd_tables = d_soup.find_all("table", class_="MsoNormalTable")

                if len(qd_tables)>=2:
                    qd_table = qd_tables[1]
                elif len(qd_tables)==1:
                    qd_table = qd_tables[0]
                else:
                    continue

                key = jieba.analyse.extract_tags(qd_table.getText(), topK=50, withFlag=False, allowPOS=('n', 'vn', 'v', 'nbr'))

                keywords = ''

                for k in key:
                    keywords = keywords + k + ' '


                item['keywords'] = key
                item['url'] = URL
                item['title'] = yesterday_str
                yield item



