"""
https://web.dev/http-cache/#cache-control
https://medium.com/pixelpoint/best-practices-for-cache-control-settings-for-your-website-ff262b38c5a2
"""
import requests
from cachecontrol import CacheControl
import time

session = requests.session()
cached_session = CacheControl(session)

def send_request(host):
    start = time.time()
    cached_session.get(host)
    cached_session.get(host)
    return time.time() - start


response = send_request('http://localhost:4243')
print(response)

response = send_request('http://localhost:4243/cached')
print(response)

response = send_request('http://localhost:4243/simple_cached')
print(response)

