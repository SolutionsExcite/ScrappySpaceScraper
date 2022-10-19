import time

from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


stfc_base_url = 'https://stfc.space/'


def get_soup(driver, url, css_selector):
    # load the url into selenium
    driver.get(url)

    # Wait until async elements are loaded utilizing data-attr whose value is async
    element = WebDriverWait(driver=driver, timeout=7).until(
        ec.presence_of_element_located((
            By.CSS_SELECTOR, css_selector))
    )
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup


def get_navigation_pages(soup):
    # Get visible number of pages
    css_pages_selector = 'nav a.bg-white'
    page_tags = soup.select(css_pages_selector)

    # Map to get string. Place in set to ensure unique values
    pages = list(set(map(lambda x: x.string, page_tags)))
    pages.remove(None)  # This removes anchors that are navigation arrows. they have nothing in tag.string

    # Create a list from 1...max
    max_val = int(max(pages))
    pages = [i for i in range(1, max_val + 1)]

    return pages


def navigate_section_page_item(driver, item_id, css_item_loaded_selector):
    item_url = stfc_base_url + item_id

    # load unique item page.
    soup = get_soup(driver, item_url, css_item_loaded_selector)
    return soup


def navigate_section_pages(driver, query_string, css_page_loaded_selector, css_item_loaded_selector):
    # First page in section of url to loop through pages
    section_url = stfc_base_url + query_string.format(current_page=1)

    # get soup, so we start paging and grabbing all the ship ID's
    soup = get_soup(driver, section_url, css_page_loaded_selector)

    # Get a list of pages from 1...n
    pages = get_navigation_pages(soup)

    # Loop over each page scanning all ships on page
    for page in pages:
        if page != 1:
            section_url = stfc_base_url + query_string.format(current_page=page)
            # load page
            soup = get_soup(driver, section_url, css_page_loaded_selector)

        # Grab anchor with href storing specific ship url
        item_tags = soup.select(css_page_loaded_selector)
        for item_tag in item_tags:
            # select value of href (string). [1:] takes the string and returns characters skipping first character
            navigate_section_page_item(driver, item_tag['href'][1:], css_item_loaded_selector)


def navigate_systems_section(driver):
    # Navigate ships section
    query_string = 'systems?f=$name=%26warp:-1%26mining:false%26housing:false%26' \
                   'missions:false%26minLevel:1%26maxLevel:60%26minWarp:1%26' \
                   'maxWarp:600%26resources@;%26hostiles@;%26he:false%26me:false%26faction:-1%26' \
                   'page:{current_page}%26scout:false%26ns:0&s=$ascending:true%26sortBy:1'

    # CSS selector of element with data-attr whose value is async loaded for page
    css_page_loaded_selector = 'a[href^="/systems/"]'

    # CSS selector of element with classes
    css_item_loaded_selector = 'span.font-bold.text-xl'
    navigate_section_pages(driver, query_string, css_page_loaded_selector, css_item_loaded_selector)


def navigate_ships_section(driver):
    # Navigate ships section
    query_string = 'ships?f=$name=%26faction:-1%26igrade:-1%26irarity:-1%26' \
                   'page:{current_page}&s=$ascending:true%26sortBy:0'

    # CSS selector of element with data-attr whose value is async loaded for page
    css_page_loaded_selector = 'a[href^="/ships/"]'

    # CSS selector of element with classes
    css_item_loaded_selector = 'td.text-center.px-2.py-2.text-sm.tabular-nums'
    navigate_section_pages(driver, query_string, css_page_loaded_selector, css_item_loaded_selector)


def navigate_officers_section(driver):
    # Navigate ships section
    query_string = 'officers?f=$name=%26sg:-1%26rarity:-1%26' \
                           'page:{current_page}&s=$ascending:true%26sortBy:0'

    # CSS selector of element with data-attr whose value is async loaded for page
    css_page_loaded_selector = 'a[href^="/officers/"]'

    # CSS selector of element with classes
    css_item_loaded_selector = 'td.text-right.px-1.py-2.text-sm.tabular-nums'
    navigate_section_pages(driver, query_string, css_page_loaded_selector, css_item_loaded_selector)


def navigate_hostiles_section(driver):
    # Navigate ships section
    query_string = 'hostiles?f=$name=%26level:0%26types@;%26uself:false%26minWarp:1%26maxWarp:600%26faction:-1%26' \
                   'page:{current_page}&s=$ascending:true%26sortBy:0'

    # CSS selector of element with data-attr whose value is async loaded for page
    css_page_loaded_selector = 'a[href^="/hostiles/"]'

    # CSS selector of element with classes
    css_item_loaded_selector = 'h4.font-bold.pb-2.mb-auto'
    navigate_section_pages(driver, query_string, css_page_loaded_selector, css_item_loaded_selector)


def navigate_sections(driver):
    # Comment out code to test individual
    # Each method utilized below relates to a screen on stfc
    navigate_officers_section(driver)
    # navigate_ships_section(driver)
    # navigate_hostiles_section(driver)
    # navigate_systems_section(driver)


# figure out why driver is not loading with https
def navigate_site():
    # configure webdriver
    options = Options()
    options.headless = True  # hide GUI
    options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
    options.add_argument("start-maximized")  # ensure window is full-screen

    # configure Chrome browser to not load images and javascript
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
        # this will disable image loading
        "prefs", {"profile.managed_default_content_settings.images": 2}
    )
    # This is the file path that chrome driver will utilize as if it were the native app data folder.
    # This can be changed to anywhere.  Desktop or Documents may be a good first location.
    chrome_options.add_argument("user-data-dir=C:/Users/lenha/AppData/Local/Google/Chrome/"
                                "User Data/ScrappySpaceScraper")

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options,
                              chrome_options=chrome_options)

    time.sleep(5)

    navigate_sections(driver)
