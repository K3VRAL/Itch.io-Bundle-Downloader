# This starts to map the items and their games

import requests
import bs4
import sys

import setup
import download

# TODO do without user login (maybe make a "nouser.py" file).
# Right now, I am unable to really test this out so I'll have to put this in the backburner until I find a bundle worth investing not tied to my main account

def uploadGames(bundle, name):
    r = requests.get(setup.data[bundle]["games"][name]["url"], headers = setup.headers, cookies = setup.cookies)

    uploads = bs4.BeautifulSoup(r.text, "html.parser").find("div", class_ = "upload_list_widget").find_all("div", class_ = "upload")
    for upload in uploads:
        upload_name = upload.find("strong", class_ = "name").get_text()
        upload_id = upload.find("a", class_ = "button download_btn")["data-upload_id"]
        setup.data[bundle]["games"][name]["uploads"][upload_name] = upload_id

def mapGames():
    print("Getting all items from each bundle")
    bundles = setup.data.keys()
    bundle_i = 0
    for bundle in bundles:
        bundle_i += 1
        print("-Looking at Bundle [{}] | [{}/{}]".format(bundle, bundle_i, len(bundles)))
        pages = setup.data[bundle]["pages"]
        for page in range(1, 2):# pages + 1): # TODO
            print("--Looking at Page [{}/{}]".format(page, pages))
            r = requests.get("https://itch.io{}?page={}".format(setup.data[bundle]["link"], page), headers = setup.headers, cookies = setup.cookies)
            
            games = bs4.BeautifulSoup(r.text, "html.parser").find("div", class_ = "game_list").find_all("div", class_ = "game_row")
            game_i = 0
            for game in games:
                game_i += 1
                print("---Looking at Items [{}/{}]".format(game_i, len(games)))
                # Claimed item/REST: GET
                findingDownload = game.find("a", class_ = "game_download_btn")
                if findingDownload != None:
                    name = game.find("h2", class_ = "game_title").a.get_text()
                    url = findingDownload["href"]
                    setup.data[bundle]["games"][name] = { "url": url, "uploads": {}}
                    uploadGames(bundle, name)
                    continue

                # Not Claimed item/REST: POST
                # TODO Look more into this (get another bundle to do more testing)
                findingDownload = game.find("form", class_ = "form")
                if findingDownload != None:
                    print("NOT CLAIMED")
                    continue

                # All Else Fails
                print("!!!\n{}\n!!!".format(game))
                print("An error has occurred when trying to find game download link. Please post the above into the `Issues` in GitHub ({}) so this can be resolved. Exitting...".format("https://github.com/K3VRAL/Itch.io-Bundle-Downloader/issues"))
                sys.exit(1)

def mapPages():
    print("Getting pages from all bundles")
    bundles = setup.data.keys()
    for bundle in bundles:
        r = requests.get("https://itch.io{}".format(setup.data[bundle]["link"]), headers = setup.headers, cookies = setup.cookies)

        page = int(bs4.BeautifulSoup(r.text, "html.parser").find("span", class_ = "pager_label").a.get_text())
        print("-Found [{}] Pages in Bundle [{}]".format(page, bundle))
        setup.data[bundle]["pages"] = page
        setup.data[bundle]["games"] = {}

def mapBundles():
    print("Getting all bundles from user")
    r = requests.get("https://itch.io/my-purchases/bundles", headers = setup.headers, cookies = setup.cookies)

    bundles = bs4.BeautifulSoup(r.text, "html.parser").find("section", class_ = "bundle_keys").find_all("li")
    for bundle in bundles:
        name = "{}".format(bundle.a.get_text())
        print("-Found Bundle [{}]".format(name))
        setup.data[name] = { "link": bundle.a["href"] }

# Starting to download bundle data
def start():
    print("Starting to map all bundles")
    mapBundles()
    mapPages()
    mapGames()