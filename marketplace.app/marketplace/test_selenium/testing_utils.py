from append_path import *
from datetime import datetime
from random import choice
from selenium import webdriver
from selenium.common import exceptions as ex
from pyvirtualdisplay import Display


def init_driver_and_display():
    driver, display = False, False
    try:
        firefox_opts = webdriver.FirefoxOptions()
        firefox_opts.add_argument('--headless')
        driver = webdriver.Firefox(firefox_options=firefox_opts)

    except ex.WebDriverException:
        display = Display(visible=0, size=(800, 600))
        display.start()
        print("display were initialized\n")
        driver = webdriver.Firefox()

    finally:
        return driver, display


def uniqueEmail():
    return "mail_" + datetime.now().strftime('%f') + "@ya.ua"


def uniqueShopName():
    name, alphabet = '', 'qwertyuiopasdfghjklzxcvbnm'
    for x in range(7):
        name += choice(alphabet)
    return "Shop_" + name


def login(driver, email, pw):
    url = 'http://127.0.0.1:8000'
    driver.get(url)
    try:
        driver.find_element_by_class_name(".navbar-toggler").click()
    except ex.NoSuchElementException:
        driver.find_element_by_css_selector("#navbarColor01 > a > img").click()
        driver.find_element_by_id("emailAuthorisation").send_keys(email)
        driver.find_element_by_id("passwordAuthorisation").send_keys(pw)
        driver.find_element_by_id("authButton").click()


def logout(driver):
    try:
        driver.find_element_by_class_name(".navbar-toggler").click()
    except ex.NoSuchElementException:
        driver.find_element_by_css_selector("button.btn:nth-child(1)").click()
        driver.find_element_by_id("logoutButton").click()


def getEditElements(driver):
    first_name = driver.find_element_by_id("consumer_first_name")
    last_name = driver.find_element_by_id("consumer_last_name")
    patronymic = driver.find_element_by_id("consumer_patronymic")
    phone = driver.find_element_by_id("consumer_phone")
    address = driver.find_element_by_id("consumer_address")

    elements = [first_name, last_name, patronymic, phone, address]
    return elements


def getPhoneMask(nums):
    return "+7({}){}-{}-{}".format(nums[:3], nums[3:6], nums[6:8], nums[8:10])


def getDataFromElements(elements):
    edited_data = []
    for element in elements:
        edited_data.append(element.get_attribute('value'))
    return edited_data


def setDictValues(data):
    names = ["Sir", "Van", "Kek", "Pes", "Rasa", "Volod"]
    addresses = ["nako 1", "treuy 7/6", "yupoi 56 2", "12 fde l23", "SavanNe 45"]
    phones = ["9991112233", "1112223344", "0002225566", "5554446677"]
    for key in data:
        if key == "phone":
            data[key] = choice(phones)
        elif key == 'address':
            data[key] = choice(addresses)
        else:
            data[key] = choice(names)
    return data


def setNewKeysForDict(text_arr):
    keys, values = text_arr[0], text_arr[1]
    eng_keys = []
    for k in keys:
        if k == 'Контактное лицо:':
            eng_keys.append('contact')
        elif k == 'E-mail:':
            eng_keys.append('email')
        elif k == 'Телефон:':
            eng_keys.append('phone')
        elif k == 'Адрес:':
            eng_keys.append('address')

    return dict(zip(eng_keys, values))