from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import userhandler


hs_driver = webdriver.Chrome()
torrent_driver = webdriver.Chrome()
ip_4 = "172.16.17.24"
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
            print("debug loop")
            WebDriverWait(hs_driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='more-button']")))
            element = hs_driver.find_element_by_xpath(
                "//a[@class='more-button']")
            ActionChains(hs_driver).click(element).perform()
        except:
            break


def get_magnet_links():
    magnet_links = list()
    episodes = hs_driver.find_elements_by_xpath(
        "//div[@class='hs-shows']/div")
    a = 1
    for episode in episodes:
        link = hs_driver.find_element_by_xpath(
            "//div[@id='{}-1080p']/span[@class='dl-type hs-magnet-link']/a[@title='Magnet Link']".format(str(a).zfill(2))).get_attribute("href")
        magnet_links.append(link)
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

def insert_links(link_list):
    download = WebDriverWait(torrent_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='downloadButton']")))
    ActionChains(torrent_driver).click(download).perform()

    torrent_driver.switch_to_frame(torrent_driver.find_element_by_id("downloadPage_iframe"))

    WebDriverWait(torrent_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='urls']")))
    element_linkbox = torrent_driver.find_element_by_xpath("//*[@id='urls']")
    for link in link_list:
        element_linkbox.send_keys(link)
        element_linkbox.send_keys(Keys.ENTER)
    submit = WebDriverWait(torrent_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='submitButton']")))
    ActionChains(torrent_driver).click(submit).perform()



def crawl():
    connect_to_horriblesubs()
    anime = userhandler.ask_for_anime()
    go_to_anime(anime)
    show_all_episodes()
    magnet_links = get_magnet_links()
    open_qbittorrent()
    log_in()
    insert_links(magnet_links)
