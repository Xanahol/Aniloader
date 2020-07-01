from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import userhandler


hs_driver = webdriver.Chrome()
torrent_driver = webdriver.Chrome()
ip_4 = "192.168.1.135"
torrent_port = "8080"
username = "Xana"
password = "Xanaholovous01"


def connect_to_horriblesubs():
    hs_driver.get('https://horriblesubs.info/shows/')
    WebDriverWait(hs_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='ind-show']/a")))


def go_to_anime(name):
    element = hs_driver.find_element_by_xpath("//a[@title='{}']".format(name))
    link = element.get_attribute("href")
    hs_driver.get(link)


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


def open_qbittorrent():
    torrent_driver.get("http://"+ip_4+":"+torrent_port+"/")


def log_in():
    WebDriverWait(torrent_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='username']")))
    WebDriverWait(torrent_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='password']")))

    element_username = torrent_driver.find_element_by_id("username")

    element_password = torrent_driver.find_element_by_id("password")

    element_username.send_keys(username)
    element_password.send_keys(password)

    submit = WebDriverWait(torrent_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='login']")))
    ActionChains(torrent_driver).click(submit).perform()


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

    submit = WebDriverWait(torrent_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='submitButton']")))
    ActionChains(torrent_driver).click(submit).perform()


def insert_downloadpath(path):
    WebDriverWait(torrent_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='savepath']")))
    element_savepath = torrent_driver.find_element_by_xpath(
        "//*[@id='savepath']")
    element_savepath.clear()
    element_savepath.send_keys(path)


def crawl():
    connect_to_horriblesubs()

    open_qbittorrent()
    log_in()

    anime = userhandler.ask_for_anime()
    go_to_anime(anime)
    show_all_episodes()
    magnet_links = get_magnet_links()

    open_add_link_interface()
    download_path = userhandler.ask_for_downloadpath()
    insert_downloadpath(download_path)
    insert_links(magnet_links)
