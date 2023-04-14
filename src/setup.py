# This is just to set up for the global variables

import argparse
import os

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--username", help = "The input of the user's username for itch.io")
    parser.add_argument("-p", "--password", help = "The input of the user's password for itch.io")
    parser.add_argument("-f", "--folder", help = "Changes the target download folder location instead of using the current directory")
    parser.add_argument("-r", "--reprocess", help = "Ignores all cached files and their status", action = argparse.BooleanOptionalAction)        
    parser.set_defaults(reprocess = False)
    parser.add_argument("-e", "--env", help = "Have the input in a .env file and read the username and password from there", action = argparse.BooleanOptionalAction)
    parser.set_defaults(env = False)
    parser.add_argument("-d", "--debug", help = "Don't download anything, just log to error files, make files, and create files but no data", action = argparse.BooleanOptionalAction)
    parser.set_defaults(debug = False)
    global args
    args = parser.parse_args()

    # Just incase, we need valid headers for requests
    global headers
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    # Login cookies to validate ourselves in itch.io
    global cookies
    cookies = {}

    # This is necessary to getting our login cookies and downloading data
    global csrf
    csrf = None
    
    # All the stored data that we will be scraping from the user's bundles
    global data
    data = {}

    # Error file just incase there is any information that may need to be used in the future
    global errorFile
    errorFile = None

    global debug
    debug = False
