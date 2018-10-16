# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BrgovscrapyItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    keywords = scrapy.Field()

    class_stock = scrapy.Field()
    type_stock = scrapy.Field()
    scope_stock = scrapy.Field()

