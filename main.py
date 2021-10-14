import logger
import crawler
import userhandler
from tabulate import tabulate


arguments = userhandler.get_parameters()
site = None

for argument, value in arguments:

    if argument in ("-h", "--help"):
        helptable = [
            ["-h", "--help", "Shows all parameter options"],
            ["-m", "--mode", 'Select a mode to run the download'],

            ["", "getAnime", 'Download a specific anime'],
            ["", "updateNewEpisodes",
                'Update Anime-shows that released new episodes in the last 24 hours'],
            ["", "getAllSeasonal",
                'Update all Anime-shows from the current weekly schedule'],
            ["", "getAllAnime", 'Update all Anime-shows'],
            ["", "standard", 'Standardize your anime-libraries for Plex to read'],

            ["-s", "--site", "Select a site on which you want to download"]
        ]
        print(tabulate(helptable))

    elif argument in ("-s", "--site"):
        if value == 'subsplease':
            site = value

    elif argument in ("-m", "--mode"):
        if site is None:
            site = 'subsplease'
        if value == 'getAnime':
            crawler.simple_download(site)
        elif value == 'updateNewEpisodes':
            crawler.update_seasonal(site)
        elif value == 'getAllSeasonal':
            crawler.download_from_schedule(site)
        elif value == "getAllAnime":
            crawler.get_all_anime(site)
        elif value == 'standard':
            crawler.standardize_downloaded()
