from append_path import *
from testing_utils import login, logout
import unittest
from selenium import webdriver
from marketplace.models import User

driver = webdriver.Firefox()

class Authorization(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000'
        self.consumer = User.query.filter_by(entity='consumer').first()
        self.producer = User.query.filter_by(entity='producer').first()
        self.password = "123123"


    def test_01_login_consumer(self):
        pw = self.password
        email = self.consumer.email
        login(driver, email, pw)

    def test_02_logout(self):
        logout(driver)

    def test_03_login_producer(self):
        pw = self.password
        email = self.producer.email
        login(driver, email, pw)
        logout(driver)

        driver.close()