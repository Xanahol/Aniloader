from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import socket
import userhandler
import threading
import filehandler
import logger
import config


def crawl():
    import sites.the_tvdb as thetvdb
    import sites.torrenthandler as torrenthandler
    import sites.horriblesubs as horriblesubs

    logger.info("Setup completed")

    horriblesubs.connect_to_horriblesubs()
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
