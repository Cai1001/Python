#!/usr/bin/env python
# coding=utf-8
import scrapy
from AutoComments.items import AutocommentsItem
from scrapy.selector import Selector
from scrapy.http import Request
import re
from AutoComments.spiders.pages_crawled import CrawledUrls
count = 0


class AutoComment1(scrapy.Spider):
	name = "AutoCommentSpider1"
	prefix = 'https://wenda.autohome.com.cn'
	start_urls = ['https://wenda.autohome.com.cn/topic/list-2-28-0-0-0-1',
	              'https://wenda.autohome.com.cn/topic/list-2-32-0-0-0-1',
	              'https://wenda.autohome.com.cn/topic/list-1-11-0-0-0-1']
	# def start_requests(self):
	# 	url = 'https://wenda.autohome.com.cn/topic/list-1-6-0-0-0-1'
	# 	urls = [re.sub('\d$', i, url) for i in range(334)]
	# 	return urls

	def parse(self, response):
		global count
		item = AutocommentsItem()
		selector = Selector(response)
		print('****************parse_detail request url: %s status_code : %s ****************' % (
		selector.response.url, str(selector.response.status)))

		print('*********************开始抓取第 %d 页 %s 信息, status : %s' % (
		count, selector.response.request, selector.response.status))

		l1_label = selector.xpath(
			'/html/body/div[3]/div/div[1]/div[1]/div[2]/div/a/span/em[@class="current"]/text()').extract()
		if l1_label:
			item['l1label'] = l1_label[0]
		else:
			item['l1label'] = ''

		l2_label = selector.xpath(
			'/html/body/div[3]/div/div[1]/div[1]/div[3]/div/a/span/em[@class="current"]/text()').extract()
		if l2_label:
			item['l2label'] = l2_label[0]
		else:
			item['l2label'] = ''

		l3_label = selector.xpath(
			'/html/body/div[3]/div/div[1]/div[1]/div[4]/div/a/span/em[@class="current"]/text()').extract()
		if l3_label:
			item['l3label'] = l3_label[0]
		else:
			item['l3label'] = ''

		questionlist = selector.xpath('/html/body/div[3]/div/div[1]/div[2]/ul/li/h4/a/text()').extract()
		print("****************完成抓取 %d 页信息 %s  | L1: %s | L2: %s | L3:%s****************" % (
		count, selector.response.url, item['l1label'], item['l2label'], item['l3label']))
		count += 1
		if questionlist:
			print(len(questionlist))
			for question in questionlist:
				item['question'] = question
				yield item
		nextlink = selector.xpath('//a[@class="athm-page__next"]/@href').extract()
		if nextlink:
			nextlink = self.prefix + nextlink[0]
			print('****************开始解析下一页 %s 信息****************' % nextlink)
			yield Request(url=nextlink, callback=self.parse)


