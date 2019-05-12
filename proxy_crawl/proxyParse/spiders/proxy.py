import lxml
from bs4 import BeautifulSoup
import scrapy
import json

class scrapyProxy(scrapy.Spider):
    name ='proxy'
    allowed_domains = ['www.us-proxy.org']
    url = 'https://httpbin.org/ip'
    start_urls = ['https://www.us-proxy.org/']
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        trs = soup.select("#proxylisttable tr")
        for tr in trs: 
            tds = tr.select("td")
            if len(tds) > 6:
                ip = tds[0].text
                port = tds[1].text
                anonymity = tds[4].text
                ifScheme = tds[6].text
                if ifScheme == 'yes': 
                    scheme = 'https'
                else: scheme = 'http'
                proxy = "%s://%s:%s"%(scheme, ip, port)
                if anonymity != 'anonymous': 
                    meta = {
                        'port': port,
                        'proxy': proxy,
                        'dont_retry': True,
                        'download_timeout': 3,
                        '_proxy_scheme': scheme,
                        '_proxy_ip': ip,
                        
                    }
                    yield scrapy.Request(self.url, callback=self.check_available, meta=meta, dont_filter=True)
                
    def check_available(self, response):
        proxy_ip = response.meta['_proxy_ip']
        if proxy_ip == json.loads(response.text)['origin']:
            yield {
                'scheme': response.meta['_proxy_scheme'],
                'proxy': response.meta['proxy'],
                'port': response.meta['port']
            }
    


    
