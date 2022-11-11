
import time
import datetime
import winsound
import json     # For parsing data
import requests # For pulling data
import time     # For dealing with time
import websocket

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe-news","symbol":"AAPL"}')


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=c3tnejiad3icmhf5ag1g",on_message = on_message,on_error = on_error,on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()