import json
from pathlib import Path
from requests.models import Response
import gzip
import brotli
import brotli_file

import process_cache
import request_adapter
import navigate

# `cwd`: current directory is straightforward (assumes this file location is in root directory)
project_root = Path.cwd()

# Next create the full path to chrome driver
chrome_driver_location = (project_root / 'drivers/chromedriver.exe').resolve()

if __name__ == '__main__':
    # navigate.navigate_site()
    process_cache.process_cache_files()

