from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import sites.the_tvdb as thetvdb
import sites.torrenthandler as torrenthandler
from classes import Anime
import socket
import time
import userhandler
import threading
import filehandler
import logger
import config
import re

sp_driver = webdriver.Chrome(ChromeDriverManager().install())
sp_driver.set_window_position(-10000,0)

def open_overview_page():
    logger.info("Connecting to Subsplease")
    sp_driver.get('https://subsplease.org/')
    time.sleep(9)


def open_seasonal_page():
    logger.info("Connecting to subsplease Seasonal page")
    sp_driver.get('https://horriblesubs.info/current-season/')
    time.sleep(2)


def go_to_anime(name):
    element = sp_driver.find_element_by_xpath('//a[text()="{}"]'.format(name))
    link = element.get_attribute("href")
    sp_driver.execute_script("window.open('');")
    sp_driver.switch_to_window(sp_driver.window_handles[1])
    sp_driver.get(link)


def leave_anime():
    sp_driver.close()
    sp_driver.switch_to_window(sp_driver.window_handles[0])


def strip_ep_from_title(raw):
    trimmed = re.sub(" —.*", '', raw)
    return trimmed


def detect_season(raw):
    s = re.findall(" S[1-9]", raw)
    if s:
        season = int(s[0].replace(' S', ''))
        return season
    else:
        return 1


def detect_title(raw):
    trimmed = re.split(" S[1-9]", raw)
    return trimmed[0]


def get_every_anime_with_new_ep():
    anime_with_new_ep_list = []
    WebDriverWait(sp_driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tr[@class='new']/td/a")))
    elements = sp_driver.find_elements_by_xpath("//tr[@class='new']/td/a")
    logger.info('Found {} Anime with the tag "New!"'.format(len(elements)))
    for element in elements:
        anime_raw = strip_ep_from_title(element.text)
        anime = Anime(None, None, None)
        anime.latest_title_on_overview = element.text
        anime.season = detect_season(anime_raw)
        anime.title = detect_title(anime_raw)
        logger.info("Collecting links for {} | Season {}".format(anime.title, anime.season))
        go_to_anime(element.text)
        anime.episodes = get_magnet_links()
        anime_with_new_ep_list.append(anime)
        logger.info("Collected {} links".format(len(anime.episodes)))
        leave_anime()
        time.sleep(2)

    return anime_with_new_ep_list


def get_magnet_links():
    time.sleep(2)
    links = list()
    WebDriverWait(sp_driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'1080p')]/span[text()='Magnet']/..")))
    magnet_elements = sp_driver.find_elements_by_xpath(
    "//a[contains(@href,'1080p')]/span[text()='Magnet']/..")
    for element in magnet_elements:
        links.append(element.get_attribute("href"))
    return links
    
