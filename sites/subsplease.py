from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from config import DEV
from classes import Anime
import time
import socket
import sys
import os
import logger
import re

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

if not DEV:
    sp_driver = webdriver.Chrome(resource_path('./driver/chromedriver.exe'))
else:
    sp_driver = webdriver.Chrome('./driver/chromedriver.exe')

sp_driver.set_window_position(-10000, 0)


def open_overview_page():
    logger.info("Connecting to Overview-Page")
    sp_driver.get('https://subsplease.org/')
    time.sleep(2)


def open_schedule_page():
    logger.info("Connecting to Schedule-Page")
    sp_driver.get('https://subsplease.org/schedule/')
    time.sleep(2)


def open_all_anime_page():
    logger.info("Connecting to Main-Page")
    sp_driver.get('https://subsplease.org/shows//')
    time.sleep(2)


def open_seasonal_page():
    logger.info("Connecting to subsplease Seasonal page")
    sp_driver.get('https://horriblesubs.info/current-season/')
    time.sleep(2)


def go_to_anime(name):
    element = sp_driver.find_element_by_xpath('//a[text()="{}"]'.format(name))
    link = element.get_attribute("href")
    sp_driver.get(link)


def leave_anime():
    sp_driver.get('https://subsplease.org/shows//')
    time.sleep(2)


def strip_ep_from_title(raw):
    trimmed = re.sub(" —.*", '', raw)
    return trimmed


def detect_season(raw):
    s = re.findall(" S[1-9]", raw)
    if s:
        season = s[0].replace(' S', '')
        return season
    else:
        return str(1)


def detect_batched():
    try:
        WebDriverWait(sp_driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Batch')]")))
        return True
    except:
        return False


def extract_episodes_from_batch():
    WebDriverWait(sp_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'1080p')]/span[text()='Magnet']/..")))
    magnet_element = sp_driver.find_element_by_xpath(
        "//a[contains(@href,'1080p')]/span[text()='Magnet']/..")
    return [magnet_element.get_attribute("href")]


def detect_title(raw):
    trimmed = re.split(" S[1-9]", raw)
    return trimmed[0]


def extract_latest_title():
    WebDriverWait(sp_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[@class='entry-title']")))
    return sp_driver.find_element_by_xpath(
        "//h1[@class='entry-title']").text


def extract_amount_of_episodes_from_batch():
    WebDriverWait(sp_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Batch')]")))
    batch_text = sp_driver.find_element_by_xpath(
        "//label[contains(text(), 'Batch')]").text
    amount_of_episodes = re.findall('\d*(?= \(Batch\))', batch_text)[0]
    return amount_of_episodes


def get_every_anime_with_new_ep():
    anime_with_new_ep_list = []
    WebDriverWait(sp_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[@class='new']/td/a")))
    elements = sp_driver.find_elements_by_xpath("//tr[@class='new']/td/a")
    logger.info('Found {} Anime with the tag "New!"'.format(len(elements)))
    for element in elements:
        anime = Anime(None, None, None)
        anime.title = strip_ep_from_title(element.text)
        anime_with_new_ep_list.append(anime)
        time.sleep(2)

    return anime_with_new_ep_list


def get_every_anime_from_schedule():
    anime_on_schedule_list = []
    WebDriverWait(sp_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[@class='all-schedule-item']/td/a")))
    elements = sp_driver.find_elements_by_xpath(
        "//tr[@class='all-schedule-item']/td/a")
    logger.info('Found {} Anime on schedule'.format(len(elements)))
    for element in elements:
        anime = Anime(None, None, None)
        anime.title = element.text
        if re.search(" (Monthly)", anime.title):
            anime.title = anime.title.replace(" (Monthly)", '')
        anime_on_schedule_list.append(anime)
    return anime_on_schedule_list


def get_magnet_links():
    time.sleep(2)
    links = list()
    WebDriverWait(sp_driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//a[contains(@href,'1080p')]/span[text()='Magnet']/..")))
    magnet_elements = sp_driver.find_elements_by_xpath(
        "//a[contains(@href,'1080p')]/span[text()='Magnet']/..")
    for element in magnet_elements:
        links.append(element.get_attribute("href"))
    return links
