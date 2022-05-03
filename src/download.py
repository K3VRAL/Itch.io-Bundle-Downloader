# This starts to download all the mapped games

import setup
import make

def start():
    print("Starting to download all mapped bundles")
    make.makeDownloadFolder()
    bundles = setup.data.keys()
    for bundle in bundles:
        make.makeBundleFolder(bundle)
        
        games = setup.data[bundle]["games"].keys()
        for game in games:
            pass