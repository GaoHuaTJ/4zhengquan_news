# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhengquanNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #某一天的新闻汇总标题，eg:12月12日四大财经报头版头条内容精华摘要
    day_sum_title=scrapy.Field()

    #某一天的新闻标题日期，eg:(2019-12-12 07:27:47)
    time_day_sum_title=scrapy.Field()




    pass
