# Modules:

import json     # For decoding data
import requests # For getting data
import time     # For dealing with time
import datetime # for historical stuff

# symbol:
symbol = "AAPL"

# a day in seconds
DAY = 86400

# 3 days ago:
threeDaysAgo = str(datetime.datetime.fromtimestamp(time.time()-(180 * DAY)))[:10]

# today:
today = str(datetime.datetime.fromtimestamp(time.time()))[:10]

# Configs: ( .: Please refer to https://polygon.io/docs under "Aggregates (Bars)" for more details :. )

STOCKSTICKER    = symbol            # Ticker of the stock
MULTIPLIER      = "1"               # Width of each bar
TIMESPAN        = "day"          # Choices:      minute \ hours \ day \ week \ month \ quarter \ year
FROM            = threeDaysAgo      # Template:     yyyy-mm-dd
TO              = today             # Template:     yyyy-mm-dd
ADJUSTED        = "true"            # Choices:      true \ false
SORT            = "desc"            # Choices:      desc \ asc
LIMIT           = "180"               # How many results you want to get
APIKEY          = "90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"


# Link Generator:

link =  "https://api.polygon.io/v2/aggs/ticker/"    \
        + STOCKSTICKER                              \
        + "/range/"                                 \
        + MULTIPLIER                                \
        + "/"                                       \
        + TIMESPAN                                  \
        + "/"                                       \
        + FROM                                      \
        + "/"                                       \
        + TO                                        \
        + "?adjusted="                              \
        + ADJUSTED                                  \
        + "&sort="                                  \
        + SORT                                      \
        + "&limit="                                 \
        + LIMIT                                     \
        + "&apiKey="                                \
        + APIKEY

# Conversion of the requested JSON Object to Dictionary:

response = requests.get(link)

resultsAsText = json.loads(response.text)["results"] # This line will give you the "results" array as a string

results = list(eval(str(resultsAsText))) # This lines transforms that string into a real array which we call results
print(results)
for i  in range(len(resultsAsText)):
        diff=int(resultsAsText[i]["h"])-int(resultsAsText[i]["o"])
        if diff>0.4*int(resultsAsText[i]["o"]):
                print("##########################   former runer   ####################")

# previousCandle = results[0]

# print("\nprinting the CLOSE of the previous candle (LITERALLY THE LAST CANDLE) as an example: \n")
# print(previousCandle["c"])
