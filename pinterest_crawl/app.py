from pincrawler import CrawlPinterest
from dotenv import load_dotenv
import os 

load_dotenv()
hashtags_defualt = os.getenv("HASHTAGS_DEFUALT")
hashtags_defualt = hashtags_defualt.split(',')
browser_path = os.getenv("BROWSER_PATH")
file_name = os.getenv("CSV_FILE_NAME")
topic = os.getenv('PINTEREST_TOPIC')
img_number = os.getenv("IMAGE_NUMBER")
crawl = CrawlPinterest(hashtags_defualt = hashtags_defualt, \
                        browser_path = browser_path,  \
                        file_name = file_name, \
                        topic=topic, \
                        img_number = img_number
                        )
crawl.start_chrome_webdriver()
