
import time
import datetime
import winsound
from yahoofinancials import YahooFinancials
import json     # For parsing data
import requests # For pulling data
import time     # For dealing with time

from polygon import RESTClient
from datetime import datetime


def main():

    start_time = time.time()
    seconds = 0
    p=[]
    star_stock=[]
    top_gainer_all=[]
    top_gainer_temp=[]

    s=0
    t=0
    while True:
      float_share = []
      current_time = time.time()
      elapsed_time = current_time - start_time -s*seconds
      elapsed = current_time - start_time -t*300


      file = open("my.txt", "r")
      chosen=[]
      ourlist=[]
      p_new =[]
      flag=0


      if elapsed_time > seconds:

          s=s+1
          #print('timing puase:------------------------------->',s)
          for line in file:
              for word in line.split():
                  if word in chosen:
                      continue
                  else:
                    chosen.append(word)
                 # print("----------------")
                 # print(word)
          for stock in chosen:
              url = "https://api.polygon.io/v2/last/nbbo/" + stock + "?&apiKey=90w3p6QkgOldp2GfDqR9NaoMT5bCOp6P"
              response = requests.get(url)
              container = response.text
              #print(container)
              l=container.find("P")
              ll = container.find(",", l)
              #print("ll", ll)
              #print("l", l)
              if ll!=-1:

                 ##########################yahoo API
                 #yahoo_financials = YahooFinancials(stock)
                 #T = yahoo_financials.get_key_statistics_data()
                 #print(T)
                 #print(stock)
                 #try:
                    #float_share.append(T[stock]["floatShares"])
                 #except:
                     #float_share.append(0)

                 ##########################################
                 #print(float(container[l + 3:ll]))
                 p_new.append(float(container[l + 3:ll]))
                 ourlist.append(stock)

                 flag = flag + 1
                 #print("flag", flag)
                 if flag > len(p):
                    p.append(float(container[l + 3:ll]))

          if elapsed>300:
             t = t + 1
             star_stock=p_new
             #print("-----------------------------------star_stock",star_stock)
          star_stock=p
          #print("p_old",p)
          #print("ourlist",ourlist)
          #print("p_new:",p_new)
          #print("restart:",star_stock)

          for j in range(0, len(p)):

              if p_new[j] - p[j] > 0.03 * p[j]:
                  if (ourlist[j] in top_gainer_all) != 0:
                      continue
                  top_gainer_all.append(ourlist[j])
                  winsound.Beep(38, 1)
                  print("@@@@@@@SAlarm of stock", ourlist[j])
                  print("askp price=",p_new[j])
                  print("old price=", p[j])
                  #print("float_share=", float_share[j])
                  now = datetime.now()

                  current_time = now.strftime("%H:%M:%S")
                  print("Current Time =", current_time)

              if p_new[j] - star_stock[j] > 0.03 * star_stock[j]:
                if (ourlist[j] in top_gainer_temp)!=0:
                    continue
                winsound.Beep(38, 1)
                top_gainer_temp.append(ourlist[j])
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$Alarm of Star stock:", ourlist[j])
                print("ask price=",p_new[j])
                print("restart  price=", star_stock[j])
                print(" news price=", p[j])
                #print("float_share=", float_share[j])
                now = datetime.now()

                current_time = now.strftime("%H:%M:%S")
                print("Current Time =", current_time)

if __name__ == '__main__':
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    main()