from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time


def navigate_site():
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
    # options.add_argument("user-data-dir=C:/Users/lenha/AppData/Local/Google/Chrome/User Data/Default")
    chrome_options.add_argument("user-data-dir=C:/Users/lenha/AppData/Local/Google/Chrome/"
                                "User Data/ScrappySpaceScraper")

    # Go to home page initially in case it sets session data there
    space_url = 'https://stfc.space/ships?f=$name=%26faction:-1%26igrade:-1%26irarity:-1%26' \
                'page:1' \
                '&s=$ascending:true%26sortBy:0'

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options,
                              chrome_options=chrome_options)

    # stfc.space
    driver.get(space_url)

    # wait for page to load
    # waiting for: <span class="truncate font-bold">AMALGAM</span>
    element = WebDriverWait(driver=driver, timeout=5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'truncate.font-bold'))
    )
    time.sleep(3000)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(soup.prettify())
