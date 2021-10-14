import datetime

now = datetime.datetime.now().strftime("%b-%d-%Y %H:%M:%S")


def info(info):
    msg = now + " - INFO - " + info
    print(msg)


def error(error):
    msg = now + " - ERROR - " + error
    print(msg)


def debug(debug):
    msg = now + " - DEBUG - " + debug
    print(msg)


def newline():
    print('\n')
