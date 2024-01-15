from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from collections import defaultdict
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
from datetime import datetime
import pandas as pd
from tabulate import tabulate
import textwrap


class IMDBScraper:
    def __init__(self,headless):
          self.headless = headless
          self.wd = self.configureSelenium()    
    def configureSelenium(self):
        chrome_options = {
        "window-size": "1920,1080",
        "ignore-certificate-errors": True,
        "allow-running-insecure-content": True,
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
		"headless" : self.headless
    }
        options = webdriver.ChromeOptions()
        for key, value in chrome_options.items():
            options.add_argument(f"--{key}={value}")
        service = Service(ChromeDriverManager().install())
        wd = webdriver.Chrome(service=service, options=options)
        return wd
    def loadHomepage(self,url):
        self.wd.get(url)
        WebDriverWait(self.wd, 10).until(EC.title_contains("IMDb"))
        return True
    def searchTitle(self,query, xpath="//input[@name='q']"):
        search = WebDriverWait(self.wd, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        search.send_keys(query)
        search.send_keys(Keys.RETURN)
        return search
    def searchResults(self,xpath):
        result = WebDriverWait(self.wd, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return result
    def findPlotElement(self, xpath):
        wait = WebDriverWait(self.wd, 10)
        plot_element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        plot_text = plot_element.text
        if "Read more" in plot_text:    
            plot_element.click()
            full_plot = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@class="ipl-zebra-list__item"]/p')))
            plot_text = full_plot[0].get_attribute('textContent')
        else:
            plot_text = plot_element.text
        return plot_text
    def findTitle(self, xpath):
        title = self.wd.find_element(By.XPATH, xpath).get_attribute('textContent')
        return title
    def findRating(self, xpath):
        rating = self.wd.find_elements(By.XPATH, xpath)
        if len(rating) > 1:
            rating = rating[1].get_attribute('textContent')
        else:
            rating = 'NA'
        return rating
    def findListElements(self,xpath):
        list_elements = self.wd.find_elements(By.XPATH, xpath)
        r = []
        for i in list_elements:
            r.append(i.get_attribute('textContent'))
        return r
    def scrapeData(self):
        try:
            query = input("Enter your Query: ")
            print(f"Searching for {query} ...")    
            wait = WebDriverWait(self.wd, 10) 
            homepage = self.loadHomepage(url="https://imdb.com")
            self.searchTitle(query=query)
            results = self.searchResults('//a[@class="ipc-metadata-list-summary-item__t"]')
            results.click()
            plot = self.findPlotElement(xpath='//p[@data-testid="plot"]')
            title = self.findTitle('//h1[@data-testid="hero__pageTitle"]')
            rating = self.findRating('//span[@class="sc-bde20123-1 cMEQkK"]')
            infoList = self.findListElements('//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt"]/li')
            genres = self.findListElements('//div[@class="ipc-chip-list__scroller"]//a')
            cast = self.findListElements('//div[@class="ipc-sub-grid ipc-sub-grid--page-span-2 ipc-sub-grid--wraps-at-above-l ipc-shoveler__grid"]/div/div/a')
            d = { 'Title' : [title], 'Rating' : [rating], 'Info' : infoList, 'Genres' : genres, 'Cast' : cast, 'Plot' : plot}
            for key,val in d.items():
                if type(val) == list:
                    d[key] = ','.join(val)
            return d
        except Exception as e:
            print("Error!", str(e))
            return defaultdict(lambda: '0')
        finally:
            self.wd.quit()

if __name__ == "__main__":
    try:
        imdb_instance = IMDBScraper(headless=True)
        start_time = datetime.now() 
        data_dict = imdb_instance.scrapeData()
        end_time = datetime.now()
        index = range(6)
        table_data = [[key, textwrap.fill(value, width=30)] for key, value in data_dict.items()]
        df = pd.DataFrame(table_data,index = index)
        print(tabulate(df.transpose(), tablefmt='fancy_grid'))
        print(f"Time Taken = {(end_time-start_time).total_seconds()} seconds.")
    except Exception as e:
        print("Error!", str(e))
