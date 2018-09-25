from append_path import *
from testing_utils import uniqueEmail, login, logout
import unittest

from selenium import webdriver
from marketplace.models import User


email_unique = uniqueEmail()
driver = webdriver.Firefox()

class Authorization(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000'
        self.consumer = User.query.filter_by(entity='consumer').first()
        self.producer = User.query.filter_by(entity='producer').first()
        self.users = [self.consumer, self.producer]
        self.password = "123123"


    def test_01_registration(self):
        url, pw = self.url, self.password
        driver.get(url)
        driver.find_element_by_css_selector(".header-login").click()
        driver.find_element_by_css_selector(
            "p.registration-link:nth-child(4) > a:nth-child(1)").click()
        driver.find_element_by_id("emailRegistration").send_keys(email_unique)
        driver.find_element_by_id("passwordRegistration").send_keys(pw)
        driver.find_element_by_id("re_passwordRegistration").send_keys(pw)
        driver.find_element_by_id("reg_button").click()


    def test_02_logout(self):
        logout(driver)


    def test_03_login_consumer(self):
        pw = self.password
        email = self.consumer.email
        login(driver, email, pw)
        logout(driver)


    def test_04_login_producer(self):
        pw = self.password
        email = self.producer.email
        login(driver, email, pw)
        logout(driver)

        driver.close()