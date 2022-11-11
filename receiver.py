import json     # For parsing data
import requests # For pulling data
import time     # For dealing with time

# CONSTANTS
Ticker = "EQ"
Duration = 1

# REQUEST LINKS

url = "https://api.polygon.io/v2/last/nbbo/" + Ticker + "?&apiKey=90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"
#url2 = "https://api.polygon.io/v2/last/trade/" + Ticker + "?&apiKey=90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"
url2 = "https://api.polygon.io/v2/last/trade/" + Ticker + "?&apiKey=90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"
while 1:
    #response = requests.request("GET", url)
    response = requests.get(url)
    response2 = requests.get(url2)
    resultsAsText = json.loads(response.text)["results"]["P"]
    print("res",resultsAsText)
    container = response.text
    container2 = response2.text
    print("EQ",response2.text)
    print("Eq_len",len(response2.text))

    l = container.find("P")
    ll = container.find(",", l)

    l2 = container2.find("p")
    ll2 = container2.find(",", l2)

    print("Last Quote ==> " + container[l + 3 : ll])


    print("Last Trade ==> " + container2[l2 + 3 : ll2])

    print(".\n.\n.")

    time.sleep(Duration)