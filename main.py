import json
from pathlib import Path
from requests.models import Response
import gzip
import brotli
import brotli_file
import request_adapter
import navigate

# `cwd`: current directory is straightforward (assumes this file location is in root directory)
project_root = Path.cwd()

# Next create the full path to chrome driver
chrome_driver_location = (project_root / 'drivers/chromedriver.exe').resolve()

if __name__ == '__main__':
    # navigate.navigate_site()
    file_path = 'C:/Users/lenha/Desktop/27c973f293b7fc20_0'
    with open(file_path, 'rb') as f:
        line = f.readline()
        # splice out junk from beginning and end

        data = gzip.decompress(lines)
        # data = brotli.decompress(lines)

        the_response = Response()
        the_response.encoding = "br"
        the_response.apparent_encoding
        the_response.status_code = 200
        the_response._content = lines

        test = the_response.json()
        print(the_response.json())



        beginning = lines.find('h')
        lines = lines[beginning - 1:]
        arr = lines.find('[')
        obj = lines.find('{')
        beginning = obj if obj < arr else arr
        lines = lines[beginning - 1:]
        end = lines.rfind('}')
        lines = lines[:end + 1]
        print(type(lines))
        j = json.loads(lines.encode('utf8').decode('utf8'))
        print(j)
        print()

