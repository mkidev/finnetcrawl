# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class FinnetcrawlPipeline(object):
    def process_item(self, item, spider):
        return item


class CalculateYieldReturnPipeline(object):
    yieldReturn = {"yr":1,"yr2":2,"yr4":4}

    def getFloat(self, value):
        return float(value.replace(",","."))
        

    def process_item(self, item, spider):
        for k,v in self.yieldReturn.items():
            item[k] =(self.getFloat(item['ask'])*v)/self.getFloat(item['ratio'])+self.getFloat(item['strike'])
        return item


class DropFalseValuesPipeline(object):
    def getFloat(self, value):
        return float(value.replace(",","."))
    def process_item(self, item, spider):
        if(self.getFloat(item['bid'])==0 or self.getFloat(item['ask'])==0):
            raise DropItem("Wrong Bid/Ask in %s" % item)   
        else:
            return item 