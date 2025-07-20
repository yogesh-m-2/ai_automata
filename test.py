# import requests
# import re
# from bs4 import BeautifulSoup
#
# # POST request details
# url = "https://all-hashtag.com/library/actions/ajax-keyword-generator.php"
# payload = {
#     "keyword": "donaldtrump",
#     "filter": "top"
# }
# headers = {
#     "Content-Type": "application/x-www-form-urlencoded",
#     "User-Agent": "Mozilla/5.0"
# }
#
# # Send the POST request
# response = requests.post(url, data=payload, headers=headers)
#
# # Parse the HTML response
# soup = BeautifulSoup(response.text, "html.parser")
#
# # Extract hashtags using regex
# hashtags = re.findall(r'#\w+', soup.get_text())
#
# # Remove duplicates while preserving order
# from collections import OrderedDict
# unique_hashtags = list(OrderedDict.fromkeys(hashtags))
#
# # Join with space and print
# output = ' '.join(unique_hashtags)
# print(output)

import json
from time import sleep
import pyperclip
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver
import os
import configparser
from selenium.common.exceptions import UnableToSetCookieException, ElementNotInteractableException



def run(config_path=None,kill_chrome=False,headless=False):
        config = configparser.ConfigParser()

        if kill_chrome:
            os.system("taskkill /im chrome.exe /f")

        # Default path: same directory as this script
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        config.read(config_path)
        user_data_dir = config['SELENIUM']['USER_DATA_DIR']

        driver = Driver(uc=True)
        sleep(3)
        driver.get("https://www.chatgpt.com")
        sleep(3)
        input_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//p[@data-placeholder='Ask anything']"))
        )
        input_element.send_keys("hi")
        sleep(1)
        input_element.send_keys(Keys.ENTER)
        sleep(1)
        WebDriverWait(driver, 2000).until(
            EC.invisibility_of_element_located((By.ID, "composer-submit-button"))
        )
        inputElements = WebDriverWait(driver, 20).until(
            EC.visibility_of_all_elements_located((By.XPATH,
                                                   "//div[@class='whitespace-pre-wrap' and normalize-space(.)='" + "hi" + "']/following::p[@data-start]"))
        )
        results = []
        for element in inputElements:
            results.append(element.text)
        print(results)

        driver.quit()

run()