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
from selenium.common.exceptions import TimeoutException
import time

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
        self.driver = Driver(uc=True, user_data_dir=self.user_data_dir,headless=False)

    def set_cookie(self):
        with open("cookies.json", "r") as f:
            cookies = json.load(f)
        try:
            for cookie in cookies:
                self.driver.add_cookie(cookie)
                print(cookie)
        except UnableToSetCookieException as e:
            print("UnableToSetCookieException occurred!")
            print(f"Exception message: {e}")  # Prints the exception's message
            return


    def prompt(self, query, copy_json=False):
        self.driver.get("https://www.chatgpt.com")
        try:
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

            if copy_json:
                copy_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "button.flex.gap-1.items-center.select-none.py-1[aria-label='Copy']"))
                )
                self.driver.execute_script("arguments[0].scrollIntoView(true);", copy_button)
                if copy_button:
                    # Click the copy button
                    copy_button.click()

                    # Wait a moment for the copy operation to complete
                    sleep(0.5)

                    # Get the copied text from clipboard
                    copied_text = pyperclip.paste()
                    results.append(copied_text)
            return(results)
        except ElementNotInteractableException:
            login_prompt = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='flex items-center justify-center' and text()='Log in']"))
            )
            if login_prompt:
                self.set_cookie()
            return self.prompt(query)

    # def prompt(self, query):
    #     self.driver.get("https://www.chatgpt.com")
    #     input_element = WebDriverWait(self.driver, 20).until(
    #         EC.visibility_of_element_located((By.XPATH, "//p[@data-placeholder='Ask anything']"))
    #     )
    #     input_element.send_keys(query)
    #     sleep(1)
    #     input_element.send_keys(Keys.ENTER)
    #     sleep(1)
    #     WebDriverWait(self.driver, 2000).until(
    #         EC.invisibility_of_element_located((By.ID, "composer-submit-button"))
    #     )
    #     inputElements = WebDriverWait(self.driver, 20).until(
    #         EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='whitespace-pre-wrap' and normalize-space(.)='" + query + "']/following::p[@data-start]"))
    #     )
    #     results = []
    #     for element in inputElements:
    #         results.append(element.text)
    #     # self.driver.quit()
    #     return(results)

    def generate_image(self,query):
        self.driver.get("https://www.chatgpt.com")
        try:
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
            sleep(3)
            inputElements = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH,
                                                       "//div[@class='whitespace-pre-wrap' and normalize-space(.)='" + query + "']/following::img[@class='absolute top-0 z-1 w-full']"))
            )

            src_value = inputElements.get_attribute("src")

            # results = []
            # for element in inputElements:
            #     results.append(element.text)
            # self.driver.quit()
            return (src_value)
        except ElementNotInteractableException:
            login_prompt = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='flex items-center justify-center' and text()='Log in']"))
            )
            print(login_prompt)
            if login_prompt:
                self.set_cookie()
                return self.generate_image(query)
            else:
                return None

    def sora_image_create(self,query):
        self.driver.get("https://sora.chatgpt.com/explore/images")
        input_element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//textarea"))
        )
        input_element.send_keys(query)
        sleep(1)
        input_element.send_keys(Keys.ENTER)
        sleep(3)
        element = self.driver.find_element(By.XPATH, "//div[text()='My media']")
        element.click()
        try:
            sleep(3)
            WebDriverWait(self.driver, 2000).until(
                EC.invisibility_of_element((By.CSS_SELECTOR, 'circle.origin-center.transition-\\[stroke-dashoffset\\]'))
            )
            elements = self.driver.find_elements(By.XPATH,
                                            '//div[div[text()="'+query+'"]]/preceding-sibling::div[1]//a')
            if elements:
                elements[0].click()

            sleep(1)
            image = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//img[@alt='Generated image']"))
            )
            img_url = image.get_attribute("src")

            return img_url
        except TimeoutException:
            print(f"Alternative approach timeout")
            return False
        except ElementNotInteractableException:
            login_prompt = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='flex items-center justify-center' and text()='Log in']"))
            )
            print(login_prompt)
            if login_prompt:
                self.set_cookie()
                return self.sora_image_create(query)
            else:
                return None
        except Exception as e:
            print(f"Alternative approach error: {e}")
            return False





