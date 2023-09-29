from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from collections import defaultdict

import time
from datetime import datetime
import csv
import os



def configureSelenium(headless = False):
	# binary_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
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

def loadHomepage(wd,url):
	wd.get(url)
	time.sleep(1.5)
	return True

def searchTitle(query, wd, xpath = "//input[@name='q']"):
	search = wd.find_element(By.XPATH, xpath )
	search.send_keys(query)
	search.send_keys(Keys.RETURN)
	return search

def searchResults(xpath,wd):
	result = wd.find_element(By.XPATH,xpath)
	return result

def findPlotElement(wd,xpath):
	plot = wd.find_element(By.XPATH,xpath).get_attribute('textContent')
	if 'Read all' in plot:
		plot_elem2 = wd.find_element(By.XPATH,'//a[@data-testid="plot-read-all-link"]')
		plot_elem2.click()
		time.sleep(1.5)
		full_plot = wd.find_elements(By.XPATH,'//li[@class="ipl-zebra-list__item"]/p')
		plot = full_plot[0].get_attribute('textContent')
		wd.back()
		time.sleep(1.5)

	else:
		plot = plot
	return plot

def findTitle(wd,xpath):
	title = wd.find_element(By.XPATH,xpath).get_attribute('textContent')
	return title

def findRating(wd,xpath):
	rating = wd.find_elements(By.XPATH, xpath)
	if len(rating) > 1:
		rating = rating[1].get_attribute('textContent')
	else:
		rating = 'NA'
	return rating

def findListElements(wd,xpath):
	list_elements = wd.find_elements(By.XPATH, xpath)
	r = []
	for i in list_elements:
		r.append(i.get_attribute('textContent'))
	return r


def saveData(filename, data_dict):
	info_list = data_dict['Info'].split(',')
	file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0
	with open(filename + ".csv", "w") as f:
		csv_writer = csv.writer(f, delimiter=',')
		if not file_exists:
			csv_writer.writerow(['Title', 'Rating', 'Year','Type','PG Rating', 'Length', "Genres", "Cast", "Plot"])
		if len(info_list) == 3:
			csv_writer.writerow([data_dict['Title'],data_dict['Rating'],info_list[0], 'Movie',info_list[1],info_list[2],','.join(data_dict['Genres']),data_dict['Cast'],data_dict['Plot']])
		else:
			csv_writer.writerow([data_dict['Title'],data_dict['Rating'],info_list[1],info_list[0],info_list[2],info_list[3],' + '.join(data_dict['Genres']),data_dict['Cast'],data_dict['Plot']])
	print("File Saved")





def scrapeData():
	try:
		query = input("Enter your Query: ")
		print(f"Searching for {query} ...")	
		wd = configureSelenium(headless=True)
		homepage = loadHomepage(wd, url = "https://imdb.com")
		print("Opened IMDb")
		searchTitle(query = query, wd = wd)
		results = searchResults('//a[@class="ipc-metadata-list-summary-item__t"]',wd)
		results.click()
		print(f"Results Fetched!")
		time.sleep(1.5)
		print("Gathering Data...")
		plot = findPlotElement(wd = wd, xpath = '//span[@data-testid="plot-xl"]')
		title = findTitle(wd, '//span[@class="sc-afe43def-1 fDTGTb"]')
		rating = findRating(wd,'//span[@class="sc-bde20123-1 iZlgcd"]')
		infoList = findListElements(wd, '//div[@class="sc-e226b0e3-3 jJsEuz"]//ul/li' )
		genres = findListElements(wd, '//div[@class="ipc-chip-list__scroller"]//a')
		cast = findListElements(wd,'//div[@class="ipc-sub-grid ipc-sub-grid--page-span-2 ipc-sub-grid--wraps-at-above-l ipc-shoveler__grid"]/div/div/a')
		d = { 'Title' : [title], 'Rating' : [rating], 'Info' : infoList, 'Genres' : genres, 'Cast' : cast, 'Plot' : plot}
		for key,val in d.items():
			if type(val) == list:
				d[key] = ','.join(val)
		return d
	except Exception as e:
		print("Error!", e)
		return defaultdict(lambda : '0')

def displayer(data_dict):
	print("-----"*20+ "\n")
	print(f"Title: {data_dict['Title']}\n" )
	print(f"Rating: {data_dict['Rating']}\n")
	info_list = data_dict['Info'].split(',')
	try:
		if len(info_list) == 3:
			print(f"Year: {info_list[0]}\n")
			print(f"PG Rating: {info_list[1]}\n")
			print(f"Movie Length: {info_list[2]}\n")

		else:	
			print(f"Type: {info_list[0]}\n")
			print(f"Year: {info_list[1]}\n")
			print(f"PG Rating: {info_list[2]}\n")
			print(f"Episode Length: {info_list[3]}\n")
	except IndexError:
		print(f"Info: {data_dict['Info']}\n")
	print(f"Genres: {data_dict['Genres']}\n")
	print(f"Cast: {data_dict['Cast']}\n")
	print(f"Plot: {data_dict['Plot']}\n")
	print("-----"*20)

if __name__ == "__main__":
	try:
		start_time = datetime.now()
		data_dict = scrapeData()
		end_time = datetime.now()
		prompt = input("To Display in Terminal press 'd',\nTo save CSV file press 'f',\nTo display and save press 'df': ")	
		if prompt.lower() == "f":
			filename = "IMDb_Data"
			saveData(filename,data_dict)
		elif prompt.lower() == 'd':
			displayer(data_dict=data_dict)
		elif prompt.lower() == 'df':
			filename = "IMDb_Data"
			displayer(data_dict=data_dict)
			saveData(filename,data_dict)
			print('CSV File Saved')
		print(f"Time Taken = {(end_time-start_time).total_seconds()} seconds.")
	except Exception as e:
		print("Error!", e)




