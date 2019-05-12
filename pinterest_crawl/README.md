
### Dependencies
* Python 3
* [chromedriver](http://chromedriver.chromium.org)
### Python Requirements
```
python-dotenv
selenium
BeautifulSoup
requests
json
re
csv
```

### Configure Settings
* Edit the file `.env.example`, and save as `.env`.
```
cp .env.example .env
vim .env
```
* For example:
```
HASHTAGS_DEFUALT = "rawfood, fruit, banana, apple, pineapple"
BROWSER_PATH =  '/txtmn/pinterest_crawl/chromedriver'
CSV_FILE_NAME = 'my_fruit.csv'
PINTEREST_TOPIC = 'fruit'
IMAGE_NUMBER = 100
```

### How to Run
```
python app.py
```

