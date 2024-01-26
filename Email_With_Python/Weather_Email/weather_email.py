from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import warnings
import sys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tabulate import tabulate
import csv
from tqdm import tqdm

class Weather():
        def __init__(self,location,sleep, verbose):
                self.location = location.lower()
                self.sleep = sleep
                self.verbose = verbose
                warnings.filterwarnings('ignore')
        def configureSelenium(self):
                options = webdriver.ChromeOptions()
                options.add_argument('--headless=new')
                options.add_argument("--window-size=1920,1080")
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--allow-running-insecure-content')
                user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
                options.add_argument(f'user-agent={user_agent}')
                service = Service(ChromeDriverManager().install())
                wd = webdriver.Chrome(service=service,options=options)
                return wd        
        def check_weather(self):
                wd = self.configureSelenium()
                url = f'https://www.google.com/search?q={self.location}+weather&oq={self.location}+weather&aqs=chrome..69i57.11368j0j4&sourceid=chrome&ie=UTF-8'
                try:
                        wd.get(url)
                        time.sleep(self.sleep)
                        location_element = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='wob_loc']")))
                        city = location_element.get_attribute('textContent')
                        temperature_element = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@id='wob_tm']")))
                        temp = temperature_element.get_attribute('textContent') + ' °C'
                        ppt_element = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@id='wob_pp']")))
                        ppt = ppt_element.get_attribute('textContent')
                        humidity_element = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@id='wob_hm']")))
                        humidity = humidity_element.get_attribute('textContent')
                        wind_element = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@id='wob_ws']")))
                        wind = wind_element.get_attribute('textContent')
                        date_element = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='wob_dts']")))
                        date = date_element.get_attribute('textContent')
                        sky_condition_element = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@id='wob_dc']")))
                        sky_condition = sky_condition_element.get_attribute('textContent')
                except Exception as e:
                        print(f"An error occurred: {e}")
                index = [self.location.replace("_"," ").title(),"Day", "Time" ,"Tempreture", "Precipitation", "Humidity", "Wind", "Sky Condition"]
                columns = ["Info"]
                day,timenow = date.split(',')                
                self.data = ["Weather", day, timenow ,temp, ppt, humidity, wind, sky_condition]
                df = pd.DataFrame(index=index,data=self.data,columns=columns)
                wd.quit()
                return df.to_html(index = True,header=False,justify='center')
                