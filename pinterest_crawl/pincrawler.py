from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import json
import re
from selenium.webdriver.chrome.options import Options
import csv

class CrawlPinterest():
    def __init__(self, hashtags_defualt, browser_path, file_name, topic, img_number):
        self.hashtags_defualt = hashtags_defualt
        self.pin_hrefs = set()
        self.browser_path = browser_path
        chrome_options = Options()
        chrome_options.add_argument("--window-size=0,0")
        self.browser = webdriver.Chrome(browser_path, chrome_options=chrome_options)
        self.file_name = file_name
        self.topic = topic 
        self.img_number = int(img_number)

    def start_chrome_webdriver(self):
        print('| * start chrome browser')
        print('| * topic: ', self.topic)
        self.browser.get('https://www.pinterest.com/search/pins/?q=' + self.topic)
        self.get_source_if_scroll()

    def get_source_if_scroll(self):
        time.sleep(2)
        source = BeautifulSoup(self.browser.page_source, 'lxml')
        all_a_tags = source.select('a')
        for a  in all_a_tags:
            if a.get('href'):
                if '/pin' in a.get('href'):
                    self.pin_hrefs.add(a.get('href'))
        self.browser.execute_script("window.scrollTo(1000, document.body.scrollHeight);")
        if len(self.pin_hrefs) < self.img_number:
            self.get_source_if_scroll()
        else:
            csv_datas = self.crawl_data_from_pin_hrefs()
            self.browser.close()
            self.write_data_to_csv_file(csv_datas)
            
    def crawl_data_from_pin_hrefs(self):
        print('| * crawl data from link')
        csv_datas = []
        for href in self.pin_hrefs:
            link = 'https://www.pinterest.com' + href
            try:
                r = requests.get(link)
                source = BeautifulSoup(r.text, 'lxml')
                obj = json.loads(source.select('script')[-3].text)
                meta = obj['initialPageInfo']['meta']
                hash_t = list(obj['resourceDataCache'][0]['data']['hashtags'])
                d = meta['description']
                hashtags = re.findall(r"#\w+", d)
                hashtags = hashtags + hash_t 
                twitter = meta['twitter:title'].lower()
                for tag in self.hashtags_defualt:
                    if tag in twitter:
                        hashtags.append('#'+ tag)
                if '#' in twitter:
                    hashtags.append(twitter.lower())
                csv_datas.append(
                    {
                        'id': href[5:-1],
                        'title': meta['og:title'],
                        'image_url':meta['og:image'],
                        'hashtags':hashtags
                    }
                )
                print('Get Pin :', meta['og:title'])
            except:
                print('err@', link)
        return csv_datas

    def write_data_to_csv_file(self, csv_datas):
        print('| * writing data to csv file')
        print('| * please dont\' close the program ')
        with open(self.file_name, 'w+') as f:
            print('| Writing data to csv file')
            fieldnames = ['id', 'title', 'image_url', 'hashtags']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_datas)
        print('| * save to ' + self.file_name)

