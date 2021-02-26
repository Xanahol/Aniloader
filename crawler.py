from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import os
import re
import socket
import userhandler
import threading
import filehandler
import logger
import config


def simple_download():

    import sites.torrenthandler as torrenthandler
    import sites.subsplease as subsplease

    subsplease.open_overview_page()
    thetvdb.connect_to_thetvdb()

    torrenthandler.open_qbittorrent()
    torrenthandler.log_in()

    anime = userhandler.ask_for_anime()
    thetvdb.check_for_anime_in_db(anime)
    subsplease.go_to_anime(anime)
    subsplease.show_all_episodes()
    magnet_links = subsplease.get_magnet_links()

    torrenthandler.open_add_link_interface()
    download_path = userhandler.ask_for_downloadpath()
    torrenthandler.insert_links(magnet_links)
    torrenthandler.insert_downloadpath(download_path)
    torrenthandler.submit_links()


def update_seasonal():

    import sites.torrenthandler as torrenthandler
    import sites.subsplease as subsplease
    import sites.the_tvdb as thetvdb

    thetvdb.tvdb_driver.quit()

    subsplease.open_overview_page()

    torrenthandler.open_qbittorrent()
    torrenthandler.log_in()
    logger.info('Login successful!')

    anime_list = subsplease.get_every_anime_with_new_ep()
    logger.newline()
    logger.info('Starting Download-Process...')
    logger.newline()
    for anime in anime_list:
        subsplease.go_to_anime(anime.latest_title_on_overview)
        episodes_available = len(anime.episodes)
        logger.info("The anime {} has {} episodes so far".format(anime.title, len(anime.episodes)))
        episode_difference = filehandler.check_if_anime_up_to_date(anime.title, anime.season, episodes_available)
        download_path = filehandler.check_directory_for_anime(anime.title, anime.season)
        logger.info("Downloading them to {}".format(download_path))
        if episode_difference is not None:
            logger.info("{} of which are not on the server yet".format(episode_difference))
            links_to_download = anime.episodes[:int(episode_difference)]
            torrenthandler.open_add_link_interface()
            logger.info('Inserting Links to download')
            torrenthandler.insert_links(links_to_download)
            logger.info('Inserting Download Path')
            torrenthandler.insert_downloadpath(download_path)
            logger.info('Submitting Links')
            torrenthandler.submit_links()
            subsplease.leave_anime()
            logger.info('Process finished for ' + anime.title)
            logger.newline()
        else:
            subsplease.leave_anime()
            logger.info(anime.title + ' is already up to date')
            logger.info('Process finished for ' + anime.title)
            logger.newline()

    torrenthandler.torrent_driver.quit()
    subsplease.sp_driver.quit()


def test_function():
    anime_list = os.walk(config.directories)
    dir_list = []
    for anime in anime_list:
        if re.search('Season ', anime[0]):
            dir_list.append(anime[0])
    print(dir_list)

def standardize_downloaded():
    for directory in config.directories:
        path_list = filehandler.select_paths(directory)
        filehandler.rename(path_list)

            

    
