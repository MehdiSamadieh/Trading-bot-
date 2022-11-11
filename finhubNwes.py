
import time
import datetime
import winsound
import json     # For parsing data
import requests # For pulling data
import time     # For dealing with time
import websocket
import requests
#print(r.json())
from yahoofinancials import YahooFinancials





def on_message(ws, message):
    print(message)
    current_time = datetime.datetime.now()
    print("Current Time =", current_time)

    #f = open("Finhub.txt", "a")
    #f.write("Current Time =  " + str(current_time) + " message=  "+message+ "\n\n")
    #f.close()

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    #ws.send('{"type":"subscribe-news","symbol":"AAPL"}')
    r = requests.get('https://finnhub.io/api/v1/stock/symbol?exchange=US&token=c3tnejiad3icmhf5ag1g')
    # print(r.json())
    print(len(r.json()))
    for i in range(0, len(r.json())):
        stock=(json.loads(r.text)[i]["displaySymbol"])
        ws.send('{"type":"subscribe-news","symbol":"'+stock+'"}')
        print("IIIIIIIIIIIIIII=",i)


        ticker = stock

        #yahoo_financials = YahooFinancials(ticker)
        #T = yahoo_financials.get_key_statistics_data()
        #if len(T)>160:

        # print(T[stock]["floatShares"])



        f = open("Finhub.txt", "a")
        f.write(stock +"\n")
        f.close()


if __name__ == "__main__":
    websocket.enableTrace(True)

    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=c3tnejiad3icmhf5ag1g",on_message = on_message,on_error = on_error,on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()