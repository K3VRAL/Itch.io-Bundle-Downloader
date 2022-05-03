# This gets the necessary login cookies before we can start downloading games

import requests
import bs4

import setup

# Getting the login cookie
def login(name, pass_):
    r = requests.get("https://itch.io/", headers = setup.headers)

    # We need the csrf token before we can do anything
    csrf_token_cookie = None
    csrf_token_payload = None
    try:
        csrf_token_cookie = r.cookies["itchio_token"]
        csrf_token_payload = bs4.BeautifulSoup(r.text, "html.parser").find("meta", attrs = { "name": "csrf_token" })["value"]
    except:
        setup.cookies = None
        setup.csrf = None
        return

    # Necessary login information
    login_payload = {
        "csrf_token": csrf_token_payload,
        "username": name,
        "password": pass_
    }

    # This will be important to access the site to gain data from the user
    login_cookie = {
        "itchio_token": csrf_token_cookie,
        "ref:register:referrer": "https://itch.io/"
    }

    # Adding the user token to login_cookie for future use
    try:
        r = requests.post("https://itch.io/login", headers = setup.headers, cookies = login_cookie, data = login_payload)
        login_cookie["itchio"] = r.cookies["itchio"]
    except:
        setup.cookies = None
        setup.csrf = None
        return

    setup.cookies = login_cookie
    setup.csrf = csrf_token_payload