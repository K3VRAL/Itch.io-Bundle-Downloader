# This starts to make all the folders for the mapped games

import os
import re

import setup

def makeGameFolder(bundle, name):
    print("Making Game Folder [{}] from Bundle [{}]".format(name, bundle))
    gamesPath = "{}/downloaded/{}/{}".format(os.getcwd(), re.sub("/", "_", bundle), re.sub("/", "_", name))
    if not os.path.isdir(gamesPath):
        os.mkdir(gamesPath)

def makeBundleFolder(name):
    print("Making Bundle Folder [{}]".format(name))
    bundlePath = "{}/downloaded/{}".format(os.getcwd(), re.sub("/", "_", name))
    if not os.path.isdir(bundlePath):
        os.mkdir(bundlePath)

def makeDownloadFolder():
    print("Making Download Folder")
    downloadPath = "{}/downloaded".format(os.getcwd())
    if not os.path.isdir(downloadPath):
        os.mkdir(downloadPath)

    print("Making Error File")
    setup.errorFile = downloadPath + "/ERRORS"
    if not os.path.isfile(setup.errorFile):
        open(setup.errorFile, "w").close()