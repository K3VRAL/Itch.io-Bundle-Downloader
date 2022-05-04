# This starts to download all the mapped games

import urllib.parse
import re
import validators
import os
import sys

import setup
import make
import reqretry
import validurls

def w3g3a5v6_ssl_hwcdn_net(response_url, bundle, game, upload):
    r = reqretry.get(response_url, stream = True)
    filename = "{}/downloaded/{}/{}/{}".format(os.getcwd(), re.sub("/", "_", bundle), re.sub("/", "_", game), re.sub("/", "_", upload))
    length = r.headers["Content-Length"]

    file = open(filename, "wb")
    if length is None:
        file.write(r.content)
    else:
        dl = 0
        length = int(length)
        for data in r.iter_content(chunk_size = 4096):
            dl += len(data)
            file.write(data)
            done = int((dl / length) * 50)
            print("\r[{}{}{}] [{}/{}]".format("=" * done, " " * (50 - done), str(dl), str(length)), end = "")
    file.close()

def start():
    print("Starting to download all mapped bundles")
    make.makeDownloadFolder()

    bundles = setup.data.keys()
    bundle_i = 0
    for bundle in bundles:
        bundle_i += 1
        print("-[{}/{}] | Downloading Bundle [{}]".format(bundle_i, len(bundles), bundle))
        make.makeBundleFolder(bundle)

        games = setup.data[bundle]["games"].keys()
        game_i = 0
        for game in games:
            game_i += 1
            print("--[{}/{}] | Downloading Game [{}]".format(game_i, len(games), game))
            make.makeGameFolder(bundle, game)

            gameUrl = urllib.parse.urlparse(setup.data[bundle]["games"][game]["url"])
            uploads = setup.data[bundle]["games"][game]["uploads"].keys()
            if len(uploads) == 0:
                error.write("Game [{}] with URL [{}] has no uploads.".format(game, setup.data[bundle]["games"][game]["url"]))
            upload_i = 0
            for upload in uploads:
                upload_i += 1
                print("---[{}/{}] | Downloading Upload [{}]".format(upload_i, len(uploads), upload))
                
                key = gameUrl.path.split("/")[len(gameUrl.path.split("/"))-1]
                params = { "source": "game_download", "key": key }
                payload = { "csrf_token": setup.csrf }
                url = "{}://{}/{}/file/{}".format(gameUrl.scheme, gameUrl.hostname, gameUrl.path.split("/")[1], setup.data[bundle]["games"][game]["uploads"][upload])
                if not validators.url(url):
                    error.write("Game [{}] of Upload [{}] with ID [{}] has a malformed URL; URL is [{}]".format(game, upload, setup.data[bundle]["games"][game]["uploads"][upload], url))
                    continue
                r = reqretry.post(url, headers = setup.headers, cookies = setup.cookies, data = payload, params = params)
                
                validurls.checking(r, bundle, game, upload, url)