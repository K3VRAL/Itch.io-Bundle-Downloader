# List of valid urls to be processed and requested corrected

import urllib.parse
import json

import reqretry
import setup
import download
import error

def checking(r, bundle, game, upload, url):
    try:
        response_url = json.loads(r.text)["url"]
        response_parsed = urllib.parse.urlparse(response_url)
    except:
        error.write("Game [{}] of Upload [{}] with ID [{}] has posted or recieved incorrectly; URL is [{}].".format(game, upload, setup.data[bundle]["games"][game]["uploads"][upload], url))
    if response_parsed.hostname == "w3g3a5v6.ssl.hwcdn.net":
        download.w3g3a5v6_ssl_hwcdn_net(response_url, bundle, game, upload)
    else:
        error.write("Game [{}] of Upload [{}] with ID [{}] has a URL that hasn't been supported to download; URL is [{}] and Response URL is [{}].".format(game, upload, setup.data[bundle]["games"][game]["uploads"][upload], url, response_url))