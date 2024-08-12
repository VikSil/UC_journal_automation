from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import time


class Browser:
    browser, service = None, None

    def __init__(self, driver: str):
        self.service = Service(driver)
        self.browser = webdriver.Chrome(service=self.service)

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
