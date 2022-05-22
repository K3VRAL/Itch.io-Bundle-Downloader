# The module `requests` only sends the data once and waits to receive data back.
# Here, we just make it constantly retry until we get an answer.

import requests

import setup
import error

def get(url, cookies = "", data = "", params = "", stream = False, allow_redirects = True):
    for i in range(1, 5 + 1):
        try:
            return requests.get(url, headers = setup.headers, cookies = cookies, data = data, params = params, stream = stream, allow_redirects = allow_redirects, timeout = 5)
        except requests.exceptions.Timeout:
            error.write("Get Timed-out - NUMB[{}/5] URL[{}]".format(i, url))
    error.write("Get request timed-out and/or returned nothing (ignore error line below) - URL[{}]".format(url))

def post(url, cookies = "", data = "", params = "", stream = False, allow_redirects = True):
    for i in range(1, 5 + 1):
        try:
            return requests.post(url, headers = setup.headers, cookies = cookies, data = data, params = params, stream = stream, allow_redirects = allow_redirects, timeout = 5)
        except requests.exceptions.Timeout:
            error.write("Post Timed-out - NUMB[{}/5] URL[{}]".format(i, url))
    error.write("Post request timed-out and/or returned nothing (ignore error line below) - URL[{}]".format(url))