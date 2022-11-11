import websocket
import time
import datetime
#from yahoofinancials import YahooFinancials
import json     # For parsing data
import requests # For pulling data
import time     # For dealing with time
import  itertools
from polygon import RESTClient
# import RESTClient
from datetime import datetime
import datetime


######################################################AGGregate para

symbol = "AAPL"

# a day in seconds
DAY = 86400

# 3 days ago:
threeDaysAgo = str(datetime.datetime.fromtimestamp(time.time()-(3 * DAY)))[:10]

# today:
today = str(datetime.datetime.fromtimestamp(time.time()))[:10]

# Configs: ( .: Please refer to https://polygon.io/docs under "Aggregates (Bars)" for more details :. )

STOCKSTICKER    = symbol            # Ticker of the stock
MULTIPLIER      = "1"               # Width of each bar
TIMESPAN        = "minute"          # Choices:      minute \ hours \ day \ week \ month \ quarter \ year
FROM            = threeDaysAgo      # Template:     yyyy-mm-dd
TO              = today             # Template:     yyyy-mm-dd
ADJUSTED        = "true"            # Choices:      true \ false
SORT            = "desc"            # Choices:      desc \ asc
LIMIT           = "1"               # How many results you want to get
APIKEY          = "90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"


# Conversion of the requested JSON Object to Dictionary:

#########################################################################

APIKEY = "90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"
key_benzinga="4146d7af17e2476b9e1b543c42e05555"

from benzinga import news_data

# global volume
Volume = 0

volumes = []
chosen_temp = {""}
chosen={}

def on_open(ws):

    print("opened")
    auth_data = {
        "action": "auth",
        "params": API_KEY
    }

    ws.send(json.dumps(auth_data))

    channel_data = {
        "action": "subscribe",
        "params": TICKERS
    }


    ws.send(json.dumps(channel_data))
    channel_data = {
        "action": "subscribe",
        "params": "A.TSLA"
    }


    ws.send(json.dumps(channel_data))


