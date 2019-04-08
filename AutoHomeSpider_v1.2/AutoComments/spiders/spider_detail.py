#!/usr/bin/env python
# coding=utf-8
import scrapy
from AutoComments.items import AutocommentsDetailItem
from scrapy.selector import Selector
from scrapy.http import Request
import re
from AutoComments.spiders.pages_crawled import CrawledUrls

count = 0


class AutocommentsDetailSpider(scrapy.Spider):
	name = "AutocommentsDetailSpider"
	start_urls = ['https://wenda.autohome.com.cn/topic/list-1-0-0-0-0-1',
	              'https://wenda.autohome.com.cn/topic/list-2-0-0-0-0-1',
	              'https://wenda.autohome.com.cn/topic/list-3-0-0-0-0-1',
	              'https://wenda.autohome.com.cn/topic/list-4-0-0-0-0-1' ]

	prefix = 'https://wenda.autohome.com.cn'

	def parse(self, response):
		selector = Selector(response)
		page = selector.xpath('//div[@class="athm-page__num"]/a[last()]/text()').extract()
		if page:
			page_num = int(page[0])
		for i in range(1, page_num + 1):
			req = re.sub('(\d+)$', str(i), selector.response.url)
			if CrawledUrls.is_url_visited(req):
				print("==================页面 {0} 已经被访问过，不再访问=================".format(req))
				continue
			else:
				print('==============Generate request: %s ================' % req)
				yield Request(url=req, callback=self.quest_detail)

	def quest_detail(self, response):
		selector = Selector(response)
		question_list = selector.xpath('//ul[@class="question-list"]/li')
		for question in question_list:
			question_url = question.xpath('./h4/a/@href').extract()
			if question_url:
				req = self.prefix + question_url[0]
				if CrawledUrls.is_url_visited(req):
					print("==================页面 {0} 已经被访问过，不再访问=================".format(req))
					continue
				else:
					print('===========开始请求解析url %s =============' % req)
					yield Request(url=req, callback=self.parse_detail)
			else:
				print('==========解析失败=========')

	def parse_detail(self, response):
		global count
		count += 1
		selector = Selector(response)

		print("****************开始抓取 %d 页信息 %s ****************" % (count, selector.response.url))

		item = AutocommentsDetailItem()
		# 问句
		question = selector.xpath('//h1[@class="card-title"]/text()').extract()
		item['question'] = ''
		if question:
			print('question {0}'.format(question[0]))
			item['question'] = question[0]

		# 问句detail
		question_detail = selector.xpath('//div[@class="content example"]/div/p/text()').extract()
		if question_detail:
			item['question_detail'] = question_detail[0]
		else:
			item['question_detail'] = ''

		# questioner
		questioner = selector.xpath('//span[@class="fn-left"]/a/text()').extract()
		item['questioner'] = ''
		if questioner:
			item['questioner'] = questioner[0]

		# labels
		labels = selector.xpath('//ul[@class="card-tag-list"]/li/a/text()').extract()
		item['labels'] = ''
		if labels:
			for label in labels:
				item['labels'] += label + "##"

		# publish_time
		publish_time = selector.xpath('//span[@class="fn-right"]/text()').extract()
		item['publish_time'] = ''
		if publish_time:
			item['publish_time'] = publish_time[0]

		# review_times
		review_times = selector.xpath(
			'//span[@class="card-record-left"]/p[@class="card-record-count"]/text()').extract()
		item['review_times'] = ''
		if review_times:
			item['review_times'] = review_times[0]

		# answer_times
		answer_times = selector.xpath(
			'//span[@class="card-record-right"]/p[@class="card-record-count"]/text()').extract()
		item['answer_times'] = ''
		if answer_times:
			item['answer_times'] = answer_times[0]

		# simiquestions
		simi_questions = selector.xpath('//div[@class="common-wrap recommend-list-wrap"]/ul/li/a/text()').extract()
		item['simi_questions'] = ''
		if simi_questions:
			for simi_question in simi_questions:
				item['simi_questions'] += simi_question + "##"

		# answers
		item['answers'] = ''
		answers = selector.xpath('//div[@class="card-reply-wrap"]')
		if answers:
			for answer in answers:
				ans = answer.xpath('./div[@class="issue-reply-content"]/div/div[@ahe-role="text"]/p/text()').extract()
				if ans:
					for i in ans:
						item['answers'] += i
					item['answers'] += "##"

		yield item
		if not CrawledUrls.is_url_visited(selector.response.url):
			CrawledUrls.add_url(selector.response.url)
			CrawledUrls.save_crawled_url(selector.response.url)


		print(CrawledUrls.urls)
		print("****************完成抓取 %d 页信息 %s ****************" % (count, selector.response.url))



