# Modules:

import json     # For decoding data
import requests # For getting data
import time     # For dealing with time
import datetime

x = now = datetime.date.today()
print(str(x))

# Configs: ( .: Please refer to https://polygon.io/docs for more details :. )

STOCKSTICKER    = "APPL"            # Ticker of the stock
MULTIPLIER      = "1"
TIMESPAN        = "minute"          # Choices:      minute \ hours \ day \ week \ month \ quarter \ year
FROM            =str(x)  # Template:     yyyy-mm-dd
TO              = str(x)      # Template:     yyyy-mm-dd
ADJUSTED        = "true"            # Choices:      true \ false
SORT            = "desc"            # Choices:      desc \ asc
LIMIT           = "2"
APIKEY          = "90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"
first=str(int( time.time())*1000-60000)
second=str(int( time.time())*1000)
print(first)
print(second)

ag="https://api.polygon.io/v2/aggs/ticker/NIO/range/1/minute/"+first+"/"+second+"?adjusted=true&sort=asc&limit=120&apiKey="+"90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"

res = requests.get(ag)
print("res",res.text)


# Link Generator:

#link =  "https://api.polygon.io/v2/aggs/ticker/"+ STOCKSTICKER+ "/range/" + MULTIPLIER+ "/"+ TIMESPAN+ "/"+ FROM+ "/"+ TO+ "?adjusted="\
        #+ ADJUSTED  + "&sort=" + SORT+ "&limit="+ LIMIT+ "&apiKey="+ APIKEY

# Conversion of the requested JSON Object to Dictionary:

#response_close = requests.get( link)

#"https://api.polygon.io/v2/aggs/ticker/AAPL/prev?adjusted=true&apiKey=90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"

##################################33last trade
##close = float(json.loads(response_close.text)["results"][0]["c"])
#container=response_close.text
#print(response_close.text)
#print("close",close)
#open = float(json.loads(response_close.text)["results"][0]["o"])
#print("open",open)

url_trade = "https://api.polygon.io/v2/last/trade/" + "APPL" + "?&apiKey=90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"
response = requests.get(url_trade)
#trade = float(json.loads(response.text)["results"]["p"])
#print(trade)
print(response.text)

######td
linktd= "https://api.tdameritrade.com/v1/marketdata/CARV/quotes?apikey=GCURJZSYQBDSTFCHTCZNYMBOKRNJRZCW"

restd = requests.get(linktd)
close = float(json.loads(restd.text)["CARV"]["totalVolume"])

print("td",restd.text)



link = "https://api.polygon.io/v2/aggs/ticker/" + "ARDS" + "/range/" + MULTIPLIER + "/" + TIMESPAN + "/" + FROM + "/" + TO + "?adjusted=" \
                        + ADJUSTED + "&sort=" + SORT + "&limit=" + LIMIT + "&apiKey=" + APIKEY

restd = requests.get(link)
print("res",restd.text)

########################################################close  and open
link_day="https://api.polygon.io/v1/open-close/FUBO/2021-07-14?adjusted=true&apiKey=90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"

res_day = requests.get(link_day)
l=float(json.loads(res_day.text)["close"])
print("resDay_close",len(res_day.text))



url = "https://api.benzinga.com/api/v2/news?token=12eeca59c8674f098b785c5e2cb5c7b4"
response = requests.get(url)

print("ben",response)

from benzinga import news_data
api_key = "12eeca59c8674f098b785c5e2cb5c7b4"
import asyncio
import html
import logging
import json
import os
import signal
import sys
import websockets
BZ_API_KEY='12eeca59c8674f098b785c5e2cb5c7b4'
BZ_API_KEY = os.getenv('BZ_API_KEY', default='12eeca59c8674f098b785c5e2cb5c7b4')


def consumer(message):
    payload = json.loads(message)

    if payload["data"]["content"]:
        print("{kind} event received.\n\tAction: {action}\n\tEvent ID: {id}\n\tContent ID: {content_id}\n\tTitle: {title}\n\tTimestamp(UTC): {ts}\n".format(
            kind=payload["kind"],
            id=payload["data"]["id"],
            action=payload["data"]["action"],
            content_id=payload["data"]["content"]["id"],
            title=html.unescape(payload["data"]["content"]["title"]),
            ts=payload["data"]["timestamp"]
        ))
    else:
        print("{kind} event received.\n\tAction: {action}\n\tEvent ID: {id}\n\tTimestamp(UTC): {ts}\n".format(
            kind=payload["kind"],
            id=payload["data"]["id"],
            action=payload["data"]["action"],
            ts=payload["data"]["timestamp"]
        ))


async def runStream():
    if BZ_API_KEY == '':
        sys.exit('BZ_API_KEY must not be empty')

    uri = 'wss://api.benzinga.com/api/v1/news/stream?token={key}'.format(
        key="12eeca59c8674f098b785c5e2cb5c7b4")

    logger = logging.getLogger('websockets')
    logger.setLevel(logging.INFO)  # change to debug if needed
    logger.addHandler(logging.StreamHandler())

    logging.info("connecting to {}", uri)

    # messages can be over 1MB, increase max_size from default
    async with websockets.connect(uri, max_size=10_000_000_000) as websocket:
        # Close the connection when receiving SIGTERM.
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(
            signal.SIGTERM, loop.create_task, websocket.close())

        async for message in websocket:
            # This is where you would call your logic.
            consumer(message)

# run until disconnect
asyncio.get_event_loop().run_until_complete(runStream())
