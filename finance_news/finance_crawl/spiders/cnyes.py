# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from finance_crawl.items import FinanceCrawlItem
import json
import requests
from datetime import datetime
import re
class SetnSpider(scrapy.Spider):
    name = 'cnyes'
    allowed_domains = ['news.cnyes.com/']
    with open('finance_crawl/spiders/company_of_Application.json') as f:
        data = f.read()
        company_of_Application = json.loads(data.replace("'",'"'))

    def start_requests(self):
        for item in  self.company_of_Application:
            last_page = self.get_last_page(startUrl='https://news.cnyes.com/api/v3/search?page=1&q='+item['company'])
            for page in range(1, last_page+1): 
            # url = 'https://www.setn.com/search.aspx?q='+item['company']
                date_of_application = str(item['date_of_application'])
                day = date_of_application
                meta = {
                    'company':item['company'],
                    'date': day
                }
                yield scrapy.Request('https://news.cnyes.com/api/v3/search?page='+str(page)+'&q='+ item['company'], self.parse, meta=meta)

    def parse(self, response):
        all_item = []
        print('-----------------------------------')
        print(response.url)
        print('-----------------------------------')
        # item = FinanceCrawlItem()
        json_datas = json.loads(response.text)
        datas = json_datas['items']['data']
        pattern = re.compile("<mark>.*</mark>")
        for data in datas:
            item = FinanceCrawlItem()
            time_num = int(data['publishAt'])
            date = datetime.fromtimestamp(time_num).strftime("%Y%m%d")
            content = pattern.search(data['content'])
            content = content.group()
            if content:
                content = content.replace('<mark>', '').replace('</mark>', '')
                item['company'] = content
            else:
                item['company'] = response.meta['company']
            item['date'] = date
            item['title'] = data['title']
            item['link'] = 'https://news.cnyes.com/news/id/' + str(data['newsId'])
            
            item['due_date'] = response.meta['date']
            all_item.append(item)
        return all_item
    
    def get_last_page(sefl, startUrl):
        r = requests.get(startUrl)
        json_datas = json.loads(r.text)
        last_page = json_datas['items']['last_page']
        return last_page
    