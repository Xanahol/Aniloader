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

hs_driver = webdriver.Chrome(ChromeDriverManager().install())


def open_overview_page():
    logger.info("Connecting to Subsplease")
    hs_driver.get('https://subsplease.org/')
    WebDriverWait(hs_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='ind-show']/a")))


def open_seasonal_page():
    logger.info("Connecting to subsplease Seasonal page")
    hs_driver.get('https://horriblesubs.info/current-season/')
    time.sleep(2)


def go_to_anime(name):
    element = hs_driver.find_element_by_xpath("//a[@title='{}']".format(name))
    link = element.get_attribute("href")
    hs_driver.execute_script("window.open('');")
    hs_driver.switch_to_window(hs_driver.window_handles[1])
    hs_driver.get(link)

def leave_anime():
    hs_driver.close()
    hs_driver.switch_to_window(hs_driver.window_handles[0])

# TODO
# return a list of all seasonal anime from the class Anime

def strip_ep_from_title(raw):
    trimmed = re.sub(" —.*", '', raw)
    return trimmed

def detect_season(raw):
    trimmed = re.split(" S[1-9]", raw)
    season = int(trimmed[1].replace(' S', ''))
    return season
    
def detect_title(raw):
    trimmed = re.split(" S[1-9]", raw)
    return trimmed[0]

def get_every_seasonal_anime():
    seasonal_anime_list = []
    elements = hs_driver.find_elements_by_xpath("//tr[@class='new']/td/a")
    for element in elements:
        anime_raw = strip_ep_from_title(element.text)
        logger.info("Collecting links for " + anime_raw)
        anime = Anime(None, None, None)
        anime.season = detect_season(anime_raw)
        anime.title = detect_title(anime_raw)
        
        anime.url = hs_driver.current_url
        show_all_episodes()
        anime.episodes = get_magnet_links()
        seasonal_anime_list.append(anime)
        leave_anime()
        time.sleep(2)

    return seasonal_anime_list


def show_all_episodes():

    while True:

        try:
            el = hs_driver.find_element_by_xpath("//*[@class='more-button']")
        except:
            break
        elattr = el.get_attribute('href')
        tryme = "#" in elattr

        if tryme == True:
            clickable = WebDriverWait(hs_driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@class='more-button']")))
            ActionChains(hs_driver).click(clickable).perform()
            time.sleep(1)

        else:
            break


def get_magnet_links():
    magnet_links = list()
    episodes = hs_driver.find_elements_by_xpath(
        "//div[@class='hs-shows']/div")
    a = 1
    for episode in episodes:
        try:
            link = hs_driver.find_element_by_xpath(
                "//div[@id='{}-1080p']/span[@class='dl-type hs-magnet-link']/a[@title='Magnet Link']".format(str(a).zfill(2))).get_attribute("href")
        except:
            link = hs_driver.find_element_by_xpath(
                "//div[@id='{}-720p']/span[@class='dl-type hs-magnet-link']/a[@title='Magnet Link']".format(str(a).zfill(2))).get_attribute("href")
        magnet_links.append(link)
        a += 1
    return magnet_links
