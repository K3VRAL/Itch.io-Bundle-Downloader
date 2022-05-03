# Main function and console flag arguments

import sys
import argparse
import dotenv

import setup
import user
import mapping

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--username", help = "The input of the user's username for itch.io")
parser.add_argument("-p", "--password", help = "The input of the user's password for itch.io")
parser.add_argument("-e", "--env", help = "Have the input in a .env file and read the username and password from there", action = argparse.BooleanOptionalAction)
parser.set_defaults(env = False)
args = parser.parse_args()

def main(argv):
    print("Username and Password being inputted")
    name = args.username
    pass_ = args.password
    if not args.env:
        while True:
            if setup.cookies != None and setup.csfr != None:
                break
            while args.username == None:
                name = input("Input Username of itch.io: ")
                if name != "":
                    break
            while args.password == None:
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
    mapping.start()
    download.start()

if __name__ == "__main__":
    setup.init()
    main(sys.argv[1:])