import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


FIREFOX_PATH = r"C:\Program Files\Mozilla Firefox\firefox.exe"


class BrowserFactory:
    @staticmethod
    def create_browser(browser_name):
        if browser_name == "chrome":
            options = ChromeOptions()
            return webdriver.Chrome(options=options)

        if browser_name == "firefox":
            options = FirefoxOptions()
            if os.path.exists(FIREFOX_PATH):
                options.binary_location = FIREFOX_PATH
            return webdriver.Firefox(options=options)

        raise ValueError(f"Неизвестный браузер: {browser_name}")
