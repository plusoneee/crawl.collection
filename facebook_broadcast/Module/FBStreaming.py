from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
import time 
from bs4 import BeautifulSoup

class StreamingCrawl():
    def __init__(self, email, password, broadcast_url):
        self.email = email
        self.password = password
        self.driver = webdriver.Firefox()
        self.data = {}
        self.broadcast_url = broadcast_url

    def get_cookies(self):
        driver = self.driver
        driver.get("https://www.facebook.com/") 
        elem = driver.find_element_by_name("email") 
        elem.send_keys(self.email) 
        elem = driver.find_element_by_name('pass')
        elem.send_keys(self.password)
        driver.find_element_by_id('loginbutton').click()
        cookies = driver.get_cookies()
        pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
        return cookies

    def parse(self, cookies):
        self.data = {}
        self.driver.get(self.broadcast_url)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        time.sleep(5)
        source = self.driver.page_source
        source = BeautifulSoup(source,'lxml')
        self.data['all_comments'] = []
        self.data['broadcast_master_name'] = source.select_one('a.profileLink').text
        self.data['title'] = source.select_one('title').text
        comments_span = source.select('div.clearfix')
        for comment in comments_span:
            each_comment = {}
            if comment:
                img = comment.select_one('img.img')
                if img: 
                    img = img.get('src').replace('&amp;','&')
                    alt = comment.select_one('img.img').get('alt')
                    UFICommentActorAndBody = comment.select('span.UFICommentActorAndBody')
                    if UFICommentActorAndBody:
                        each_comment['name'] = UFICommentActorAndBody[0].select_one('a.UFICommentActorName').text
                        each_comment['comment'] = UFICommentActorAndBody[0].select_one('span.UFICommentBody').text
                        each_comment['img_url'] = img
                        self.data['all_comments'].append(each_comment)
        return self.data


# if __name__ == "__main__": 
#     email = os.getenv("EMAIL")
#     password = os.getenv("PASSWORD")
#     url = 'https://www.facebook.com/LoveVeryTJ/videos/417797382351163/'
#     fb = StreamingCrawl(email, password, url)
#     cookies = fb.get_cookies()
#     # cookies = pickle.load(open("cookies.pkl", "rb"))
#     for i in range(10):
#         print(fb.parse(cookies))