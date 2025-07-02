from time import sleep

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver
import os
import configparser


class Chat:
    def __init__(self, config_path=None,kill_chrome=False):
        self.config = configparser.ConfigParser()

        if kill_chrome:
            os.system("taskkill /im chrome.exe /f")

        # Default path: same directory as this script
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        self.config.read(config_path)
        self.user_data_dir = self.config['SELENIUM']['USER_DATA_DIR']
        self.driver = Driver(uc=True, user_data_dir=self.user_data_dir)

    def prompt(self, query):
        self.driver.get("https://www.chatgpt.com")
        input_element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//p[@data-placeholder='Ask anything']"))
        )
        input_element.send_keys(query)
        sleep(1)
        input_element.send_keys(Keys.ENTER)
        sleep(1)
        WebDriverWait(self.driver, 2000).until(
            EC.invisibility_of_element_located((By.ID, "composer-submit-button"))
        )
        inputElements = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='whitespace-pre-wrap' and normalize-space(.)='" + query + "']/following::p[@data-start]"))
        )
        results = []
        for element in inputElements:
            results.append(element.text)
        # self.driver.quit()
        return(results)

