# This is just to set up for the global variables

def init():
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