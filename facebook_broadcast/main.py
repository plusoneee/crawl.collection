from dotenv import load_dotenv
load_dotenv()
import os
from Module.FBStreaming import StreamingCrawl
import time 

if __name__ == "__main__": 
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    url = 'https://www.facebook.com/dryangmark/videos/419630028857659/'
    fb = StreamingCrawl(email, password, url)
    cookies = fb.get_cookies()
    # cookies = pickle.load(open("cookies.pkl", "rb"))
    for i in range(1):
        time.sleep(5)
        print(fb.parse(cookies))