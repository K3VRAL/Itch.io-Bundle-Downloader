# This starts to map the items and their games

import bs4
import sys

import setup
import reqretry
import error

def mapUploads(bundle, name):
    r = reqretry.get(setup.data[bundle]["games"][name]["url"], headers = setup.headers, cookies = setup.cookies)

    uploads = bs4.BeautifulSoup(r.text, "html.parser").find("div", class_ = "upload_list_widget").find_all("div", class_ = "upload")
    for upload in uploads:
        upload_name = upload.find("strong", class_ = "name").get_text()
        try:
            upload_id = upload.find("a", class_ = "button download_btn")["data-upload_id"]
        except:
            upload_id = upload.div.get_text()
        setup.data[bundle]["games"][name]["uploads"][upload_name] = upload_id

def mapGames():
    print("Getting all items from each bundle")
    bundles = setup.data.keys()
    bundle_i = 0
    for bundle in bundles:
        bundle_i += 1
        print("-[{}/{}] | Looking at Bundle [{}]".format(bundle_i, len(bundles), bundle))
        pages = setup.data[bundle]["pages"]
        for page in range(1, pages + 1):
            print("--[{}/{}] | Looking at Page".format(page, pages))
            r = reqretry.get("https://itch.io{}?page={}".format(setup.data[bundle]["link"], page), headers = setup.headers, cookies = setup.cookies)
            
            games = bs4.BeautifulSoup(r.text, "html.parser").find("div", class_ = "game_list").find_all("div", class_ = "game_row")
            game_i = 0
            for game in games:
                game_i += 1
                print("---[{}/{}] | Looking at Items - ".format(game_i, len(games)), end = "")
                # Claimed item/REST: GET
                findingDownload = game.find("a", class_ = "game_download_btn")
                if findingDownload != None:
                    print("Game Claimed")
                    name = game.find("h2", class_ = "game_title").a.get_text()
                    url = findingDownload["href"]
                    setup.data[bundle]["games"][name] = { "url": url, "uploads": {}}
                    mapUploads(bundle, name)
                    continue

                # Not Claimed item/REST: POST
                findingDownload = game.find("form", class_ = "form")
                if findingDownload != None:
                    print("Game Not Claimed")
                    continue

                # (Weird) View Page/REST: GET
                # This most likely has to do with disabling all the download links
                # so this will go in the error file until I see something that changes with the state
                findingDownload = game.find("a", class_ = "forward_link")
                if findingDownload != None:
                    print("Game Viewing Page")
                    name = game.find("h2", class_ = "game_title").a.get_text()
                    url = findingDownload["href"]
                    setup.data[bundle]["games"][name] = { "url": url, "uploads": {}}
                    continue

                # All Else Fails
                error.write("!!!ERROR STARTS HERE!!!")
                error.write("{}".format(game))
                error.write("!!!ERROR ENDS HERE!!!")
                print("!!!An error has occurred when trying to find game download link. It is recommended that you check out the error file to find more details. If you wish to help with the development of the script, please report this to the maintainers. REMOVE ALL THE REVEALING INFORMATION/LINKS (specifically look out for [.../download/ID]) before posting the above to the `Issues` in GitHub ({}) so this can be resolved safely!!!".format("https://github.com/K3VRAL/Itch.io-Bundle-Downloader/issues"))
                print("Exitting...")
                sys.exit(1)

def mapPages():
    print("Getting pages from all bundles")
    bundles = setup.data.keys()
    for bundle in bundles:
        r = reqretry.get("https://itch.io{}".format(setup.data[bundle]["link"]), headers = setup.headers, cookies = setup.cookies)

        page = int(bs4.BeautifulSoup(r.text, "html.parser").find("span", class_ = "pager_label").a.get_text())
        print("-Found [{}] Pages in Bundle [{}]".format(page, bundle))
        setup.data[bundle]["pages"] = page
        setup.data[bundle]["games"] = {}

def mapBundles():
    print("Getting all bundles from user")
    r = reqretry.get("https://itch.io/my-purchases/bundles", headers = setup.headers, cookies = setup.cookies)

    bundles = bs4.BeautifulSoup(r.text, "html.parser").find("section", class_ = "bundle_keys").find_all("li")
    bundle_i = 0
    for bundle in bundles:
        bundle_i += 1
        name = "{}".format(bundle.a.get_text())
        print("-[{}/{}] | Found Bundle [{}]".format(bundle_i, len(bundles), name))
        setup.data[name] = { "link": bundle.a["href"] }

# Starting to download bundle data
def start():
    print("Starting to map all bundles")
    mapBundles()
    mapPages()
    mapGames()