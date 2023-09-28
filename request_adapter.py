import os
import brotli
import requests
from requests_testadapter import Resp

# holy sweet wow the file has been identified as 	WebView cache data	application/octet-stream


class LocalFileAdapter(requests.adapters.HTTPAdapter):
    def build_response_from_file(self, request):
        file_path = request.url[7:]

        with open(file_path, encoding='utf-8-sig', errors='ignore') as f:
            lines = f.readlines()
            data = lines[0]

        with open(file_path, 'rb') as file:
            buff = bytearray(os.path.getsize(file_path))
            file.readinto(buff)
            resp = Resp(buff)
            r = self.build_response(request, resp)

            data = brotli.decompress(r.content)

            return r

    def send(self, request, stream=False, timeout=None,
             verify=True, cert=None, proxies=None):

        return self.build_response_from_file(request)


def get_local_file(file_path):
    file_path = 'file://C:/Users/lenha/Desktop/8a57d9228b65c8e9_0'
    requests_session = requests.session()
    requests_session.mount('file://', LocalFileAdapter())
    requests_session.get(file_path)
    print('')

