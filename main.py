from pathlib import Path

import navigate
import process_cache

# `cwd`: current directory is straightforward (assumes this file location is in root directory)
project_root = Path.cwd()

# Next create the full path to chrome driver
chrome_driver_location = (project_root / 'drivers/chromedriver.exe').resolve()

if __name__ == '__main__':
    # navigate.navigate_site()
    process_cache.process_cache_files()

