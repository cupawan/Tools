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
        def check_weather(self,query):
                wd = self.configureSelenium()
                url = f'https://www.google.com/search?q={query}+weather&oq={query}+weather&aqs=chrome..69i57.11368j0j4&sourceid=chrome&ie=UTF-8'
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
                index = [self.location.title(),'Tempreture','Precipitation','Humidity','Wind','Day and Time','Sky Condition']
                columns = ["Info"]
                self.data = [city, date, temp, ppt, humidity, wind, sky_condition]
                df = pd.DataFrame(index=index,data=self.data,columns=columns)
                day,timenow = date.split(',')
                self.data = [query.title(), day, timenow ,temp, ppt, humidity, wind, sky_condition]
                if self.verbose:
                        print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
                time.sleep(self.sleep)
                wd.quit()
        def process_multiple_queries(self,queries,csv_path):
                df = pd.read_csv(csv_path)
                available_cities = list(df['Place'])
                for query in tqdm(queries, total=len(queries), desc= f"Checking Weather..."):
                        self.check_weather(query)
                        self.make_csv(csv_path)
        def make_csv(self, csv_path):
                self.csv_path = csv_path
                with open(csv_path, 'a+') as f:
                        csv_writer = csv.writer(f,lineterminator='\n')
                        csv_writer.writerow(self.data)
                


if __name__ == "__main__":
        save_csv_path = 'scraped_data.csv'
        weather_instance = Weather(location = '', sleep = 1,verbose = True)        
        if len(sys.argv) < 3:
                print("Usage: python3 weather_updated.py location1 [location2 location3 ...]")
                sys.exit(1)
        if sys.argv[1] != "--multiple":
                query = ' '.join(sys.argv[1:])
                weather_instance.location = query.title()        
                weather_instance.check_weather(query=query)
                weather_instance.make_csv(csv_path= save_csv_path)
        else:
                weather_instance.verbose = False
                queries = sys.argv[2:]
                len_queries = len(queries)
                weather_instance.process_multiple_queries(queries = queries, csv_path=save_csv_path)
                df = pd.read_csv(save_csv_path)
                df.drop_duplicates(subset = ['Place'],keep='last')
                show = input("Show Table?: ")
                if show.lower() in ["yes", "y", "yup", "yeah"]:
                        print(tabulate(df.tail(len_queries), headers='keys', tablefmt='fancy_grid'))
                else:
                        print(f"Table saved at {weather_instance.csv_path}")

