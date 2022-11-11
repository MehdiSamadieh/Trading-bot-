# Created by: Alireza Teimoori
# Created on: 14 / 07 / 2021

# Explanation:  This code tests the functionality of the recentVolume function
#               by putting it through a while loop and checking every 1 second.
#               
#               The actual usable code can be found in recentVolume.py 

import requests, json, time

# Configs: ( .: Please refer to https://polygon.io/docs under "Aggregates (Bars)" for more details :. )

STOCKSTICKER    = " FUBO"            # Ticker of the stock
MULTIPLIER      = "1"
TIMESPAN        = "minute"          # Choices:      minute \ hours \ day \ week \ month \ quarter \ year
FROM            = 0                 # UNIX time -   To be set in the while loop
TO              = 0                 # UNIX time -   To be set in the while loop
ADJUSTED        = "true"            # Choices:      true \ false
SORT            = "desc"            # Choices:      desc \ asc
LIMIT           = "3"               # This tells how many results you want to get. (KEEP on 2 -- FIRST IS CURRENT)
APIKEY          = "90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"

while True:

    # Update time:

    FROM        = str(round((time.time()-59)*1000))    # Template:     yyyy-mm-dd
    TO          = str(round(time.time()*1000))          # Template:     yyyy-mm-dd

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

    # This line will give you the "results" array as a string:
    print(len(response.text))
    resultsAsText = json.loads(response.text)["results"] 
    
    # This lines transforms that string into a real array which we call results:
    results = list(eval(str(resultsAsText))) 
    
    #
    # IMPORTANT: "results" is the array of *CANDLES* (each candle is a python dictionary type)
    #

    recentVolume = 0        # Reset the volume summation for the next print

    for result in results:  # For every given candle
        
        recentVolume += result["v"]     # Adds upp the volume
    

    print("\nlast 3 mins total Volume: " + str(recentVolume))   # prints the last 3 min total volume

    time.sleep(1)   # Every 1 second

########
# I don't know how this code will handle the beginning minutes of any market as
# there will not be any "previous" data there.
########