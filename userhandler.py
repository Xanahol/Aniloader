from getpass import getpass
import getopt
import sys


def ask_for_anime():
    return input("Which anime would you like to download?\n")


def ask_for_downloadpath():
    return input("Where would you like to store the the files?\n")


def ask_for_username():
    return input("Please enter your credentials for qBittorrent:\nUsername:")


def ask_for_password():
    return getpass.getpass('Password (Invisible):')


def get_parameters():
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    short_options = "hm:s:"
    long_options = ["help", "mode=", "site="]
    try:
        arguments, values = getopt.getopt(
            argument_list, short_options, long_options)
        return arguments
    except getopt.error as err:
        print(err)
        sys.exit(2)
