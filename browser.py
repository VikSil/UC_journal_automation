from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import time

# sudo docker run -it uc must be run for following to work
# Set these to work in server enviroment and to work in docker containerised enviroment.
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")

class Browser:
    browser, service = None, None

    def __init__(self):
        # no need to get the driver binary or correct version now.
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options)

    def open_page(self, url: str):
        self.browser.get(url)

    def close(self):
        self.browser.close()

    def add_input(self, by: By, id: str, value: str):
        field = self.browser.find_element(by=by, value=id)
        field.send_keys(value)
        time.sleep(1)

    def click_button(self, by: By, id: str):
        button = self.browser.find_element(by=by, value=id)
        button.click()
        time.sleep(1)

    def sleep(self, timeout: int):
        time.sleep(timeout)
