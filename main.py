import json 
import pycurl
from io import BytesIO
import config
from math import log, floor
from colorama import Fore, init
from time import sleep
from tabulate import tabulate
import os
from Benzinga import Benzinga
from threading import Thread, Event
import schedule
from datetime import datetime
from pdb import set_trace as byebug


#-----------------------------[Init]-----------------------------------------------#
init(autoreset=True)
clear = lambda: os.system('clear')
#----------------------------------------------------------------------------------#


#-----------------------------[Global Variable]------------------------------------#
news_list=[]
news_var=None
run_flag=False
saved_news_rows={}
#----------------------------------------------------------------------------------#


def human_format(number):
    if number==0: return 0
    units = ['', 'K', 'M', 'G', 'T', 'P']
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    return '%.2f%s' % (number / k**magnitude, units[magnitude])

def topgainer():
     response = BytesIO() 
     c = pycurl.Curl()
     c.setopt(c.URL, 'https://data-api-pro.benzinga.com/scanner?apikey='+config.API+'&fields=symbol%2Cprice%2Cchange%2CchangePercent%2CchangePercent5Minute%2CdayVolume%2CaverageVolume&filter=subtype_in_COMMON_SHARE%2CETF%2CADR&filter=dayVolume_bt_10000%2C&sortDir=DESC&sortField=changePercent5Minute&limit=100')
     c.setopt(c.WRITEFUNCTION, response.write)
     c.setopt(c.HTTPHEADER, ['User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0', 'Referer: https://pro.benzinga.com/', 'Connection: keep-alive', 'Accept: application/json','Host: data-api-pro.benzinga.com'])
     c.perform()
     c.close()
     y = json.loads(response.getvalue())
     response.close()
     return y
 
def return_list():
    add_list={}
    results=topgainer()
    for value in results['instruments']:
        if ((('changePercent1Minute' in value) and value['changePercent1Minute']> config.change_Percent_1Minute) \
            or (('changePercent5Minute' in value) and value['changePercent5Minute']> config.change_Percent_5Minute
            )) and ('dayVolume' in value) and float(value['dayVolume']!=0):
                
            #if value['symbol'] not in add_list:
            
            value = dict({'changePercent1Minute': 'N/A',
            'changePercent5Minute':'N/A', 'volume1Minute': 0,
            'symbol': 'N/A', 'gicsSectorName': 'N/A', 'shareFloat': 0,
            'sharesOutstanding': 'N/A', 'price': 'N/A', 'averageVolume':0,
            'dayVolume': 0, 'volume1min_hot': False, 'volumerelative_hot': False
            }, **value)
            
            if value['volume1Minute']!=0:
                value['volume1Minute']=float(value['volume1Minute'])
            if value['averageVolume']!=0:
                value['averageVolume']=float(value['averageVolume'])
            if value['dayVolume']!=0:
                value['dayVolume']=float(value['dayVolume'])
            
                if value['volume1Minute'] > config.volume_minimum_1minute: value['volume1min_hot']=True
                if (value['volume1Minute']!= 0 and (value['dayVolume'] / value['volume1Minute'] > config.volume_relative_threshold)): value['volumerelative_hot']=True
            
            # add_list[value['symbol']]= {'changePercent1Minute': value['changePercent1Minute'],
            # 'changePercent5Minute': value['changePercent5Minute'], 'volume1Minute': value['volume1Minute'],
            # 'symbol':value['symbol'], 'gicsSectorName': value['gicsSectorName'], 'shareFloat': value['shareFloat'],
            # 'sharesOutstanding':value['sharesOutstanding'], 'price': value['price'], 'averageVolume':value['averageVolume'],
            # 'dayVolume': value['dayVolume'], 'hot': 'Y' if(value['volume1min_hot']==True or value['volumerelative_hot']==True) else 'N'
            # } 
            
            add_list[value['symbol']]= {'symbol':value['symbol'], 'shareFloat': human_format(float(value['shareFloat'])), 'price': value['price'],
                                        'gicsSectorName': value['gicsSectorName'], 'dayVolume': human_format(value['dayVolume']), 'changePercent1Minute': value['changePercent1Minute'],
                                        'changePercent5Minute': value['changePercent5Minute'], 'hot': 'Y' if(value['volume1min_hot']==True or value['volumerelative_hot']==True) else 'N'
            } 
    return dict(sorted(add_list.items(), key=lambda item: item[1]['changePercent5Minute'], reverse=True))



#----------------------[news]-----------------------#
def news_thread():
        # DB.create_tables([News])
        for news in Benzinga().newsfeed():
            if news[1] in news_list or '$' in news[1] or ':' in news[1]: continue
            news_list.append(news[1])
            




#----------------------[schedule]-----------------------#

def schedule_start_time():
    global run_flag
    clear()
    run_flag=True
    
def schedule_end_time():
    global run_flag, news_var
    clear()
    run_flag=False
    #news_var.join()
    print("The market is closed!")
    
def schedule_start_news_time():
    global news_var
    clear()
    news_var=Thread(target=news_thread, daemon=True, name="news_thread")
    news_var.start()

def schedule_job():
    global run_flag
    if run_flag:
        
        try:
            clear()
            values=return_list()
            rows=[]
            for key in values:
                rows.append(list(values[key].values())+['Y' if key in news_list else 'N'])
                if (key in news_list):
                    if key not in saved_news_rows:
                        saved_news_rows[key]=[datetime.now().strftime("%H:%M:%S")]+list(values[key].values())
                        
                    else:
                        saved_news_rows[key]=[saved_news_rows[key][0]]+list(values[key].values())
            print(Fore.LIGHTCYAN_EX +"---------------------------------\nLast news update: {}\n---------------------------------".format(datetime.now().strftime("%H:%M:%S")))   
            print(tabulate(saved_news_rows.values(), headers=['Time', 'Symbol', 'float', 'price', 'sector','volume', '1m%', '5m%', 'hot' ]), end='\r')
            print("\n\n")
            print(Fore.LIGHTGREEN_EX +"---------------------------------\nLast scanner update: {}\n---------------------------------".format(datetime.now().strftime("%H:%M:%S")))
            print(tabulate(rows, headers=['Symbol', 'float', 'price', 'sector','volume', '1m%', '5m%', 'hot', 'news' ]), end='\r')
            
        except Exception as e:
            print(e)
            pass

def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]
    
if __name__ == '__main__':

    run_flag=is_between(datetime.now().strftime("%H:%M"), ("04:00", "20:00"))
    if not run_flag: print("The market is closed!")
    else: schedule_start_news_time()
    
    schedule.every().day.at("03:55:00").do(schedule_start_news_time)
    schedule.every().day.at("04:00:00").do(schedule_start_time)
    schedule.every().day.at("20:00:00").do(schedule_end_time)
    schedule.every(config.inteval_value).seconds.do(schedule_job) 
    while True:
        schedule.run_pending()
        sleep(1)
    
    
    
    # Thread(target=news_thread, daemon=True, name="news_thread").start()
    # while True:
    #     try:
    #         clear()
    #         values=return_list()
    #         rows=[]
    #         for key in values:
    #             rows.append( list(values[key].values())+['Y' if key in news_list else 'N'])
    #         print(tabulate(rows, headers=['Symbol', 'float', 'price', 'sector','volume', '1m%', '5m%', 'hot', 'news' ]), end='\r')
    #     except Exception as e:
    #         print(e)
    #         pass
    #     sleep(config.inteval_value)