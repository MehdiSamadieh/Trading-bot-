
import time
import datetime
import winsound
import json     # For parsing data
import requests # For pulling data
import time     # For dealing with time
from polygon import RESTClient

stock=""
DAY = 86400

url2 = "https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers?tickers=" + stock + "&apiKey=90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"
response1 = requests.get(url2)
close = float(json.loads(response1.text)["tickers"][0]["min"]["c"])
print(response1)
print(close)
#while(1):
   #url = "https://api.benzinga.com/api/v2/news?token=12eeca59c8674f098b785c5e2cb5c7b4"
  # benzinga = requests.get(url)
from benzinga import news_data

# 3 days ago:
threeDaysAgo = str(datetime.datetime.fromtimestamp(time.time() - (3 * DAY)))[:10]

# today:
today = str(datetime.datetime.fromtimestamp(time.time()))[:10]
############
MULTIPLIER = "1"
TIMESPAN = "minute"  # Choices:      minute \ hours \ day \ week \ month \ quarter \ year
FROM = threeDaysAgo  # str(x)  # Template:     yyyy-mm-dd
TO = today  # str(x)  # Template:     yyyy-mm-dd
ADJUSTED = "true"  # Choices:      true \ false
SORT = "desc"  # Choices:      desc \ asc
LIMIT = "1"
APIKEY = "90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"
key_benzinga = "12eeca59c8674f098b785c5e2cb5c7b4"
link = "https://api.polygon.io/v2/aggs/ticker/" + "RECAF" + "/range/" + MULTIPLIER + "/" + TIMESPAN + "/" + FROM + "/" + TO + "?adjusted=" \
       + ADJUSTED + "&sort=" + SORT + "&limit=" + LIMIT + "&apiKey=" + APIKEY

# Conversion of the requested JSON Object to Dictionary:

response_close = requests.get(link)
print(response_close.text)
close = float(json.loads(response_close.text)["results"][0]["c"])
print("close",close)
url_trade = "https://api.polygon.io/v2/last/trade/" + "RECAF" + "?&apiKey=90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"
response = requests.get(url_trade)
print(response.text)
f = open("RRR.txt", "a")
f.write("stock-news:"+ "\n")
f.close()
