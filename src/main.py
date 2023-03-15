# Main function and console flag arguments

import sys
import dotenv
import os

import json
import setup
import user
import mapp
import download

def main(argv):
    print("Username and Password being inputted")
    
    print (setup.args)
    name = setup.args.username
    pass_ = setup.args.password
    folder_ = setup.args.folder
    reprocess_ = setup.args.reprocess
    

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
            while setup.args.folder == None:
                folder_ = os.getcwd()
            while setup.args.reprocess == None:
                reprocess_ = False
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

        folder_ = config.get("FOLDER")
        if folder_ == None or folder_ == "":
           folder_ = os.getcwd()

        reprocess_ = config.get("REPROCESS")
        if reprocess_ == None or reprocess_ == "":
           reprocess_ = False

        setup.args.folder = folder_
        setup.args.reprocess = reprocess_

        user.login(name, pass_)
        if setup.cookies == None or setup.csrf == None:
            print("Username or Password inputted is incorrect")
            sys.exit(1)

    print("Received valid cookies and csfr token")

    # check for existing bundle list
    setup.data = read()

    if (setup.data == {} or reprocess_ == "True"):
        setup.data = {}
        mapp.start()

    # If we're reprocessing, make sure all the games are set to processed = false
    if (setup.args.reprocess == "True"):
        for bundle in setup.data:
            for game in setup.data[bundle]["games"]:
                setup.data[bundle]["games"][game]["processed"] = False

    #output the list of games so we don't have to keep looking it up
    write(setup.data, "datafile.json")

    bundles = list(setup.data.keys())
    
    if len(bundles) > 0:
        download.start()
    
    write(setup.data, "datafile.json")

    errors = []
    for bundle in setup.data:
        for game in setup.data[bundle]["games"]:
            if (setup.data[bundle]["games"][game]["processed"] == False):
                game = setup.data[bundle]["games"][game]
                errors.append(game)
           
    #errors.json output    
    write(errors, "errors.json")
   
    print("Finished")

def write(data, filename):
    with open( filename , "w" ) as write:
        json.dump( data , write )

def read():   
    datafile = 'datafile.json'
    if (os.path.exists(datafile)):
        with open(datafile) as f:
            data = json.load(f)
            return data
    else:
        return {}

if __name__ == "__main__":
    try:
        setup.init()
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(1)