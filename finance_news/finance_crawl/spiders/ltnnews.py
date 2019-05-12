# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from finance_crawl.items import FinanceCrawlItem
class LtnnewsSpider(scrapy.Spider):
    name = 'ltnnews'
    allowed_domains = ['news.ltn.com.tw']
    start_urls = ['http://news.ltn.com.tw/list/breakingnews/business']
    page_num = 1
    def parse(self, response):
        if response.status == 200:
            source = BeautifulSoup(response.text, 'lxml')
            news_a_tag = source.select('ul.list li > a.tit')
            for tag in news_a_tag:
                meta = {}
                meta['link'] = 'http:' + tag.get('href')
                meta['title'] = tag.get('data-desc')[4:]
                print(meta)
                yield scrapy.Request(meta['link'], callback = self.parse_product, meta=meta)
            self.page_num += 1
            print('http://news.ltn.com.tw/list/breakingnews/business/'+str(self.page_num))
            yield scrapy.Request('http://news.ltn.com.tw/list/breakingnews/business/'+str(self.page_num), callback = self.parse)
        else:
            print('done')
    def parse_product(self, response):
        item = FinanceCrawlItem()
        title = response.meta['title']
        link = response.meta['link']
        source = BeautifulSoup(response.text, 'lxml')
        time = source.select_one('span.time').text
        texts = source.select('div.text p')[:-4]
        text = ''
        for t in texts:
            text = text + t.text 
        item['time'] = time
        item['title'] = title
        item['link'] = link
        item['text'] = text
        return item
