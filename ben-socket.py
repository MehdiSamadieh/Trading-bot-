
import time
import datetime
import winsound
import json     # For parsing data
import requests # For pulling data
import time     # For dealing with time
from datetime import date
from datetime import datetime
from benzinga import news_data
#while(1):
   #url = "https://api.benzinga.com/api/v2/news?token=12eeca59c8674f098b785c5e2cb5c7b4"
  # benzinga = requests.get(url)


chosen=[]

import benzinga
  # print("benzinga=",benzinga.text)
api_key = "12eeca59c8674f098b785c5e2cb5c7b4"
while(1):
    time.sleep(1)

    paper = news_data.News(api_key)
    stories = paper.news()
    for story in stories:
        if (story["stocks"] in chosen)==False:

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            if  len(story["stocks"])>0:
                print("@@@=\n",story["stocks"][0]["name"])
                if str(story["stocks"][0]["name"]) in chosen==False:
                   chosen.append((str(story["stocks"][0]["name"])))
                   print("" + str(story["stocks"]), "Current Time:", current_time, "chosen:",chosen)
                   f = open("newsRelease.txt", "a")

                   f.write("" + str(story["stocks"])+ " Current Time:"+ current_time+"\n")
                   f.close()





