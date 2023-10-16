from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from Webscraping import configureSelenium
import time
import requests
import os

def loginToInstagram(wd, user, passwd):
    username_xpath = '//input[@name="username"]'
    password_xpath = '//input[@name="password"]'
    username = wd.find_element(By.XPATH, username_xpath)
    password = wd.find_element(By.XPATH, password_xpath)
    username.send_keys(user)
    username.send_keys(Keys.TAB)
    password.send_keys(passwd)
    password.send_keys(Keys.ENTER)
    time.sleep(5)
    wd.find_element(By.XPATH,'//div[@role="button"]').click()
    
def scroll_and_wait_for_elements(wd):
    all_links = []
    element_xpath = '//div[@class="_aabd _aa8k  _al3l"]/a'
    last_height = wd.execute_script("return document.body.scrollHeight")
    while True:
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        new_height = wd.execute_script("return document.body.scrollHeight")
        elements = wd.find_elements(By.XPATH, element_xpath)
        wait = WebDriverWait(wd, 5)
        visible_elements = wait.until(lambda driver: [element for element in elements if element.is_displayed()])
        for i in visible_elements:
            all_links.append(i.get_attribute('href'))
        print(f"INFO >> Current Height : {new_height}")
        print(f"INFO >> Reels Fetched : {len(set(all_links))}")
        if new_height == last_height:
            break
        last_height = new_height
    return all_links

def processOneLink(wd, link):
    print(f"<><><><><><><><><><> {link} <><><><><><><><><>")
    pasteherexpath = '//input[@id="s_input"]'
    pastehere = wd.find_element(By.XPATH, pasteherexpath)
    pastehere.send_keys(link)
    pastehere.send_keys(Keys.ENTER)
    time.sleep(3)
    try:
        downloadit = '//a[@title="Download Video 1"]'
        dlink = wd.find_element(By.XPATH, downloadit).get_attribute('href')
        wd.get(dlink)
        time.sleep(10)
        print('Downloaded in Try')

    except:
        close = '//button[@id="closeModalBtn"]'
        wd.find_element(By.XPATH, close).click()
        downloadit = '//a[@title="Download Video 1"]'
        dlink = wd.find_element(By.XPATH, downloadit).get_attribute('href')
        wd.get(dlink)
        time.sleep(10)
        print('Downloaded in Except')

if __name__ == "__main__":    
    road = input("Do you have the CSV file? Yes/No: ") 
    wd = configureSelenium()  
    if road.lower() == "no":         
        USERNAME =  input("Enter your instagram username: ")  
        PASSWORD = input('Enter your instagram password')
        URL = f"https://www.instagram.com/{USERNAME}/saved/all-posts/"    
        wd.get(URL)
        time.sleep(5)
        loginToInstagram(wd=wd, user = USERNAME, passwd= PASSWORD)
        time.sleep(10)
        all_reels = scroll_and_wait_for_elements(wd)
        print(f"TOTAL NUMBER OF REELS: {len(set(all_reels))}")
        df = pd.DataFrame()
        df['Links'] = list(set(all_reels))
        df.to_csv('links_new_final.csv')
    else:        
        filename = input("Enter the filename: ")
        data = pd.read_csv(filename)
        print(data.head())
        all_links = data['Links']
        print(len(all_links), "Links")
        for i, link in enumerate(all_links):
            try:
                response = requests.get(link)
            except:
                print("Connection problem, waiting for 30 seconds...")
                time.sleep(30)
                continue
            if response.status_code == 200:
                link_name = link.split('/')[-2]
                if not os.path.exists(f"Downloaded_Reels/{link_name}.mp4"):
                    with open(f"Downloaded_Reels/{link_name}.mp4", "wb") as file:
                        file.write(response.content)
                        print(f"Downloaded {link}, Number {i} / {len(all_links)}")
                else:
                    print(i,"Already Downloaded")
            else:
                print(f"Failed to download {link}.")
    wd.quit()
