import crawler
import userhandler
from tabulate import tabulate


arguments = userhandler.get_parameters()

for current_argument, current_value in arguments:

    if current_argument in ("-h", "--help"):
        helptable = [
            ["-h", "--help", "Shows all parameter options"],
            ["-m", "--mode", 'Select a mode to run the download'],
            # TODO
            # ["", "getAnime", 'Download a specific anime'],
            ["", "updateSeasonal", 'Update to the seasonal progress'],
            ["", "standard", 'Standardize your anime-libraries for Plex to read'],
            # TODO
            # ["-s", "--site", "Select a site on which you want to download"]
        ]
        print(tabulate(helptable))

    elif current_argument in ("-m", "--mode"):
        if current_value == 'getAnime':
            crawler.simple_download()
        elif current_value == 'updateSeasonal':
            crawler.update_seasonal()
        elif current_value == 'standard':
            crawler.standardize_downloaded()

    elif current_argument in ("-s", "--site"):
        print(("Not implemented yet") % (current_value))
