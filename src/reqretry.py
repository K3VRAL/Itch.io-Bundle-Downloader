# The module `requests` only sends the data once and waits to receive data back.
# Here, we just make it constantly retry until we get an answer.

import requests

def get(url, headers = "", cookies = "", data = "", params = "", stream = False):
    r = None
    while r == None:
        try:
            r = requests.get(url, headers = headers, cookies = cookies, data = data, params = params, stream = stream, timeout = 5)
        except requests.exceptions.Timeout:
            r = None
    return r

def post(url, headers = "", cookies = "", data = "", params = "", stream = False):
    r = None
    while r == None:
        try:
            r = requests.post(url, headers = headers, cookies = cookies, data = data, params = params, stream = stream, timeout = 5)
        except requests.exceptions.Timeout:
            r = None
    return r