import json     # For parsing data
import requests # For pulling data
import time     # For dealing with time
v=["RSG"]
url = "https://api.polygon.io/v2/last/nbbo/"+v[0]+"?&apiKey=90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"

for i in range(0,1):
   print("ho")
   url = "https://api.polygon.io/v2/last/nbbo/" + v[i] + "?&apiKey=90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"
   # response = requests.request("GET", url)
   response = requests.get(url)
   # g=response["results"]
   container = response.text
   l = container.find("P")
   ll = container.find(",", l)
   print("ll", ll)

   try:
    url = "https://api.polygon.io/v2/last/nbbo/" + v[i] + "?&apiKey=90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"
    #response = requests.request("GET", url)
    response = requests.get(url)
    #g=response["results"]
    container=response.text
    l=container.find("P")
    ll=container.find(",",l)
    print("ll",ll)
   except:
    print("not working ")


    print("p",float(container[l+3:ll]))

    #h=response[status]
    print(response)
    print("jlnn,,,,,,,,,,,,")
    time.sleep(0)




