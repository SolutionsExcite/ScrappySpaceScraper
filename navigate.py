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


def navigate_ship(driver, ship_id):
    ship_url = stfc_base_url + ship_id

    # load unique ship page.  Selector looks for when tier data is loaded
    css_loaded_selector = 'td.text-center.px-2.py-2.text-sm.tabular-nums'
    soup = get_soup(driver, ship_url, css_loaded_selector)
    return soup


def navigate_ships(driver):
    # Base ships url to loop through pages
    ship_query_string = 'ships?f=$name=%26faction:-1%26igrade:-1%26irarity:-1%26' \
                        'page:{current_page}&s=$ascending:true%26sortBy:0'
    ships_url = stfc_base_url + ship_query_string.format(current_page=1)

    # CSS selector of element with data-attr whose value is async loaded
    css_loaded_selector = 'a[href^="/ships/"] '

    # get soup, so we start paging and grabbing all the ship ID's
    soup = get_soup(driver, ships_url, css_loaded_selector)

    # Get visible number of pages
    css_pages_selector = 'nav a.bg-white'
    page_tags = soup.select(css_pages_selector)

    # Map to get string. Filter for only numbers.  Place in set to ensure unique values
    pages = list(set(map(lambda x: x.string, page_tags)))
    pages.remove(None)
    pages.sort()

    # Loop over each page scanning all ships on page
    for page in pages:
        if page != 1:
            ships_url = stfc_base_url + ship_query_string.format(current_page=page)
            # load page
            soup = get_soup(driver, ships_url, css_loaded_selector)

        # Grab anchor with href storing specific ship url
        ship_tags = soup.select(css_loaded_selector)
        for ship_tag in ship_tags:
            # select value of href (string). [1:] takes the string and returns characters skipping first character
            navigate_ship(driver, ship_tag['href'][1:])


def navigate_officers(driver):
    # Base ships url to loop through pages
    officer_query_string = '/officers?f=$name=%26sg:-1%26rarity:-1%26' \
                           'page:{current_page}&s=$ascending:true%26sortBy:0'
    officers_url = stfc_base_url + officer_query_string.format(current_page=1)

    # CSS selector of element with data-attr whose value is async loaded
    css_loaded_selector = 'a[href^="/officers/"] '

    # get soup, so we start paging and grabbing all the ship ID's
    soup = get_soup(driver, officers_url, css_loaded_selector)

    # Get visible number of pages
    css_pages_selector = 'nav a.bg-white'
    page_tags = soup.select(css_pages_selector)

    # Map to get string. Filter for only numbers.  Place in set to ensure unique values
    pages = list(set(map(lambda x: x.string, page_tags)))
    pages.remove(None)
    pages.sort()

    # Loop over each page scanning all ships on page
    for page in pages:
        if page != 1:
            officers_url = stfc_base_url + officer_query_string.format(current_page=page)
            # load page
            soup = get_soup(driver, officers_url, css_loaded_selector)

        # Grab anchor with href storing specific ship url
        officer_tags = soup.select(css_loaded_selector)
        for ship_tag in officer_tags:
            # select value of href (string). [1:] takes the string and returns characters skipping first character
            navigate_ship(driver, ship_tag['href'][1:])


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


def navigate_sections(driver):
    # Navigate ships section
    query_string = 'ships?f=$name=%26faction:-1%26igrade:-1%26irarity:-1%26' \
                        'page:{current_page}&s=$ascending:true%26sortBy:0'
    # CSS selector of element with data-attr whose value is async loaded for page
    css_page_loaded_selector = 'a[href^="/ships/"] '
    # CSS selector of element with classes
    css_item_loaded_selector = 'td.text-center.px-2.py-2.text-sm.tabular-nums'
    navigate_section_pages(driver, query_string, css_page_loaded_selector, css_item_loaded_selector)
    # navigate_ships(driver)


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
    chrome_options.add_argument("user-data-dir=C:/Users/lenha/AppData/Local/Google/Chrome/"
                                "User Data/ScrappySpaceScraper")

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options,
                              chrome_options=chrome_options)

    navigate_sections(driver)


