# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from finance_crawl.items import FinanceCrawlItem
import json
class SetnSpider(scrapy.Spider):
    name = 'setn'
    allowed_domains = ['www.setn.com']
    with open('finance_crawl/spiders/company_of_Application.json') as f:
        data = f.read()
        company_of_Application = json.loads(data.replace("'",'"'))

    def start_requests(self):
        for item in  self.company_of_Application:
            url = 'https://www.setn.com/search.aspx?q='+item['company']
            date_of_application = str(item['date_of_application'])
            day = date_of_application[0:4]+'/'+ date_of_application[4:6]+'/'+ date_of_application[6:]
            meta = {
                'company':item['company'],
                'date': day
            }
            yield scrapy.Request(url, self.parse, meta=meta)
        # yield scrapy.Request('https://www.setn.com/search.aspx?q=奇偶', self.parse)
    def parse(self, response):
        item = FinanceCrawlItem()
        due_date = response.meta['date']
        company = response.meta['company']
        source = BeautifulSoup(response.text, 'lxml')
        news_tags = source.select('div.newsimg-area-item-2 ')
        for i in news_tags:
            url = i.select_one('a.gt').get('href')
            title = i.select_one('div.newsimg-area-text-2 ').text
            news_date = i.select_one('div.label-area div.newsimg-date').text[:11]
            print(title, url, news_date, due_date)
            item['company'] = company
            item['date'] = news_date
            item['due_date'] = due_date
            item['title'] = title
            item['link'] = 'https://www.setn.com/'+url
            return item
            # if 
            # for tag in news_a_tag:
            #     meta = {}
            #     meta['link'] = 'https://www.setn.com' + tag.get('href')
            #     item['title'] = tag.text
            #     item['link'] = link
            #     item['time'] = time
            #     item['date'] = text
                # yield scrapy.Request(meta['link'], callback = self.parse_product, meta=meta)
            # self.page_num += 1

        #     if self.page_num != 25:
        #         yield scrapy.Request('https://www.setn.com/ViewAll.aspx?PageGroupID=2&p='+str(self.page_num), callback = self.parse)
        # else:
        #     print('done')
    # def parse_product(self, response):
    #     item = FinanceCrawlItem()
    #     title = response.meta['title']
    #     link = response.meta['link']
    #     source = BeautifulSoup(response.text, 'lxml')
    #     time = source.select_one('time.page-date').text
    #     texts = source.select('article div#Content1 p')
    #     text = ''
    #     for t in texts:
    #         text += t.text
    #     item['title'] = title
    #     item['link'] = link
    #     item['time'] = time
    #     item['text'] = text
    #     return item