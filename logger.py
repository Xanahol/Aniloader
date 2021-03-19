import datetime

now = datetime.datetime.now().strftime("%b-%d-%Y %H:%M:%S")


def info(info):
    msg = now + " - INFO - " + info# + newline
    print(msg)
    # log(msg)


def error(error):
    msg = now + " - ERROR - " + error #+ newline
    print(msg)
    # log(msg)


def debug(debug):
    msg = now + " - DEBUG - " + debug #+ newline
    print(msg)
    # log(msg)


def newline():
    print('\n')
