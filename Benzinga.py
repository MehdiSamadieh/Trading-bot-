from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions  
import pandas as pd
import config
from pdb import set_trace as byebug
from time import sleep
from retry import retry
import logging
from colorama import Fore, init
from bs4 import BeautifulSoup
from polygon import RESTClient
import requests # For pulling data

#---------------------------------------------------------------------------------------------
init(autoreset=True)
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(filename='log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
URL = 'https://pro.benzinga.com/dashboard/'
#---------------------------------------------------------------------------------------------
class Benzinga(object):

    def __init__(self):
        options = webdriver.FirefoxOptions()
        #options.add_argument('--headless')
        options.add_argument('window-size=1920x1080')
        self.driver = webdriver.Firefox(options=options) #webdriver.Chrome('/usr/bin/chromedriver') 
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, config.SCRAPER_TIMEOUT)
        self.login()
        self.load_news_feed()
        self.turn_off_ticker()
        self.filter_news()

    @retry(Exception, tries=config.BENZINGA_RETRY_ATTEMPTS)
    def login(self):
        self.driver.get(URL)
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'UserEntry-submit')))
        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')
        username.clear()
        password.clear()
        username.send_keys(config.SCRAPER_USERNAME)
        password.send_keys(config.SCRAPER_PASSWORD)
        self.driver.find_element_by_css_selector('.UserEntry-submit').click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'TUTORIAL_WorkspaceNav-Add')))
        print ('Login successful!')


    @retry(Exception, tries=config.BENZINGA_RETRY_ATTEMPTS)
    def load_news_feed(self):
        self.driver.find_elements_by_class_name('EmptyWorkspace-widgets')[0].find_elements_by_class_name('TUTORIAL_EmptyWorkspace-widget_Newsfeed')[0].click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'TUTORIAL_Search-input_Newsfeed')))
        print ('News feed is ready!')

    @retry(Exception, tries=config.BENZINGA_RETRY_ATTEMPTS)
    def turn_off_ticker(self):
        self.driver.find_element_by_class_name('TUTORIAL_WidgetContainer-Remove').click()
        self.driver.find_elements_by_class_name('PlatformBar-right--button')[-1].click()
        self.driver.find_element_by_xpath("//*[contains(text(), 'Settings')]").click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Preferences-section')))
        self.driver.find_elements_by_class_name('Preferences-section')[1].find_element_by_css_selector('button').click()
        self.driver.find_element_by_class_name('Modal-titleBar').find_element_by_class_name('u-closeIcon').click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'NewsfeedStory-topRow')))
        print ('News ticker turned off')

    @retry(Exception, tries=config.BENZINGA_RETRY_ATTEMPTS)
    def filter_news(self):
        try:
            self.driver.find_element_by_class_name('Modal-container')
        except exceptions.NoSuchElementException:
            self.driver.find_element_by_css_selector('.TUTORIAL_NewsfeedToolbar-Sources').click()
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'MillerColumns-columns')))

        menus=self.driver.find_element_by_css_selector('.NewsfeedModal').find_elements_by_class_name('MillerColumns-columns')[0].find_elements_by_class_name('MillerColumns-column')[1].find_elements_by_class_name('MillerColumns-item')
        for item in menus:
            v=item.find_elements_by_class_name('MillerColumns-name')[0]
            if v.text=='Press Releases': item.find_elements_by_class_name('MillerColumns-checkbox')[0].click()
            if v.text=='Benzinga Wire': item.find_elements_by_class_name('MillerColumns-checkbox')[0].click()
            #if v.text=='Press Releases' or v.text=='Benzinga Wire': item.find_elements_by_class_name('MillerColumns-checkbox')[0].click()
        self.driver.find_element_by_css_selector('.NewsfeedModal .Button--done').click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ReactVirtualized__Grid__innerScrollContainer')))
        print('News feed is filtered!')

    def update_news_snapshot(self):
        self.news_snapshot = BeautifulSoup(self.driver.page_source, 'lxml').findAll('div', class_='NewsfeedStory-topRow') 

    def newsfeed(self, get_old_news = True):
        self.update_news_snapshot()
        latest = self.news_snapshot[0].text

        if get_old_news:
            self.update_news_snapshot()
            for row in self.news_snapshot:
                symbol = row.findAll('div', class_='NewsfeedStory-symbols')[0].text.split('+')[0].strip()
                if not symbol: continue

                title=row.find('div', class_='NewsfeedStory-title').text.strip()
                time=row.find('div', class_='NewsfeedStory-time').text.strip()
                yield (time, symbol, title)

        self.driver.find_element_by_class_name('ReactVirtualized__List').send_keys(Keys.HOME)  
        sleep(5)

        while True:
            self.update_news_snapshot()
            if latest == self.news_snapshot[0].text:
                sleep(config.BENZINGA_REFRESH_INTERVAL)
                continue

            new_latest = None
            for row in self.news_snapshot:
                if not new_latest: new_latest = row.text
                if latest == row.text: break
                symbol = row.findAll('div', class_='NewsfeedStory-symbols')[0].text.split('+')[0].strip()
                if not symbol: continue
                title=row.find('div', class_='NewsfeedStory-title').text.strip()
                time=row.find('div', class_='NewsfeedStory-time').text.strip()
                yield(time, symbol, title)

            latest = new_latest

            self.driver.find_element_by_class_name('ReactVirtualized__List').send_keys(Keys.HOME)  
            sleep(5)

    
    
if __name__ == '__main__':
    benzinga = Benzinga()
    stock_list=[]

    try:
        for stock in benzinga.newsfeed():
            print('[{}] {}'.format(stock[0], stock[1]))
            #stock_list.append(stock[1])
            print(stock_list)
            f = open("my.txt", "a")

            f.write(str(stock[1]) +"\n")
            f.close()

    except Exception:
        # benzinga.driver.quit()
        raise





