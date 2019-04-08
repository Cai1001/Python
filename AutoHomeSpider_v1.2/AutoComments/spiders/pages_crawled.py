#!/usr/bin/env python
# coding=utf-8
from AutoComments.settings import URLS_CRAWLED


def load_crawled_urls():
	temp = []
	path = URLS_CRAWLED
	try:
		with open(path, 'r') as fin:
			for line in fin.readlines():
				line = line.replace('\n', '')
				temp.append(line)
			print("===========载入已访问的urls：{0} 个=============".format(len(temp)))
		return temp
	except IOError:
		print("缺少已经访问的urls 文件{0}".format(path))
		return []


class CrawledUrls:

	urls = load_crawled_urls()

	@staticmethod
	def save_crawled_urls():
		path = URLS_CRAWLED
		try:
			with open(path, 'a', encoding='utf-8') as fw:
				for url in CrawledUrls.urls:
					fw.writelines(url+'\n')
				print("===========保存已访问的urls：{0} 个=============".format(len(CrawledUrls.urls)))
		except IOError:
			raise IOError("打开文件失败" + URLS_CRAWLED)

	@staticmethod
	def save_crawled_url(url):
		path = URLS_CRAWLED
		try:
			with open(path, 'a', encoding='utf-8') as fw:
				fw.writelines(url+'\n')
		except IOError:
			raise IOError("打开文件失败" + URLS_CRAWLED)

	@staticmethod
	def add_url(url):
		if url not in CrawledUrls.urls:
			CrawledUrls.urls.append(url)

	@staticmethod
	def is_url_visited(url):
		return url in CrawledUrls.urls
