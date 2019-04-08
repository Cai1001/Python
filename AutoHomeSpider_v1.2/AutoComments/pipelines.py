# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from AutoComments.spiders.pages_crawled import CrawledUrls

class AutocommentsPipeline(object):
	'''
        管道文件可以写多个，需要在 setting.py 文件中定义，数值越小，优先级越高
        类初始化只有一次，第一次初始化后, __init__方法会失效。
    '''

	def __init__(self):
		pass


	def process_item(self, item, spider):
		return item

	def close_spider(self, spider):
		pass