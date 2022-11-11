#!/usr/bin/env python3


import requests
import time

key = 'GCURJZSYQBDSTFCHTCZNYMBOKRNJRZCW'

def get_quotes(**kwargs):
	
	# Define endpoint URL
	url = 'https://api.tdameritrade.com/v1/marketdata/quotes'
	
	# Create parameters, update api key.
	params = {}
	params.update({'apikey': key})
	
	# Create and fill the symbol_list list with symbols from argument
	symbol_list = [symbol for symbol in kwargs.get('symbol')]
	params.update({'symbol': symbol_list})
	
	# Create request, with URL and parameters
	return requests.get(url, params=params).json()

def get_ohlc(**kwargs):
	data = get_quotes(symbol=kwargs.get('symbol'))
	for symbol in kwargs.get('symbol'):
		print(symbol)
		print(data)
		print(data[symbol]['lastPrice'])
		
		
def getOpen(symbol):
	
	data = get_quotes(symbol=[symbol])
	return str(data[symbol]['openPrice'])

		
def getHigh(symbol):
	
	data = get_quotes(symbol=[symbol])
	return str(data[symbol]['highPrice'])


def getLow(symbol):
	
	data = get_quotes(symbol=[symbol])
	return str(data[symbol]['lowPrice'])


def getClose(symbol):
	
	data = get_quotes(symbol=[symbol])
	return str(data[symbol]['closePrice'])


def getTotalVolume(symbol):
	
	data = get_quotes(symbol=[symbol])
	return str(data[symbol]['totalVolume'])


def getSecondVolume(symbol, lastTotalVolume):
	
	data = get_quotes(symbol=[symbol])
	secondVolume = data[symbol]['totalVolume'] - 0#lastTotalVolume
	return secondVolume


lastData = None
lastTotalVolume = None
tableRowCounter = 0

while True:
	symbol = 'AAPL'
	if tableRowCounter == 0: print("Open\tHigh\tLow\t\tClose\tVolume\t\t"+symbol)
	if tableRowCounter == 14: tableRowCounter = 0
	else: tableRowCounter += 1
	
	if lastTotalVolume == None:
		lastTotalVolume = int(getTotalVolume(symbol))
		continue
	
	row = ''
	row += getOpen(symbol) + '\t'
	row += getHigh(symbol) + '\t'
	row += getLow(symbol) + '\t'
	row += getClose(symbol) + '\t'
	row += str(getSecondVolume(symbol, lastTotalVolume)) + '\t'
	lastTotalVolume = int(getTotalVolume(symbol))
	

		
	print(row)
	time.sleep(1)