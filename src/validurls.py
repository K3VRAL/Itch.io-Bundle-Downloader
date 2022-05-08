# List of valid urls to be processed and requested corrected

import urllib.parse
import json
import os
import re

import reqretry
import setup
import download
import error

def checking(r, bundle, game, upload, url):
    try:
        response_url = json.loads(r.text)["url"]
        response_parsed = urllib.parse.urlparse(response_url)

        if response_parsed.hostname in [ "w3g3a5v6.ssl.hwcdn.net", "www.oddwarg.com", "study-japanese.net" ]:
            r = reqretry.get(response_url, stream = True)
            filename = "{}/downloaded/{}/{}/{}".format(os.getcwd(), re.sub("/", "_", bundle), re.sub("/", "_", game), re.sub("/", "_", upload))
            length = r.headers["Content-Length"]

            download.downloadFile(r, length, filename, "w3g3a5v6_ssl_hwcdn_net")
        elif response_parsed.hostname in [ "drive.google.com", "docs.google.com", "www.amazon.com" ]: # TODO
            error.write("Support in development - Upload[{}] ID[{}] URL[{}] ResponseURL[{}] Game[{}]".format(upload, setup.data[bundle]["games"][game]["uploads"][upload], url, response_url, game))
        else:
            error.write("Download is currently not supported - Upload[{}] ID[{}] URL[{}] ResponseURL[{}] Game[{}]".format(upload, setup.data[bundle]["games"][game]["uploads"][upload], url, response_url, game))
    except:
        error.write("Posted or recieved incorrectly, or something went wrong in the code - Upload[{}] ID[{}] URL[{}] Game[{}]".format(upload, setup.data[bundle]["games"][game]["uploads"][upload], url, game))