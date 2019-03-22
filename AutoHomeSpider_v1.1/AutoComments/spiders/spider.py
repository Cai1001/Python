# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request,Response
from AutoComments.items import AutocommentsItem
import requests
from lxml import etree
import re

from AutoComments.mymiddlewares.spiderproxy import IpProxy
p = IpProxy()
count = 0
class Autohome2Spider(scrapy.Spider):
	name = "autohome_spider"
	prefix = 'http://wenda.autohome.com.cn'
	start_urls = ['http://wenda.autohome.com.cn/topic/list-1-0-0-0-0-1',
	              'http://wenda.autohome.com.cn/topic/list-2-0-0-0-0-1',
	              'http://wenda.autohome.com.cn/topic/list-3-0-0-0-0-1',
	              'http://wenda.autohome.com.cn/topic/list-4-0-0-0-0-1']

	# def start_requests(self):
	# 	global p
	# 	proxies = {'http': p.get_ip()}
	# 	user_agent = {'User-agent': p.get_usragent()}
	# 	# html = requests.get(url=self.start_urls[0], proxies=proxies, headers=user_agent)
	# 	html = requests.get(self.start_urls[0])
	# 	selector = etree.HTML(html.text)
	#
	# 	print('****************parse request url: %s status_code : %s ****************'%(html.url, str(html.status_code)))
	# 	urls = []
	# 	nodes = selector.xpath('//div[@class="classify"][2]/div/a/@href')
	# 	for node in nodes:
	# 		req = self.prefix + node
	# 		print('二级标签首页: %s'%req)
	# 		urls.append(req)
	# 	print("num of l2 label: %d" %len(urls))
	# 	for url in urls:
	# 		yield scrapy.Request(url=url, callback=self.parse)
	# 	# 爬取所有的标签网页
	# # def parse(self, response):
	# # 	selector = Selector(response)
	# # 	print('****************parse request url: %s status_code : %s ****************'%(selector.response.url, str(selector.response.status)))
	# # 	reqs = []
	# # 	nodes = selector.xpath('//div[@class="classify"][2]/div/a')
	# # 	for node in nodes:
	# # 		req = self.prefix + node.xpath('./@href').extract()[0]
	# # 		print('二级标签首页: %s'%req)
	# # 		reqs.append(req)
	# # 	print("num of l2 label: %d" %len(reqs))
	# # 	for req in reqs:
	# # 		yield Request(url=req, callback=self.gen_all_req
	'''
	一级标签下所有的问句
	一级标签一级二级标签下所有问句
	一级二级三级标签下所有问句
	'''


	def parse(self, response):
		selector = Selector(response)
		print('****************parse request url: %s status_code : %s ****************'%(selector.response.url, str(selector.response.status)))
		l2_urls = selector.xpath('//div[@class="classify"][2]//div/a')
		if l2_urls:
			for l2_url in l2_urls:
				url = self.prefix + l2_url.xpath('./@href').extract()[0]
				print('****************请求 二级 标签首页: %s****************' %url)
				yield Request(url=url, callback=self.gen_all_reqs)
		else:
			print('****************解析 一级 标签首页: %s****************' % selector.response.url)
			yield Request(url=selector.response.url, callback=self.parse_detail)


	def gen_all_reqs(self, response):
		selector = Selector(response)
		print('****************gen_all_reqs: request url: %s status_code : %s ****************'%(selector.response.url, str(selector.response.status)))
		l3_urls = selector.xpath('//div[@class="classify"][3]//div/a')
		if l3_urls:
			for l3_url in l3_urls:
				url = self.prefix + l3_url.xpath('./@href').extract()[0]
				print('****************解析 三级 标签首页: %s****************' %url)
				yield Request(url=url, callback=self.parse_detail)
		else:
			print('****************解析 二级 标签首页: %s****************' % selector.response.url)
			yield Request(url=selector.response.url, callback=self.parse_detail)


	def parse_detail(self, response):
		global count
		item = AutocommentsItem()
		selector = Selector(response)
		print('****************parse_detail request url: %s status_code : %s ****************'%(selector.response.url, str(selector.response.status)))

		print('*********************开始抓取第 %d 页 %s 信息, status : %s'%(count, selector.response.request, selector.response.status))

		l1_label = selector.xpath('/html/body/div[3]/div/div[1]/div[1]/div[2]/div/a/span/em[@class="current"]/text()').extract()
		if l1_label:
			item['l1label'] = l1_label[0]
		else:
			item['l1label'] = ''

		l2_label = selector.xpath('/html/body/div[3]/div/div[1]/div[1]/div[3]/div/a/span/em[@class="current"]/text()').extract()
		if l2_label:
			item['l2label'] = l2_label[0]
		else:
			item['l2label'] = ''

		l3_label = selector.xpath('/html/body/div[3]/div/div[1]/div[1]/div[4]/div/a/span/em[@class="current"]/text()').extract()
		if l3_label:
			item['l3label'] = l3_label[0]
		else:
			item['l3label'] = ''

		questionlist = selector.xpath('/html/body/div[3]/div/div[1]/div[2]/ul/li/h4/a/text()').extract()
		print("****************完成抓取 %d 页信息 %s  | L1: %s | L2: %s | L3:%s****************" %(count, selector.response.url,item['l1label'],item['l2label'], item['l3label']))
		count += 1
		if questionlist:
			print(len(questionlist))
			for question in questionlist:
				item['question'] = question
				yield item
		nextlink = selector.xpath('//a[@class="athm-page__next"]/@href').extract()
		if nextlink:
			nextlink = self.prefix + nextlink[0]
			print('****************开始解析下一页 %s 信息****************'% nextlink)
			yield Request(url=nextlink, callback=self.parse_detail)




