from append_path import *
from datetime import datetime


def uniqueEmail():
    return "mail" + datetime.now().strftime('%f') + "@ya.ua"


def login(driver, email, pw):
    url = 'http://127.0.0.1:8000'
    driver.get(url)
    driver.find_element_by_xpath("/html/body/header/nav/div/div/a").click()
    driver.find_element_by_id("emailAuthorisation").send_keys(email)
    driver.find_element_by_id("passwordAuthorisation").send_keys(pw)
    driver.find_element_by_id("authButton").click()


def logout(driver):
    driver.find_element_by_css_selector("button.btn:nth-child(1)").click()
    driver.find_element_by_id("logoutButton").click()