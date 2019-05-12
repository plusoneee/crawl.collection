# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from finance_crawl.items import FinanceCrawlItem
class EttodaySpider(scrapy.Spider):
    name = 'ettoday'
    allowed_domains = ['www.ettoday.net']
    page_index = 0
    def start_requests(self):
        keywords_list = [
                'https://www.ettoday.net/news_search/doSearch.php?keywords=上櫃',
                'https://www.ettoday.net/news_search/doSearch.php?keywords=上市',
                'https://www.ettoday.net/news_search/doSearch.php?keywords=ipo']
        for keyword in keywords_list:
            for page in range(1,20):
                link = keyword + '&idx=1&page='+str(page)
                print(link)
                yield scrapy.Request(link, callback=self.parse)
    
    def parse(self, response):     
        source = BeautifulSoup(response.text, 'lxml')
        news_a_tag = source.select('div.result_archive div.clearfix h2 a')
        next_page_list = []
        for tag in news_a_tag:
            meta = {}
            meta['link'] = tag.get('href')
            meta['title'] = tag.text
            yield scrapy.Request(meta['link'], callback = self.parse_product, meta=meta)

    def parse_product(self, response):
        item = FinanceCrawlItem()
        title = response.meta['title']
        link = response.meta['link']
        source = BeautifulSoup(response.text, 'lxml')
        time = source.select_one('time.date')
        if time:
            time = time.get('datetime')
        else:
            time = source.select_one('time.news-time').get('datetime')

        texts = source.select('div.story p')
        text = ''
        for t in texts:
            text = text + t.text
        item['time'] = time[:-9]
        item['title'] = title.replace('\u3000','')
        item['link'] = link
        item['text'] = text
        return item
        