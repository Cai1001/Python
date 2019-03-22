# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class AutocommentsPipeline(object):
    '''
        管道文件可以写多个，需要在 setting.py 文件中定义，数值越小，优先级越高
        类初始化只有一次，第一次初始化后, __init__方法会失效。
    '''
    def __init__(self):
        self.f = open("./data/AutoQA.json", 'wb')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False)
        self.f.write(content.encode('utf-8'))
        return item

    def close_spider(self, spider):
        self.f.close()
