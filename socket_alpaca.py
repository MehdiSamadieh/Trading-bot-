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
import alpaca_trade_api as tradeapi
import websocket

def on_open(ws):
    # print("jkajkbbbnbcz zzzzzzzzzzzzzzzzzzzz")

    # print("opened")
    # auth_data = {
    #     "action": "auth",
    #     "key": "{PK0A5NDDK4VA5HUKKD6Q}",
    #     "secret": "{4LXbI9cWfq9lRhG3XFrkjRCxnw0pgyLCfKsrM6Ej}"
        
    # }
    

    # ws.send(json.dumps(auth_data))

    print("opened")
    auth_data = {"action":"auth","key":"PKPTWYX4UL0A2E7301NI","secret":"CYXDkyc05Iy9eW6IyECqurYZtjia6575A1W3Y33f"}
    uth_data={"action": "auth", "key": "{PKPTWYX4UL0A2E7301NI}", "secret": "{CYXDkyc05Iy9eW6IyECqurYZtjia6575A1W3Y33f}"}

        

    ws.send(json.dumps(auth_data))
    channel_data ={"action":"subscribe","trades":["AAPL"],"quotes":["AMD","CLDR"],"bars":["AAPL","VOO"]}
    ws.send(json.dumps(channel_data))


    # channel_data = {
    #     "action": "subscribe",
    #     "params": TICKERS
    # }

    # ws.send(json.dumps(channel_data))

    # channel_data = {"action":"subscribe",
    # "trades":["AAPL"],"quotes":["AMD","CLDR"],
    # "bars":["AAPL","VOO"]
    # }

    ws.send(json.dumps(channel_data))

def on_message(ws, message):
    print("message:",message)


def on_close(ws):
    print("closed connection")



def main():

    

    socket = "wss://stream.data.alpaca.markets/v2/sip" 

    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)

    ws.run_forever()



if __name__ == "__main__":
    main()
    
    
