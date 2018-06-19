import scrapy
from finnetcrawl.items import FinnetcrawlItem

class QuotesSpider(scrapy.Spider):
    name = "options"

    def start_requests(self):
        urls = [
            'http://zertifikat.finanzen.net/optionsscheine/suche?listingbit_inlistofint=1,3,4,5,6&parentderivativetypeid_equals=13&firstunderlyingid_inlistofint=301&maturitydate_lowerbounddate=30.09.2018&derivativesubtypeid_inlistofint=1&issuercompanyid_inlistofint=2,3,4,5,8,9,11,12,14,16,19,22,24,30,52,100,101,102,4338,7190&orderby=firststrikeabsolute:asc&dynamickeys=omega,volatility,spreadhomogenous'        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parseOption(self, response):
        item = response.meta['item']
        item['ratio'] = response.css('.main_right > div')[0].css('td::text')[14].extract()
        yield item
        
    def parse(self, response):
        for row in response.css('#ctl00_MainContentPlaceHolder_DerivativeSearchResultTable_Container > div.content > div > table> tbody:nth-child(3) > tr'):
            item = FinnetcrawlItem()
            try: 
                item['emittent'] = row.css('tr > td:nth-child(1) > div')[0].xpath('@title')[0].extract()
                item['wkn'] = row.css('tr > td:nth-child(2) a::text')[0].extract()
                item['wkn_link'] = "http://zertifikat.finanzen.net"+row.css('tr > td:nth-child(2) a')[0].xpath("@href")[0].extract()
                item['bid'] = row.css('tr > td:nth-child(3) span::text')[0].extract()
                item['ask'] = row.css('tr > td:nth-child(4) span::text')[0].extract()
                item['due'] = row.css('tr > td:nth-child(5)::text')[0].extract()
                item['strike'] = row.css('tr > td:nth-child(6)::text')[0].extract() 
                yield response.follow(row.css('tr > td:nth-child(2) a')[0], callback=self.parseOption,meta={'item':item})                     
            except Exception as e:
                print(e)
#pagination
        current_page = int(response.css(".paging span::text")[0].extract())
        for page in response.css(".paging a"):
            try: 
                if int(page.css("::text")[0].extract()) > current_page:
                    if current_page > 30:
                        page = None
                    if page is not None:
                        yield response.follow(page, callback=self.parse)
            except:
                pass
            