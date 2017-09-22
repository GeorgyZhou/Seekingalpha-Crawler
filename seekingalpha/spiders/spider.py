from __future__ import absolute_import
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import FormRequest, Request
from ..items import SAItem
from .log import *
from .html2text import html2text
import re

class seekingalphaSpider(CrawlSpider):
    name = 'seekingalpha'
    allowed_domains = ['seekingalpha.com']
    start_urls = [
        'https://seekingalpha.com/stock-ideas/short-ideas?page=%d' % pn for pn in range(1, 250)
    ]
    rules = [
        Rule(sle(allow=('/article/\d+\-[0-9a-zA-Z\-]+')), callback='parse_rp', follow=True)
    ]
    aid_pattern = re.compile('https://seekingalpha\.com/article/(?P<aid>\d+)\-[0-9a-zA-Z\-]+')
    stock_pattern = re.compile('(?P<sn>[a-zA-Z0-9\s,.]+)\((?P<sid>[a-zA-Z0-9]+)\)')
    # use_proxy = True
    use_agent = True

    def parse_rp(self, response):
        cur_url = response.url
        info('[SA-INFO] Article Parsed: ' + cur_url)
        info('[' + cur_url + '] Response Status: ' + str(response.status))
        if not cur_url.startswith('https://seekingalpha.com/article/'):
            debug('[SA-DEBUG] Current URL is not article: ' + cur_url)
            return
        item = SAItem()
        # Article url
        item['url'] = cur_url
        # Article ID
        m = self.aid_pattern.match(cur_url)
        item['article_id'] = m.group('aid').encode('utf-8') if m else None
        # Article title
        title = response.xpath('//div[@id="a-hd"]/h1[@class="has-title-test"]/text()').extract_first()
        item['article_title'] = title.encode('utf-8') if title else None
        # Article date
        date = response.xpath('//div[@id="a-hd"]//time/@content').extract_first()
        item['article_date'] = date.encode('utf-8') if date else None
        # Stock name & stock id
        stock = response.xpath('//div[@id="a-hd"]//a/text()').extract_first()
        stock = stock if stock else ''
        m = self.stock_pattern.match(stock)
        item['stock_id'] = m.group('sid').encode('utf-8') if m else None
        item['stock_name'] = m.group('sn').encode('utf-8') if m else None
        # Author name & author id
        author_name = response.xpath('//div[@id="author-hd"]//a[@rel="author"]/span[@class="name"]/text()').extract_first()
        author_id = response.xpath('//*[@id="author-hd"]/div[2]/div[1]/div[1]/div/@data-id').extract_first()
        item['author'] = author_name.encode('utf-8') if author_name else None
        item['author_id'] = author_id.encode('utf-8') if author_id else None
        # Article raw & article text
        raw = response.xpath('//div[@id="a-cont"]').extract_first()
        item['article_raw'] = raw.encode('utf-8') if raw else None
        item['article_text'] = html2text(raw if raw else '').encode('utf-8')
        # Disclosure
        disclosure = response.xpath('//p[@id="a-disclosure"]/b/text()').extract_first()
        if not disclosure:
            disclosure = response.xpath('//div[@id="a-body"]/text()').extract_first()
        else:
            disclosure += response.xpath('//p[@id="a-disclosure"]/span/text()').extract_first()
            addition = response.xpath('//span[@id="top-business-disclosure"]/../text()').extract_first()
            disclosure += addition if addition else ''
        item['disclosure'] = disclosure.encode('utf-8') if disclosure else None
        yield item