def on_message(ws, message):
    global Volume
    global chosen_temp
    global i
    global chosen

    seconds=400
    print("message:",message)


    paper = news_data.News(key_benzinga)
    stories = paper.news()

    News={""}

    #print("@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("stories:",stories)
    News.clear()

    for story in stories:

        if len(story["stocks"]) > 0:
            #f = open("oha_Result.txt", "a")
            #f.write("stock-news-Entered:" + str(story["stocks"][0]["name"]) + "\n")
            #f.clofse()

            if str(story["stocks"][0]["name"]) in chosen_temp:
                i=0
            else:
                stock_name=str(story["stocks"][0]["name"])
                chosen_temp.add(stock_name)

                News.add(stock_name)

                channel_data = {
                    "action": "subscribe",
                    "params": "A."+stock_name
                }

                ws.send(json.dumps(channel_data))


                print("subs", stock_name)

    stock_sym=str(json.loads(message)[0]["sym"])


    print("chosen=",chosen)
    print("sym=",stock_sym)
    print("##########################################################",float(json.loads(message)[0]["v"]))
    if stock_sym in chosen:
        print("stock_sym",stock_sym)
        #chosen[stock_sym]["vol_acu"] = float(json.loads(message)[0]["v"])+chosen[stock_sym]["vol_acu"]

        #print("type(chosen[stock_sym])", type(chosen[stock_sym]))

        Volume=chosen[stock_sym]["vol_acu"]+float(json.loads(message)[0]["v"])
        #print("chosen before", chosen)
        #print("chosen[stock_sym][vol_acu]",chosen[stock_sym]["vol_acu"])
        #print("float(json.loads(message)[0][v]", float(json.loads(message)[0]["v"]))
        #print("Volume", Volume)

        chosen[stock_sym]["vol_acu"] =Volume
        #print("chosen[stock_sym][vol_acu]",chosen[stock_sym]["vol_acu"])
        #print("chosen after", chosen)
        chosen[stock_sym]["volume"] = float(json.loads(message)[0]["v"])
        chosen[stock_sym]["av_vol"] = float(json.loads(message)[0]["av"])
        chosen[stock_sym]["last_trade"] = float(json.loads(message)[0]["c"])
        #print("chosen in $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", chosen)
    else:
      print("################################",stock_sym)
      chosen[stock_sym] = {}
      chosen[stock_sym]["start"] = time.time() #float(json.loads(message)[0]["s"])
      chosen[stock_sym]["vol_acu"] = float(json.loads(message)[0]["v"])
      chosen[stock_sym]["volume"] = float(json.loads(message)[0]["v"])
      chosen[stock_sym]["av_vol"] = float(json.loads(message)[0]["av"])
      chosen[stock_sym]["last_trade"] = float(json.loads(message)[0]["c"])
      link = "https://api.polygon.io/v2/aggs/ticker/" + stock_sym + "/range/" + MULTIPLIER + "/" + TIMESPAN + "/" + FROM + "/" + TO + "?adjusted=" \
           + ADJUSTED + "&sort=" + SORT + "&limit=" + LIMIT + "&apiKey=" + APIKEY
      response_close = requests.get(link)
      if len(response_close.text) >= 185:
         chosen[stock_sym]["last_close"] = float(json.loads(response_close.text)["results"][0]["c"])
      else:
         chosen[stock_sym]["last_close"] = float(json.loads(message)[0]["c"])
    ###################################################### check the alaram  comnditions
    if (chosen[stock_sym]["last_trade"] - chosen[stock_sym]["last_close"]>= 0.02* chosen[stock_sym]["last_close"] or (chosen[stock_sym]["last_trade"] - chosen[stock_sym]["last_close"]<= -0.02* chosen[stock_sym]["last_close"])) and stock_sym !="AAPL" and stock_sym !="TSLA":
      f = open("oha_Result.txt", "a")
      f.write("Alaram For: " + str(stock_sym) +" Sign: "+str(chosen[stock_sym]["last_trade"] - chosen[stock_sym]["last_close"] )+" volume=  "+str(chosen[stock_sym]["volume"])+" total volume=  "+str(chosen[stock_sym]["vol_acu"])+" ave volume=  "+str(chosen[stock_sym]["av_vol"])+ " news time = "+str(chosen[stock_sym]["start"])+
      " News_price= "+str(chosen[stock_sym]["last_close"])+ " last _trade = "+str(chosen[stock_sym]["last_trade"]) +" current time= "+ str(datetime.datetime.now())+"\n\n")
      f.close()
      channel_data = {
          "action": "unsubscribe",
          "params": "A." + stock_sym
      }
      ws.send(json.dumps(channel_data))
      chosen.pop(stock_sym)
      chosen_temp.pop(stock_sym)

    if chosen[stock_sym]["start"]+seconds<time.time() and stock_sym !="AAPL" and stock_sym !="TSLA":
        channel_data = {
            "action": "unsubscribe",
            "params": "A." + stock_sym
        }
        ws.send(json.dumps(channel_data))
        chosen.pop(stock_sym)
        chosen_temp.pop(stock_sym)




    #####################################################



    print("chosen$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", chosen)





    #channel_data = {
     #   "action": "subscribe",
        #"params": "A.AHT"
   # }
    #ws.send(json.dumps(channel_data))
   # channel_data = {
       # "action": "unsubscribe",
        #"params": "A.AAPL"
    #}
    #ws.send(json.dumps(channel_data))


def on_close(ws):
    print("closed connection")





def main():
    global API_KEY
    API_KEY = "90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"
    global  SYMBOL
    SYMBOL = "AAPL"
    global TICKERS
    TICKERS = "A.AAPL"

    socket = "wss://socket.polygon.io/stocks"

    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)

    ws.run_forever()


if __name__ == "__main__":
    main()
