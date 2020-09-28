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

hs_driver = webdriver.Chrome(ChromeDriverManager().install())


def open_overview_page():
    logger.info("Connecting to HorribleSubs")
    hs_driver.get('https://horriblesubs.info/shows/')
    WebDriverWait(hs_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='ind-show']/a")))


def open_seasonal_page():
    logger.info("Connecting to HorribleSubs Seasonal page")
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


def get_every_seasonal_anime():
    seasonal_anime_list = []
    elements = hs_driver.find_elements_by_xpath("//div[@class='ind-show']/a")
    for element in elements[:2]:
        logger.info("Collecting links for " + element.text)
        anime = Anime(None, None, None)
        anime.title = element.get_attribute("title")
        go_to_anime(anime.title)
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
