# This starts to make all the folders for the mapped games

import os
import re

import setup
import error

def makeGameFolder(bundle, name):
    gamesPath = "{}/{}/{}".format(setup.args.folder, re.sub("/", "_", bundle), re.sub("/", "_", name))
    if not os.path.isdir(gamesPath):
        print("Making Game Folder [{}] from Bundle [{}]".format(name, bundle))
        os.mkdir(gamesPath)

def makeBundleFolder(name):
    bundlePath = "{}/{}".format(setup.args.folder, re.sub("/", "_", name))
    if not os.path.isdir(bundlePath):
        print("Making Bundle Folder [{}]".format(name))
        os.mkdir(bundlePath)

def makeDownloadFolder():
    if not os.path.isdir(setup.args.folder):
        print("Making Download Folder")
        os.mkdir(setup.args.folder)

    setup.errorFile = "{}/_errors.txt".format(setup.args.folder)
    if not os.path.isfile(setup.errorFile):
        print("Making Error File")
        open(setup.errorFile, "w").close()
        text = "Before sending this error data to the GitHub Issues, make sure all the private information is removed"
        error.write("{}".format("#" * (len(text) + (1 * 2) + (3 * 2))))
        error.write("### {} ###".format(text))
        error.write("{}".format("#" * (len(text) + (1 * 2) + (3 * 2))))
