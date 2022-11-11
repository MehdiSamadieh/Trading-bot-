
import time
import datetime
import winsound
import json     # For parsing data
import requests # For pulling data
import time     # For dealing with time
from polygon import RESTClient


link="http://app.quotemedia.com/data/getHeadlines.json?topics=business,national&perTopic=2&src=upi&webmasterId=104285"
response = requests.get(link)

link1="http://app.quotemedia.com/data/getHeadlines.xml?topics=msft&perTopic=2&webmasterId=YmQ5ZmQxYjgtOTNhZC00MTFiLTlmZGYtMzNmY2E5NGE1YTcx"
response1 = requests.get(link)
print(response1.text)
