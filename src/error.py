# Allowing to make writing to output to be a lot easier

import datetime

import setup

title = False

def write(message):
    global title
    if not title:
        with open(setup.errorFile, "a") as err:
            err.write("{} {} {}\n".format("-" * 10, str(datetime.datetime.now()), "-" * 10))
        title = True
    with open(setup.errorFile, "a") as err:
        err.write("{}\n".format(message))
