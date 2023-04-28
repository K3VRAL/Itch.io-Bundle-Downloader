# List of valid urls to be processed and requested corrected

import urllib.parse
import json
import os
import re
import sys

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
            filename = "{}/{}/{}/{}".format(setup.args.folder, re.sub("/", "_", bundle), re.sub("/", "_", game), re.sub("/", "_", upload))
            length = r.headers["Content-Length"]

            download.downloadFile(r, length, filename, response_parsed.hostname)
        elif response_parsed.hostname in [ "drive.google.com" ]:
            url_split = response_url.split("/")
            if url_split[3] == "file" and url_split[4] == "d":
                id = url_split[5]

                r_url = "https://drive.google.com/uc"
                params = { "id": id, "export": "download", "confirm": "t" }
                r_getLocation = reqretry.post(r_url, params = params, allow_redirects = False)

                r = reqretry.get(r_getLocation.headers["Location"], stream = True)
                filename = "{}/{}/{}/{}".format(setup.args.folder, re.sub("/", "_", bundle), re.sub("/", "_", game), re.sub("/", "_", upload))
                length = r.headers["Content-Length"]

                download.downloadFile(r, length, filename, response_parsed.hostname)
        elif response_parsed.hostname in [ "docs.google.com" ]:
            error.write("Support for download in development - Upload[{}] ID[{}] URL[{}] ResponseURL[{}] Game[{}]".format(upload, setup.data[bundle]["games"][game]["uploads"][upload], url, response_url, game))
        elif response_parsed.hostname in [ "www.amazon.com" ]:
            error.write("Please check to see if this link is downloadable (some links are redirections to webpages for the purchase of products) - Upload[{}] ID[{}] URL[{}] ResponseURL[{}] Game[{}]".format(upload, setup.data[bundle]["games"][game]["uploads"][upload], url, response_url, game))
        else:
            error.write("Support for download not found - Upload[{}] ID[{}] URL[{}] ResponseURL[{}] Game[{}]".format(upload, setup.data[bundle]["games"][game]["uploads"][upload], url, response_url, game))
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()

        fileError = exc_traceback.tb_frame.f_code.co_filename
        lineError = exc_traceback.tb_lineno
        executionError = exc_value
        error.write("Something went wrong in the code - File[{}] Line[{}] Error[{}] - Upload[{}] ID[{}] URL[{}] Game[{}]".format(fileError, lineError, executionError, upload, setup.data[bundle]["games"][game]["uploads"][upload], url, game))
