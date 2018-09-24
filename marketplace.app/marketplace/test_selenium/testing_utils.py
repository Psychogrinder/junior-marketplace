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


def getEditArgs(driver):
    first_name = driver.find_element_by_id("consumer_first_name")
    last_name = driver.find_element_by_id("consumer_last_name")
    patronymic = driver.find_element_by_id("consumer_patronymic")
    phone = driver.find_element_by_id("consumer_phone")
    address = driver.find_element_by_id("consumer_address")
    elements = [first_name, last_name, patronymic, phone, address]

    edited_data = []
    for element in elements:
        edited_data.append(element.get_attribute('value'))

    return elements, edited_data
