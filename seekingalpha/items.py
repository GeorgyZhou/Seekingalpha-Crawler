# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SAItem(scrapy.Item):
    url = scrapy.Field()
    article_id = scrapy.Field()
    article_date = scrapy.Field()
    article_title = scrapy.Field()
    article_text = scrapy.Field()
    article_raw = scrapy.Field()
    # article_comments = scrapy.Field()
    # article_commenters = scrapy.Field()
    author = scrapy.Field()
    author_id = scrapy.Field()
    stock_name = scrapy.Field()
    stock_id = scrapy.Field()
    disclosure = scrapy.Field()
