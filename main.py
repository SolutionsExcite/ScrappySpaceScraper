from parsel import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# from seleniumwire import webdriver
# from seleniumwire.webdriver.chrome.options import Options
from pathlib import Path

# `cwd`: current directory is straightforward (assumes this file location is in root directory)
project_root = Path.cwd()

# Next create the full path to chrome driver
chrome_driver_location = (project_root / 'drivers/chromedriver.exe').resolve()

if __name__ == '__main__':

    # configure webdriver
    options = Options()
    options.headless = True  # hide GUI
    options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
    options.add_argument("start-maximized")  # ensure window is full-screen

    # configure chrome browser to not load images and javascript
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
        # this will disable image loading
        "prefs", {"profile.managed_default_content_settings.images": 2}
    )

    # Go to home page initially in case it sets session data there
    space_url = 'https://stfc.space/ships'

    # Create a new instance of the Chrome driver
    # driver = webdriver.Chrome(executable_path=chrome_driver_location, options=options, chrome_options=chrome_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options,
                              chrome_options=chrome_options)

    # stfc.space
    driver.get(space_url)

    # wait for page to load
    # waiting for: <span class="truncate font-bold">AMALGAM</span>
    element = WebDriverWait(driver=driver, timeout=5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'truncate'))
    )
    print(driver.page_source)

    # Access requests via the `requests` attribute
    # for request in driver.requests:
    #     if request.response:
    #         print(
    #             request.url,
    #             request.response.status_code,
    #             request.response.headers['Content-Type']
    #         )





