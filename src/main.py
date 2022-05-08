# Main function and console flag arguments

import sys
import dotenv

import setup
import user
import mapp
import download

def main(argv):
    print("Username and Password being inputted")
    name = setup.args.username
    pass_ = setup.args.password
    if not setup.args.env:
        while True:
            if setup.cookies != None and setup.csfr != None:
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
    print("Received valid cookies and csfr token")
    mapp.start()
    download.start()

if __name__ == "__main__":
    try:
        setup.init()
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(1)