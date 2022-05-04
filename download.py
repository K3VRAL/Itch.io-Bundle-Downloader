import bs4
import requests
import json
import sys
import threading
import os
import re
import datetime

debug = False
def dprint(printing):
    if debug:
        print("[DEBUG] " + printing)

def downloadGames(inp, allGames):
    path = os.getcwd() + "/" + inp
    if not os.path.isdir(path):
        os.mkdir(path)
        dprint("Created path for downloads: " + path)
    else:
        dprint("Path for downloads already exists: " + path)
    lookatPath = path + "/Lookat.TODO"
    if not os.path.isfile(lookatPath):
        open(lookatPath, "w").close()
        dprint("Created path for items to be downloaded at a later time (as it cannot be downloaded now): " + lookatPath)
    else:
        dprint("Path for items to be downloaded at a later time (as it cannot be downloaded now) already exists: " + lookatPath)
    f = open(lookatPath, "a")
    f.write("-" * 10)
    f.write(str(datetime.datetime.now()))
    f.write("-" * 10)
    f.write("\n")
    f.close()
    for i in allGames:
        pathitem = path + "/" + i[0].replace("/", "_")
        if not os.path.isdir(pathitem):
            os.mkdir(pathitem)
            dprint("Created pathitem: " + pathitem)
        else:
            dprint("pathitem already exists: " + pathitem)
        for j in range(1, len(i)):
            if "lookatUrl" in i[j] and "lookatPost" in i[j]:
                dprint("Appended to be looked at: " + lookatPath)
                f = open(lookatPath, "a")
                for k in i[j].keys():
                    f.write(k + " " + str(i[j][k]) + " ")
                    dprint("Look at: " + k + " - " + str(i[j][k]))
                f.write("\n")
                f.close()
            else:
                dprint("Downloading item: " + i[j] + " " + j)
                response = requests.post(i[j]["url"], params = i[j]["params"], data = i[j]["data"], cookies = i[j]["cookies"])
                filename = json.loads(response.text)["url"].rsplit("/", 1)[1].replace("/", "_").rsplit("?", 1)[0]
                dprint("Current filename: " + filename)
                if json.loads(response.text)["url"].split("/")[2] == "w3g3a5v6.ssl.hwcdn.net":
                    response = requests.get(json.loads(response.text)["url"], stream = True)
                    dprint("Response: " + str(response))
                    dprint("Text: " + response.text)
                    dprint("Does `Content-Disposition` exists?: " + str("Content-Disposition" in response.headers))
                    if "Content-Disposition" in response.headers:
                        refind = re.findall("filename=(.+)", response.headers["content-disposition"])[0]
                        filename = i[j]["url"].rsplit("/", 1)[len(i[j]["url"].rsplit("/", 1))-1] + "_" + refind[1:len(refind)-1].replace("/", "_")
                        dprint("filename changed: " + filename)
                length = response.headers.get("content-length")
                dprint("Current length to be downloaded: " + length)
                print("Downloading " + i[0] + ": " + filename)
                with open(pathitem + "/" + filename, "wb") as file:
                    if length is None:
                        file.write(response.content)
                    else:
                        dl = 0
                        length = int(length)
                        for data in response.iter_content(chunk_size=4096):
                            dl += len(data)
                            file.write(data)
                            done = int(50 * dl / length)
                            sys.stdout.write("\r[%s%s] " % ('=' * done, ' ' * (50-done)) + str(dl) + " of " + str(length))    
                            sys.stdout.flush()
                    file.close()
                print("")

