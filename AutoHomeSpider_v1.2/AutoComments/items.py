# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutocommentsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    question = scrapy.Field()
    l1label = scrapy.Field()
    l2label = scrapy.Field()
    l3label = scrapy.Field()


class AutocommentsDetailItem(scrapy.Item):
    # 问句
    question = scrapy.Field()        #     //h1[@class="card-title"]/text()
    # 问句detail
    question_detail = scrapy.Field() #     //div[@class="content example"]/div/text()   不知道是否有
    # 发布者
    questioner = scrapy.Field()      #     //span[@class="fn-left"]/a/text()
    # l1 标签
    labels = scrapy.Field()          #     //ul[@class="card-tag-list"]/li/a/text()
    # 发布时间
    publish_time = scrapy.Field()    #      //span[@class="fn-right"]/text()
    # 浏览次数
    review_times = scrapy.Field()    #     //span[@class="card-record-left"]/p[@class="card-record-count"]/text()
    # 回答个数
    answer_times = scrapy.Field()    #     //span[@class="card-record-right"]/p[@class="card-record-count"]/text()
    # 推荐问句
    simi_questions = scrapy.Field()  #   //div[@class="common-wrap recommend-list-wrap"]/ul/li/a/text()
    # 答案1
    answers = scrapy.Field()         #    //div[@class="card-reply-wrap"]     ./div[@class="issue-reply-content"]/div/div[@ahe-role="text"]/p/text()







