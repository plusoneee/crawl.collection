# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from finance_crawl.items import FinanceCrawlItem

class NownewsSpider(scrapy.Spider):
    page_num = 1
    name = 'nownews'
    allowed_domains = ['www.nownews.com']
    start_urls = ['https://www.nownews.com/cat/finance/']
    def parse(self, response):
        if response.status == 200:
            source = BeautifulSoup(response.text, 'lxml')
            news_a_tag = source.select('h3.entry-title > a')
            for news_info in news_a_tag:
                meta = {'title': news_info.get('title'),
                        'link': news_info.get('href')}
                yield scrapy.Request(meta['link'], callback = self.parse_product, meta=meta)
            self.page_num += 1
            print('https://www.nownews.com/cat/finance/page/'+str(self.page_num))
            yield scrapy.Request('https://www.nownews.com/cat/finance/page/'+str(self.page_num), callback=self.parse)
        else:
            print('done!')

    def parse_product(self, response):
        item = FinanceCrawlItem()
        title = response.meta['title']
        link = response.meta['link']
        source = BeautifulSoup(response.text, 'lxml')
        time = source.select_one('time.entry-date').text
        all_text = source.select('div.td-post-content p')
        text =''
        for t in all_text[1:]:
            if 'figure' not in t:
                text = text+t.text
        item['title'] = title
        item['link'] = link
        item['time'] = time
        item['text'] = text
        return item