def listingGames(inp, url, posting, item, reqData):
    gameList = [ item ]
    gamesUploaded = []
    urlPost = ""
    paramPost = {}
    cookiesPost = {}
    csfrToken = {}
    if not posting:
        dataGet = requests.get(reqData)
        dprint("GET: " + str(dataGet))
        dprint("Text: " + dataGet.text)
        urlPost = reqData.rsplit("/", 2)[0]
        paramPost = { "source": "game_download", "key": reqData.split("/")[5] }
        cookiesPost = dataGet.cookies
        csfrToken = { "csrf_token": bs4.BeautifulSoup(dataGet.text, "html.parser").find("meta", attrs = { "name": "csrf_token" })["value"] }
        gamesUploaded = bs4.BeautifulSoup(dataGet.text, "html.parser").find("div", class_ = "upload_list_widget").find_all(class_ = "upload")
    else:
        dataPost = requests.post(url, data = reqData[0], cookies = reqData[1])
        dprint("POST: " + str(dataPost))
        dprint("Text: " + dataPost.text)
        urlPost = url.rsplit("/", 2)[0]
        paramPost = { "source": "game_download", "key": url.split("/")[5] }
        cookiesPost = dataPost.cookies
        csfrToken = { "csrf_token": bs4.BeautifulSoup(dataPost.text, "html.parser").find("meta", attrs = { "name": "csrf_token" })["value"] }
        gamesUploaded = bs4.BeautifulSoup(dataPost.text, "html.parser").find("div", class_ = "upload_list_widget").find_all(class_ = "upload")
    if not (os.path.isdir(os.getcwd() + "/" + inp + "/" + gameList[0].replace("/", "_") + "/") and len(gamesUploaded) == len(os.listdir(os.getcwd() + "/" + inp + "/" + gameList[0].replace("/", "_") + "/"))):
        for game in range(0, len(gamesUploaded)):
            try:
                uploadId = gamesUploaded[game].find("a")["data-upload_id"]
                gameList.append({ "url": urlPost + "/file/" + uploadId, "params": paramPost, "data": csfrToken, "cookies": cookiesPost })
                print(gameList[0] + " =>", gameList[len(gameList)-1]["url"])
            except TypeError:
                gameList.append({ "lookatUrl": url, "lookatPost": urlPost, "id": (game + 1) })
                print(gameList[0] + " => Look At " + str(game))
        return gameList
    else:
        print(gameList[0] + " =# Has already been downloaded")
        return None

def main():
    dprint("Debugging enabled")
    print("Please input bundle from itch.io (only the id of the url, not with the actual)")
    inp = input()
    url = "https://itch.io/bundle/download/" + inp
    r = requests.get(url)
    dprint(url + ": " + str(r))
    if r.ok and r.status_code == 200:
        allGamesId = []
        pages = int(bs4.BeautifulSoup(r.text, "html.parser").find("span", class_ = "pager_label").a.get_text())
        dprint("Number of pages in " + url + ": " + str(pages))
        for i in range(1, pages + 1):
            print("PAGE: {} of {}".format(i, pages))
            r = requests.get(url + "?page=" + str(i))
            dprint(url + "?page=" + str(i) + " : " + str(r))
            if r.ok and r.status_code == 200:
                findingSoup = bs4.BeautifulSoup(r.text, "html.parser").find("div", class_ = "game_list").find_all(class_ = "game_row")
                dprint("List of games: " + str(findingSoup))
                for gamesList in findingSoup:
                    findingDownload = gamesList.find("a", class_ = "game_download_btn")
                    if findingDownload != None:
                        # get
                        dprint("Game has been claimed - GET: " + gamesList.find("h2", class_ = "game_title").get_text())
                        listingG = listingGames(inp, url, False, gamesList.find("h2", class_ = "game_title").get_text(), findingDownload["href"])
                        dprint("Appending if listingG is True: " + str(not listingG == None))
                        if not listingG == None:
                            allGamesId.append(listingG)
                        continue
                    
                    findingDownload = gamesList.find("form", class_ = "form")
                    if findingDownload != None:
                        # post
                        dprint("Game has NOT been claimed - POST: " + url)
                        inpFinding = findingDownload.find_all("input")
                        butFinding = findingDownload.find("button", class_ = "button")
                        listingG = listingGames(inp, url, True, gamesList.find("a")["href"], [{ inpFinding[0]["name"]: inpFinding[0]["value"], inpFinding[1]["name"]: inpFinding[1]["value"], butFinding["name"]: butFinding["value"] }, r.cookies])
                        dprint("Appending if listingG is True: " + str(not listingG == None))
                        if not listingG == None:
                            allGamesId.append(listingG)
                        continue
                        
                    print("FAILED")
                    sys.exit(1)
            else:
                print("ERROR")
        dprint("Finally downloading the games: " + str(allGamesId))
        downloadGames(inp, allGamesId)
        print("FINISHED!")
    else:
        print("FAILED TO GET BUNDLE")

if __name__ == "__main__":
    for x in sys.argv:
        if x == "-d":
            debug = True
    main()
