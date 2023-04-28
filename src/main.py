# Main function and console flag arguments

import sys
import dotenv
import os
import json

import setup
import user
import mapp
import download
import error

def main(argv):
    print("Username and Password being inputted")
    
    name = setup.args.username
    pass_ = setup.args.password

    if (setup.args.folder != None):
        setup.args.folder = " ".join(setup.args.folder)
    else:
        setup.args.folder = os.getcwd()

    if not setup.args.env:
        while True:
            if setup.cookies != None and setup.csrf != None:
                break
            while setup.args.username == None:
                name = input("Input Username of itch.io: ")
                if name != "":
                    break
            while setup.args.password == None:
                pass_ = input("Input Password of itch.io: ")
                if pass_ != "":
                    break
            user.login(name, pass_)
    else:
        config = dotenv.dotenv_values(".env")
        name = config.get("USERNAME")
        if name == None or name == "":
            print("No Username inputted")
            sys.exit(1)

        pass_ = config.get("PASSWORD")
        if pass_ == None or pass_ == "":
            print("No Password inputted")
            sys.exit(1)

        user.login(name, pass_)
        if setup.cookies == None or setup.csrf == None:
            print("Username or Password inputted is incorrect")
            sys.exit(1)

    print("Received valid cookies and csrf token")

    # Check for existing bundle list
    datafile = "{}/_datafile.json".format(setup.args.folder)
    if (os.path.exists(datafile)):
        with open(datafile, "r") as f:
            setup.data = json.load(f)
    if (setup.data == {} or setup.args.reprocess):
        setup.data = {}
        mapp.start()

    # If we're reprocessing, make sure all the games that are set to processed equal to false
    if (setup.args.reprocess):
        for bundle in setup.data:
            for game in setup.data[bundle]["games"]:
                setup.data[bundle]["games"][game]["processed"] = False

    # Output the list of games so we don't have to keep looking it up
    with open(datafile, "w") as write:
        json.dump(setup.data, write)
        if len(list(setup.data.keys())) > 0:
            download.start()
        json.dump(setup.data, write)

    # Errors output    
    for bundle in setup.data:
        for game in setup.data[bundle]["games"]:
            if (setup.data[bundle]["games"][game]["processed"] == False):
                error.write("Game was not processed - Bundle[{}] Error[{}]".format(bundle, game))
   
    # Done
    print("Finished")

if __name__ == "__main__":
    try:
        setup.init()
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(1)
