# Allowing to make writing to output to be a lot easier

import datetime

import setup

title = False

def write(message):    
    global title
    if not title:
        err_ = open(setup.errorFile, "a")
        err_.write("{} {} {}\n".format("-" * 10, str(datetime.datetime.now()), "-" * 10))
        err_.close()
        title = True
    err_ = open(setup.errorFile, "a")
    err_.write(f"{message}\n")
    
    err_.close()