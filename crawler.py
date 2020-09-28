from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import sites.the_tvdb as thetvdb
import sites.torrenthandler as torrenthandler
import sites.horriblesubs as horriblesubs
import socket
import userhandler
import threading
import filehandler
import logger
import config


def simple_download():

    horriblesubs.open_overview_page()
    thetvdb.connect_to_thetvdb()

    torrenthandler.open_qbittorrent()
    torrenthandler.log_in()

    anime = userhandler.ask_for_anime()
    thetvdb.check_for_anime_in_db(anime)
    horriblesubs.go_to_anime(anime)
    horriblesubs.show_all_episodes()
    magnet_links = horriblesubs.get_magnet_links()

    torrenthandler.open_add_link_interface()
    download_path = userhandler.ask_for_downloadpath()
    torrenthandler.insert_links(magnet_links)
    torrenthandler.insert_downloadpath(download_path)
    torrenthandler.submit_links()


# TODO
# Download all seasonal anime episodes that have not been added yet
def update_seasonal():
    horriblesubs.open_seasonal_page()
    thetvdb.connect_to_thetvdb()

    torrenthandler.open_qbittorrent()
    torrenthandler.log_in()

    anime_list = horriblesubs.get_every_seasonal_anime()
    for anime in anime_list:
        horriblesubs.go_to_anime(anime.title)
        episodes_available = len(anime.episodes)
        episode_difference = filehandler.check_if_anime_up_to_date(anime.title, episodes_available)
        if episode_difference is not None:
            links_to_download = anime.episodes[-int(episode_difference):]
            anime.episodes = links_to_download
            torrenthandler.open_add_link_interface()
            torrenthandler.insert_links(anime.episodes)
            download_path = config.default_directory + ":\Plex\Anime\\" + anime.name
            torrenthandler.insert_downloadpath(download_path)
            torrenthandler.submit_links()
            


            

    
