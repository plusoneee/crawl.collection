# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from finance_crawl.items import FinanceCrawlItem
import json
import requests
class TvbsSpider(scrapy.Spider):
    name = 'tvbs'
    allowed_domains = ['news.tvbs.com.tw']
    # start_urls = ['https://news.tvbs.com.tw/news/LoadMoreOverview?limit=30&offset=1&cateid=12&cate=tech&newsid=1012090&newslist=%27%27']
    start_urls = ['https://news.tvbs.com.tw/tech']
    def parse(self, response):
       
        # first time get link
        source = BeautifulSoup(response.text, 'lxml')
        news_a_tag = source.select('div.content_center_list_box ul#block_pc li a')
        links = []
        for link in news_a_tag:
            link = link.get('href').split('/')[-1]
            links.append(link)   
        #  get either link from last ID
        for idx in range(20): 
            print(links[-1])
            api = 'https://news.tvbs.com.tw/news/LoadMoreOverview?limit=30&offset=1&cateid=12&cate=tech&newsid='+ links[-1] +'&newslist=%27%27'
            r = requests.get(api)
            news_new_links = json.loads(r.text)['news_id_list'][3:].replace("'",'').split(',')
            links = links + news_new_links
        
        for news_id in links:
            link = 'https://news.tvbs.com.tw/tech/' + news_id
            yield scrapy.Request(link, callback = self.parse_product)

    def parse_product(self, response):
        item = FinanceCrawlItem()
        # print(response.url)
        source = BeautifulSoup(response.text, 'lxml')
        title = source.select_one('h1.margin_b20').text
        time = source.select_one('div.icon_time').text
        text = source.select_one('div#news_detail_div').text.replace('\n','').replace('\t\t\t\t\t   \t\t','')
        item['time'] = time
        item['title'] = title
        item['link'] = response.url
        item['text'] = text
        return item