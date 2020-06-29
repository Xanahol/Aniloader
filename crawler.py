from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import userhandler


driver = webdriver.Chrome()


def connect_to_horriblesubs():
    driver.get('https://horriblesubs.info/shows/')


def wait_for_site_to_load():
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='ind-show']")))


def get_all_episodes(name):
    element = driver.find_element_by_xpath("//a[@title='{}']".format(name))
    link = element.get_attribute("href")
    driver.get(link)


def crawl():
    connect_to_horriblesubs()
    wait_for_site_to_load()
    anime = userhandler.ask_for_anime()
    get_all_episodes(anime)
