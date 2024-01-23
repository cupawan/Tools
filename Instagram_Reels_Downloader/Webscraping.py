from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from collections import defaultdict



def configureSelenium():
        # binary_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless=new')
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        options.add_argument(f'user-agent={user_agent}')
        service = Service(ChromeDriverManager().install())
        wd = webdriver.Chrome(service=service,options=options)
        return wd

