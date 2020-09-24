from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import userhandler
import threading
import filehandler
import logger


hs_driver = webdriver.Chrome()
torrent_driver = webdriver.Chrome()
tvdb_driver = webdriver.Chrome()
ip_4 = "192.168.1.135"
torrent_port = "8080"


def connect_to_horriblesubs():
    logger.info("Connecting to HorribleSubs")
    hs_driver.get('https://horriblesubs.info/shows/')
    WebDriverWait(hs_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='ind-show']/a")))


def connect_to_thetvdb():
    logger.info("Connecting to TheTVDB")
    tvdb_driver.get('https://www.thetvdb.com/')

    try:
        # Check for cookies
        cookie_accept_button = WebDriverWait(tvdb_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains( text(), "I accept")]')))
        ActionChains(tvdb_driver).click(cookie_accept_button).perform()
    except:
        logger.info("No Cookies to be accepted")

    WebDriverWait(tvdb_driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "form-control")))


def open_qbittorrent():
    logger.info("Connecting to the qBittorrent")
    torrent_driver.get("http://"+ip_4+":"+torrent_port+"/")


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


def log_in():
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
    except:
        logger.error("Wrong username or password. Please try again.")
        log_in()


def open_add_link_interface():
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


def submit_links():
    submit = WebDriverWait(torrent_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='submitButton']")))
    ActionChains(torrent_driver).click(submit).perform()


def crawl():
    connect_to_horriblesubs()
    connect_to_thetvdb()

    open_qbittorrent()
    log_in()

    anime = userhandler.ask_for_anime()
    check_for_anime_in_db(anime)
    go_to_anime(anime)
    show_all_episodes()
    magnet_links = get_magnet_links()

    open_add_link_interface()
    download_path = userhandler.ask_for_downloadpath()
    threading.Thread(target=insert_links(magnet_links)).start()
    threading.Thread(target=insert_downloadpath(download_path)).start()
    submit_links()
