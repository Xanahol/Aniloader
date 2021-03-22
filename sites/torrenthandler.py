from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from sites.subsplease import leave_anime
import socket
import userhandler
import logger
import config
import time

torrent_driver = webdriver.Chrome(ChromeDriverManager().install())
torrent_driver.set_window_position(-10000, 0)


def open_qbittorrent():
    logger.info("Connecting to the qBittorrent")
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        ip_4 = ip_address
        logger.info("Your IP is: " + ip_4)
        torrent_driver.get("http://"+ip_4+":"+config.torrent_port+"/")
    except:
        torrent_driver.get("http://"+config.ip_4+":"+config.torrent_port+"/")


def log_in():
    try:
        WebDriverWait(torrent_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='username']")))
        WebDriverWait(torrent_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='password']")))

        element_username = torrent_driver.find_element_by_id("username")

        element_password = torrent_driver.find_element_by_id("password")

        # Asks for credentials
        username = userhandler.ask_for_username()
        password = userhandler.ask_for_password()

        element_username.clear()
        element_password.clear()
        element_username.send_keys(username)
        element_password.send_keys(password)

        submit = WebDriverWait(torrent_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='login']")))
        ActionChains(torrent_driver).click(submit).perform()

        try:
            WebDriverWait(torrent_driver, 2).until(
                EC.presence_of_element_located((By.ID, "downloadButton")))
            logger.info('Login successful!')
        except:
            logger.error("Wrong username or password. Please try again")
            log_in()
    except:
        try:
            WebDriverWait(torrent_driver, 2).until(
                EC.presence_of_element_located((By.ID, "downloadButton")))
            logger.info("Bypass detected. No login necessary")
        except:
            logger.error("There was an error trying to load the Torrent-Page")
            log_in()


def open_add_link_interface():
    time.sleep(2)
    download = WebDriverWait(torrent_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='downloadButton']")))
    ActionChains(torrent_driver).click(download).perform()

    torrent_driver.switch_to_frame(
        torrent_driver.find_element_by_id("downloadPage_iframe"))


def insert_links(link_list):

    WebDriverWait(torrent_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='urls']")))
    element_linkbox = torrent_driver.find_element_by_xpath("//*[@id='urls']")

    for link in link_list:

        element_linkbox.send_keys(link)
        element_linkbox.send_keys(Keys.ENTER)


def insert_downloadpath(path):
    WebDriverWait(torrent_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='savepath']")))
    element_savepath = torrent_driver.find_element_by_xpath(
        "//*[@id='savepath']")
    element_savepath.clear()
    element_savepath.send_keys(path)


def queue(links, path):
    open_add_link_interface()
    logger.info('Inserting Links to download')
    insert_links(links)
    logger.info('Inserting Download Path')
    insert_downloadpath(path)
    logger.info('Submitting Links')
    submit_links()
    leave_anime()


def submit_links():
    submit = WebDriverWait(torrent_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='submitButton']")))
    ActionChains(torrent_driver).click(submit).perform()
