# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import random
import time

from scrapy import signals
from scrapy.utils.response import response_status_message
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from AutoComments.mymiddlewares.spiderproxy import IpProxy

p = IpProxy()


class Process_Proxies(RetryMiddleware):
    logger = logging.getLogger(__name__)

    def resetip(self, ip):
        global p
        print('重置代理')
        p.remove_ip(ip)
        return p.get_ip()

    def process_response(self, request, response, spider):
        # if request.meta.get('dont_retry',False):
        #     return response
        # if response.status in self.retry_http_codes:
        if response.status != 200:
            print('状态码 %s 异常' % response.status)
            max_retry_times = len(IpProxy.ips)
            reason = response_status_message(response.status)
            ip = request.meta['proxy']
            request.meta['proxy'] =self.resetip(ip)
            request.meta['max_retry_times'] = max_retry_times
            print('ip %s 替换为: %s 最大重连次数为: %s'%(ip, request.meta['proxy'], max_retry_times))
            time.sleep(random.randint(3, 5))
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        global p
        # if isinstance(exception, self.EXCEPTIONS_TO_RETRY) and not request.meta.get('dont_retry', False):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
            ip = request.meta['proxy']
            max_retry_times = len(IpProxy.ips)
            request.meta['proxy'] =self.resetip(ip)
            request.meta['max_retry_times'] = max_retry_times
            print('ip %s 替换为: %s 最大重连次数为: %s'%(ip, request.meta['proxy'], max_retry_times))
            request.headers.setdefault('User-Agent', p.get_usragent())
            time.sleep(random.randint(3, 5))
            self.logger.warning('连接异常,进行重试......')
            return self._retry(request, exception, spider)







class AutocommentsSpiderMiddleware(object):
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


class AutocommentsDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):

        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        global p
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            print('<<<<<<<<<<<<<<<<返回异常，正在使用代理重试 %s>>>>>>>>>>>>>>>>'%response.status)
            request.meta['proxy'] = p.get_ip()
            request.headers.setdefault('User-Agent', p.get_usragent())
            return request
        return response


    def process_exception(self, request, exception, spider):
        global p
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        print('<<<<<<<<<<<<<<<<请求异常，正在使用代理重试>>>>>>>>>>>>>>>>')
        request.meta['proxy'] = p.get_ip()
        request.headers.setdefault('User-Agent', p.get_usragent())

        return request


    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
