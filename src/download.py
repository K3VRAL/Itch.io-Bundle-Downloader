# This starts to download all the mapped games

import urllib.parse
import validators
import sys

import setup
import make
import reqretry
import valid
import error

def downloadFile(r, length, filename, origFunction):
    if not setup.args.debug:
        file = open(filename, "wb")
        if length is None:
            file.write(r.content)
        else:
            dl = 0
            length = int(length)
            for data in r.iter_content(chunk_size = 65536):
                dl += len(data)
                file.write(data)
                done = int((dl / length) * 50)
                sys.stdout.write("\r[%s%s] [%d/%d]" % ("=" * done, " " * (50 - done), dl, length))
                sys.stdout.flush()
        print("")
        file.close()
    else:
        file = open(filename, "w")
        file.write("Hostname[{}] File_Length[{}]".format(origFunction, length))
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
            try:
                if (setup.data[bundle]["games"][game]["processed"]):
                    continue 
                else:
                    game_i += 1
                    print("--[{}/{}] | Downloading Game [{}]".format(game_i, len(games), game))
                    make.makeGameFolder(bundle, game)

                    gameUrl = urllib.parse.urlparse(setup.data[bundle]["games"][game]["url"])
                    uploads = setup.data[bundle]["games"][game]["uploads"].keys()
                    if len(uploads) == 0:
                        error.write("No Uploads - Game[{}] URL[{}]".format(game, setup.data[bundle]["games"][game]["url"]))
                    upload_i = 0
                    for upload in uploads:
                        url = "{}://{}/{}/file/{}".format(gameUrl.scheme, gameUrl.hostname, gameUrl.path.split("/")[1], setup.data[bundle]["games"][game]["uploads"][upload])
                        if not validators.url(url):
                            error.write("Malformed URL - Upload[{}] ID[{}] URL[{}] Game[{}]".format(upload, setup.data[bundle]["games"][game]["uploads"][upload], url, game))
                            continue
                        if not setup.data[bundle]["games"][game]["uploads"][upload].isdigit():
                            error.write("ID is not an integer - Upload[{}] ID[{}] Game[{}]".format(upload, setup.data[bundle]["games"][game]["uploads"][upload], game))
                            continue

                        upload_i += 1
                        print("---[{}/{}] | Downloading Upload [{}]".format(upload_i, len(uploads), upload))
                        
                        key = gameUrl.path.split("/")[len(gameUrl.path.split("/"))-1]
                        params = { "source": "game_download", "key": key }
                        payload = { "csrf_token": setup.csrf }
                        r = reqretry.post(url, cookies = setup.cookies, data = payload, params = params)
                        valid.checking(r, bundle, game, upload, url)
                    setup.data[bundle]["games"][game]["processed"] = True
            except:
                print("Error with: {}".format(game))
