from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import sites.the_tvdb as thetvdb
import socket
import userhandler
import threading
import filehandler
import logger
import config

tvdb_driver = webdriver.Chrome(ChromeDriverManager().install())


def connect_to_thetvdb():
    logger.info("Connecting to TheTVDB")
    tvdb_driver.get('https://www.thetvdb.com/')

    try:
        # Check for cookies
        cookie_accept_button = WebDriverWait(tvdb_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains( text(), "I accept")]')))
        ActionChains(tvdb_driver).click(cookie_accept_button).perform()
        logger.info("Cookies have been accepted")
    except:
        logger.info("No Cookies to be accepted")

    WebDriverWait(tvdb_driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "form-control")))


def check_for_anime_in_db(anime):
    searchbar = tvdb_driver.find_element_by_class_name("form-control")
    searchbar.send_keys(anime)

    submit_button = tvdb_driver.find_element_by_xpath(
        '//button[@type = "submit"]')
    submit_button.click()

    tv_button = WebDriverWait(tvdb_driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    '//li[@class = "ais-Menu-item list-group-item"]/div/a/span[@class="ais-Menu-label" and contains( text(), "TV")]/..')))
    tv_button.click()

    all_shows_on_overwiew = WebDriverWait(tvdb_driver, 10).until(EC.presence_of_all_elements_located(
        (By.XPATH, '//li[@class="ais-Hits-item"]/div/div/h3/a')))

    counter = 0
    for show in all_shows_on_overwiew:
        if show.text == anime:
            show.click()
            break
        elif counter == 20:
            all_shows_on_overwiew[0].click()
            break
        else:
            counter += 1

    anime_db_name = tvdb_driver.find_element_by_id('series_title').text

    anime_redundance = filehandler.check_if_files_exist(anime_db_name)

    if anime_redundance == True:
        logger.info(
            "It seems you already have a library named after the Anime!")
    else:
        logger.info(
            "It looks like you don't have a library named after the Anime yet!")
