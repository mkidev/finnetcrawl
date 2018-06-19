# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import numpy as np


def serializeNum(val):
    val = val.replace(",",".")
    return float(val)

class FinnetcrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    wkn = scrapy.Field()
    wkn_link = scrapy.Field()
    emittent = scrapy.Field()
    bid = scrapy.Field(serializer=serializeNum)
    ask = scrapy.Field(serializer=serializeNum)
    due = scrapy.Field()
    strike = scrapy.Field(serializer=serializeNum)
    ratio = scrapy.Field(serializer=serializeNum)
    yr = scrapy.Field()
    yr2 = scrapy.Field()
    yr4 = scrapy.Field()

