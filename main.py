from pathlib import Path
import request_adapter
import navigate

# `cwd`: current directory is straightforward (assumes this file location is in root directory)
project_root = Path.cwd()

# Next create the full path to chrome driver
chrome_driver_location = (project_root / 'drivers/chromedriver.exe').resolve()

if __name__ == '__main__':
    # navigate.navigate_site()
    request_adapter.get_local_file('')

