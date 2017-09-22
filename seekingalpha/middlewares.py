# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.conf import settings
from spiders.log import *
import random

class SeekingalphaSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class SeekingalphaDownloaderMiddleware(object):
    def __init__(self):
        self.proxy_list = settings['PROXY_LIST']
        self.user_agent_list = settings['USER_AGENTS_LIST']

    def process_request(self, request, spider):
        if not self.is_retry(request):
            return
        if getattr(spider, 'use_proxy', False) and 'proxy' not in request.meta:
            self.set_random_proxy(request)
            spider.log(
                u'IP-Proxy: {} {}'.format(request.meta.get('proxy'), request)
            )
        if getattr(spider, 'use_agent', False):
            self.set_random_agent(request)
            spider.log(
                u'User-Agent: {} {}'.format(request.headers.get('User-Agent'), request),
                level=log.DEBUG
            )

    def set_random_proxy(self, request):
        proxy_address = random.choice(self.proxy_list)
        if proxy_address:
            request.meta['proxy'] = proxy_address
        else:
            warn('[ERROR] proxy not loaded!')

    def set_random_agent(self, request):
        user_agent = random.choice(self.user_agent_list)
        if user_agent:
            request.headers['User-Agent'] = user_agent
        else:
            warn('[ERROR] User agent not loaded!')

    def is_retry(self, request):
        request_times = request.meta.get('retry_times', 0)
        info('[RETRY TIMES]: %d' % request_times)
        return True if request_times > 0 else False