import crawler
import userhandler
import logger
from tabulate import tabulate


arguments = userhandler.get_parameters()

for current_argument, current_value in arguments:

    if current_argument in ("-h", "--help"):
        helptable = [
            ["-h", "--help", "Shows all parameter options"],
            ["-m", "--mode", 'Select a mode to run the download'],
            ["", "getAnime", 'Download a specific anime'],
            [],
            ["-s", "--site", "Select a site on which you want to download"]
        ]
        print(tabulate(helptable))

    elif current_argument in ("-m", "--mode"):
        switcher = {
            'getAnime': crawler.crawl(),
        }
        switcher.get(current_value, 'getAnime')
        crawler.crawl()

    elif current_argument in ("-s", "--site"):
        # TODO
        # implement support for multiple sites (Animekaizoku)
        print(("Not implemented yet") % (current_value))
