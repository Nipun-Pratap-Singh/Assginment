import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

class CoinMarketCap:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service('/path/to/chromedriver'), options=chrome_options)

    def fetch_coin_data(self, coin_name):
        url = f"https://coinmarketcap.com/currencies/{coin_name}/"
        self.driver.get(url)

        data = {}

        try:
            data['price'] = self.driver.find_element(By.XPATH, 'xpath_to_price').text
            # Continue scraping other required details using selenium find methods
            # Fill in the rest of the data dictionary similarly
        except Exception as e:
            data['error'] = str(e)

        return data

    def close(self):
        self.driver.quit()
