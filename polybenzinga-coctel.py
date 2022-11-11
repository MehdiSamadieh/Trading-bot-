import time
import datetime
import winsound
#from yahoofinancials import YahooFinancials
import json     # For parsing data
import requests # For pulling data
import time     # For dealing with time
import  itertools
from polygon import RESTClient
# import RESTClient
from datetime import datetime
import datetime

from benzinga import news_data

def main():
    x = datetime.date.today()
    #STOCKSTICKER = "BLIN"  # Ticker of the stock

    # a day in seconds
    DAY = 86400

    # 3 days ago:
    threeDaysAgo = str(datetime.datetime.fromtimestamp(time.time() - (3 * DAY)))[:10]

    # today:
    today = str(datetime.datetime.fromtimestamp(time.time()))[:10]
    ############
    MULTIPLIER = "1"
    TIMESPAN = "minute"  # Choices:      minute \ hours \ day \ week \ month \ quarter \ year
    FROM =threeDaysAgo #str(x)  # Template:     yyyy-mm-dd
    TO = today#str(x)  # Template:     yyyy-mm-dd
    ADJUSTED = "true"  # Choices:      true \ false
    SORT = "desc"  # Choices:      desc \ asc
    LIMIT = "1"
    APIKEY = "90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"
    key_benzinga="12eeca59c8674f098b785c5e2cb5c7b4"
    ##############################################3last close
    start_time = time.time()
    seconds = 400
    lastTrade=[]
    lastClose=[]

    star_stock=[]
    top_gainer_all=[]

    chosen=[]
    timing=[]
    s=0
    VOLUM=[]


    f = open('my.txt', 'r+')
    f.truncate(0)



    while True:
      #float_share = []

      #print("lastClose",lastClose)
      #print("lastTrade",lastTrade)
      #print("timing:", timing)
      #print("top_gainer_all",top_gainer_all)

      #file = open("my.txt", "r")   work with file benzinga




      #for i in range(0,len(timing)-1):
          #print("i",i)
          #print("timing:",timing)

      for t in timing:
          i=timing.index(t)


          if timing[i]+seconds<time.time():

              timing.remove(timing[i])

              chosen.remove(chosen[i])
              lastTrade.remove(lastTrade[i])
              lastClose.remove(lastClose[i])
              VOLUM.remove(VOLUM[i])


      chosen_temp=[]
      paper = news_data.News(key_benzinga)
      stories = paper.news()

      for story in stories:
          if len(story["stocks"]) > 0:
              f = open("result.txt", "a")
              f.write("stock-news-Entered:" + str(story["stocks"][0]["name"]) + "\n")
              f.close()
              if str(story["stocks"][0]["name"]) in chosen:
                  print("")
              else:

                  chosen_temp.append((str(story["stocks"][0]["name"])))

                  f = open("result.txt", "a")
                  f.write("stock-news  is new:"+ str(story["stocks"][0]["name"])+ "\n")
                  f.close()
      for stock in chosen_temp:


                 puzzel=chosen_temp.index(stock)
                 link = "https://api.polygon.io/v2/aggs/ticker/" + stock + "/range/" + MULTIPLIER + "/" + TIMESPAN + "/" + FROM + "/" + TO + "?adjusted=" \
                        + ADJUSTED + "&sort=" + SORT + "&limit=" + LIMIT + "&apiKey=" + APIKEY

                 # Conversion of the requested JSON Object to Dictionary:

                 response_close = requests.get(link)
                 #print(stock)
                 #print(response_close.text)
                 # "https://api.polygon.io/v2/aggs/ticker/AAPL/prev?adjusted=true&apiKey=90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"
                 #try

                 url_trade = "https://api.polygon.io/v2/last/trade/" + stock + "?&apiKey=90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"
                 response = requests.get(url_trade)
                 ###########################################close day before
                 link_day = "https://api.polygon.io/v1/open-close/" + stock + "/2021-07-14?adjusted=true&apiKey=90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"

                 res_day = requests.get(link_day)
                 if len(response_close.text)>=185:
                    close = float(json.loads(response_close.text)["results"][0]["c"])

                 #elif len(response.text) >= 120:

                 #elif len(res_day.text)>=140:

                   ## close = float(json.loads(response.text)["results"]["p"])

                    #close = float(json.loads(res_day.text)["close"])

                    trade = float(json.loads(response.text)["results"]["p"])

                    ##################################################for last close
                    lastClose.append(close)
                    timing.append(time.time())
                    chosen.append(stock)

                    #####################################################for last trade

                    lastTrade.append(trade)

                    #############################################td VOLUME

                    #linktd = "https://api.tdameritrade.com/v1/marketdata/" + stock + "/quotes?apikey=GCURJZSYQBDSTFCHTCZNYMBOKRNJRZCW"

                    #restd = requests.get(linktd)
                    #volume = float(json.loads(restd.text)[stock]["totalVolume"])

                    ############################################################
                    volume = float(json.loads(response.text)["results"]["s"])
                    VOLUM.append(volume)
                 #except:
                     #print("are not accepted", stock)

      ################################################################################update chosen
      for stock in chosen:

                 url_trade = "https://api.polygon.io/v2/last/trade/" + stock + "?&apiKey=90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"
                 response = requests.get(url_trade)

                 trade = float(json.loads(response.text)["results"]["p"])
                 volume = float(json.loads(response.text)["results"]["s"])
                 #print("trade",trade)
                 ############################# #####################for last close
                 stock_index= chosen.index(stock)
                 lastTrade[stock_index]=trade
                 VOLUM[stock_index] = VOLUM[stock_index]+volume
      #print("listing", chosen)
      #print("lastclose", lastClose)

      #print("lasttrade", lastTrade)

      time.sleep(1)
      for stock in chosen:
          j=chosen.index(stock)
          if lastTrade[j] - lastClose[j] >=0.02* lastClose[j]:



              #winsound.beep(400,2000)
              print("\n\n\n\n@@@@@@\n\n\n@@@@@@\n\n\n@@@@@@\n\n\n@@@@SAlarm of stock", chosen[j])
              print("lastTrade price=", lastTrade[j])
              print("lastclose=", lastClose[j])

              ##############################################
              current_time=datetime.datetime.now()
              print("Current Time =", current_time)

              file = open("Anounce.txt", "a")
              file.write("stock Alaram@@@:  "+ chosen[j]+" lastTrade:  "+str(lastTrade[j])+"  newsPrice=  "+str(lastClose[j])+
                      "  Current Time =  "+ str(current_time)+" Total-Volume: "+str(VOLUM[j])+"\n")
              file.close()
              top_gainer_all.append(chosen[j])
              chosen.remove(chosen[j])
              lastClose.remove(lastClose[j])
              lastTrade.remove(lastTrade[j])
              VOLUM.remove(VOLUM[j])
              timing.remove(timing[j])



if __name__ == '__main__':
    current_time=datetime.datetime.now()
    print(current_time)
    main()