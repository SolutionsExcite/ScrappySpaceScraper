from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_soup(driver, url, css_selector):
    # load the url into selenium
    driver.get(url)

    # Wait until async elements are loaded utilizing data-attr whose value is async
    element = WebDriverWait(driver=driver, timeout=7).until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR, css_selector))
    )
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup


def navigate_ships(driver):
    # Base ships url to loop through pages
    ships_url = 'https://stfc.space/ships?f=$name=%26faction:-1%26igrade:-1%26irarity:-1%26' \
                'page:1' \
                '&s=$ascending:true%26sortBy:0'

    # CSS selector of element with data-attr whose value is async loaded
    css_loaded_selector = 'a[href^="/ships/"] '

    # get soup, so we start paging and grabbing all the ship ID's
    soup = get_soup(driver, ships_url, css_loaded_selector)
    # print(soup.prettify())

    # Grab anchor with href storing specific ship url


def navigate_sections(driver):
    navigate_ships(driver)


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

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options,
                              chrome_options=chrome_options)

    navigate_sections(driver)


