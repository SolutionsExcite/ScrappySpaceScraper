from seleniumwire import webdriver

# stfc.space uses vue.js
# Need to actually use a web driver to handle running JS.  Utilize selenium WIRE package

if __name__ == '__main__':

    # Go to home page initially in case it sets session data there
    space_url = 'https://stfc.space/'

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()

    # Go to the Google home page
    driver.get(space_url)

    # Access requests via the `requests` attribute
    for request in driver.requests:
        if request.response:
            print(
                request.url,
                request.response.status_code,
                request.response.headers['Content-Type']
            )





