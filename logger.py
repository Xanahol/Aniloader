import datetime

now = datetime.datetime.now().strftime("%b-%d-%Y %H:%M:%S")


def info(info):
    print(now + " - INFO - " + info)


def error(error):
    print(now + " - ERROR - " + error)


def debug(debug):
    print(now + " - DEBUG - " + debug)

def newline():
    print('\n')
