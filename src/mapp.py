# This starts to map the items and their games
from slugify import slugify
import bs4
import sys
import os
import re

import setup
import reqretry
import error
import valid
import make

def mapUploads(bundle, name):
    r = reqretry.get(setup.data[bundle]["games"][name]["url"], cookies = setup.cookies)

    uploads = bs4.BeautifulSoup(r.text, "html.parser").find("div", class_ = "upload_list_widget").find_all("div", class_ = "upload")
    upload_i = 0
    for upload in uploads:
        upload_i += 1
        upload_name = upload.find("strong", class_ = "name").get_text()
        print("----[{}/{}] | Looking at Upload [{}] - ".format(upload_i, len(uploads), upload_name), end = "")
        try:
            upload_id = upload.find("a", class_ = "button download_btn")["data-upload_id"]
        except:
            upload_id = upload.div.get_text()

        filename = "{}/downloaded/{}/{}/{}".format(setup.args.folder, re.sub("/", "_", bundle), re.sub("/", "_", name), re.sub("/", "_", upload_name))
        if not os.path.isfile(filename):
            setup.data[bundle]["games"][name]["uploads"][upload_name] = upload_id
            print("Adding to queue")
        else:
            print("Already downloaded")
    if len(setup.data[bundle]["games"][name]["uploads"]) == 0:
        del setup.data[bundle]["games"][name]


def mapGames():
    print("Getting all items from each bundle")
    bundles = setup.data.keys()
    bundle_i = 0
    for bundle in bundles:
        bundle_i += 1
        print("-[{}/{}] | Looking at Bundle [{}]".format(bundle_i, len(bundles), bundle))
        pages = setup.data[bundle]["pages"]
        for page in range(pages + 1):
            print("--[{}/{}] | Looking at Page".format(page, pages))
            r = reqretry.get("https://itch.io{}?page={}".format(setup.data[bundle]["link"], page), cookies = setup.cookies)
            
            games = bs4.BeautifulSoup(r.text, "html.parser").find("div", class_ = "game_list").find_all("div", class_ = "game_row")
            game_i = 0
            for game in games:
                game_i += 1
                print("---[{}/{}] | Looking at Items - ".format(game_i, len(games)), end = "")
                # Claimed item/REST: GET
                findingDownload = game.find("a", class_ = "game_download_btn")
                if findingDownload != None:
                    print("Game Claimed")
                    name = slugify(game.find("h2", class_ = "game_title").a.get_text())
                    url = findingDownload["href"]
                    setup.data[bundle]["games"][name] = { "url": url, "uploads": {}, "processed": False}
                    mapUploads(bundle, name)
                    continue

                # Not Claimed item/REST: POST
                findingDownload = game.find("form", class_ = "form")
                if findingDownload != None:
                    print("Game Not Claimed")
                    error.write("\"Game not claimed\" is currently under development - Page[{}/{}] Games[{}/{}] Bundle[{}] Game[{}] - Error[{}]".format(page, pages, game_i, len(games), bundle, name, game))
                    continue

                # (Weird) View Page/REST: GET
                # This most likely has to do with disabling all the download links
                # so this will go in the error file until I see something that changes with the state
                findingDownload = game.find("a", class_ = "forward_link")
                if findingDownload != None:
                    print("Game Viewing Page")
                    name = game.find("h2", class_ = "game_title").a.get_text()
                    url = findingDownload["href"]
                    error.write("Unable to download due to link being disabled - Page[{}/{}] Games[{}/{}] Bundle[{}] Game[{}] URL[{}]".format(page, pages, game_i, len(games), bundle, name, url))
                    continue

                # All Else Fails
                error.write("!!!ERROR!!!")
                try:
                    error.write("{}".format(game))
                except:
                    print('error!')
                error.write("!!!ERROR!!!")
                print("Game Given Error Skipping")

def mapPages():
    print("Getting pages from all bundles")
    bundles = setup.data.keys()
    for bundle in bundles:
        r = reqretry.get("https://itch.io{}".format(setup.data[bundle]["link"]), cookies = setup.cookies)

        page = int(bs4.BeautifulSoup(r.text, "html.parser").find("span", class_ = "pager_label").a.get_text())
        print("-Found [{}] Pages in Bundle [{}]".format(page, bundle))
        setup.data[bundle]["pages"] = page
        setup.data[bundle]["games"] = {}

def mapBundles():
    print("Getting all bundles from user")
    r = reqretry.get("https://itch.io/my-purchases/bundles", cookies = setup.cookies)

    bundles = bs4.BeautifulSoup(r.text, "html.parser").find("section", class_ = "bundle_keys").find_all("li")
    bundle_i = 0
    for bundle in bundles:
        bundle_i += 1
        name = "{}".format(bundle.a.get_text())
        print("-[{}/{}] | Found Bundle [{}]".format(bundle_i, len(bundles), name))
        setup.data[name] = { "link": bundle.a["href"] }
        make.makeBundleFolder(name)

# Starting to download bundle data
def start():
    print("Starting to map all bundles")
    make.makeDownloadFolder()
    mapBundles()

    try:
        print("")
        bundles = list(setup.data.keys())
        bundle_i = 0
        for bundle in bundles:
            bundle_i += 1
            print("{}: {}".format(bundle_i, bundle))
        inp = "".join(input("Which bundles do you want to exclude? (If you don't want to exclude anything, just enter in with no input) ")).split(" ")
        if not (len(inp) == 1 and inp[0] == ""):
            for i in inp:
                bundle = bundles[int(i) - 1]
                if bundle in setup.data:
                    del setup.data[bundle]
        print("")
    except:
        print("Incorrect input")
        sys.exit(1)

    bundles = list(setup.data.keys())
    if len(bundles) > 0:
        mapPages()
        mapGames()