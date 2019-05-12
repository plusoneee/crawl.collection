# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from finance_crawl.items import FinanceCrawlItem

class ApplydaliySpider(scrapy.Spider):
    name = 'appledaliy'
    allowed_domains = ['tw.finance.appledaily.com']
    start_urls = ['https://tw.finance.appledaily.com/realtime/']
    page_num = 1
    def parse(self, response):
        if response.status == 200:
            source = BeautifulSoup(response.text, 'lxml')
            all_tags = source.select('li.rtddt a')
            for tag in all_tags:
                link = tag.get('href')
                yield scrapy.Request('https://tw.finance.appledaily.com'+link, callback = self.parse_product)
                
        self.page_num += 1
        if self.page_num < 20:
            yield scrapy.Request('https://tw.finance.appledaily.com/realtime/'+str(self.page_num), callback = self.parse)
    def parse_product(self, response):
        source = BeautifulSoup(response.text, 'lxml')
        item = FinanceCrawlItem()
        title = source.select_one('h1').text
        time = source.select_one('div.ndArticle_creat').text.replace('出版時間：','')
        texts = source.select('div.ndArticle_margin p')
        text = texts[0].text.replace('\xa0','').replace('\t','')
        if text =='':
            text = texts[1].text.replace('\xa0','').replace('\t','')
        item['time'] = time
        item['title'] = title
        item['link'] = response.url
        item['text'] = text
        return item
        
