from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import sites.the_tvdb as thetvdb
import sites.torrenthandler as torrenthandler
import socket
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
    logger.info("Connecting to HorribleSubs")
    hs_driver.get('https://horriblesubs.info/current-season/')
    WebDriverWait(hs_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='ind-show']/a")))

def go_to_anime(name):
    element = hs_driver.find_element_by_xpath("//a[@title='{}']".format(name))
    link = element.get_attribute("href")
    hs_driver.get(link)


def get_newest_anime():
    return None


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
