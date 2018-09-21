from append_path import *
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from marketplace.models import User


driver = webdriver.Firefox()

class TestAuthorization(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000'
        self.consumer = User.query.filter_by(entity='consumer').first()
        self.producer = User.query.filter_by(entity='producer').first()
        self.users = [self.consumer, self.producer]

        self.password = '123123'


    # def test_01_registration(self):
    #     driver = self.driver
    #     url, pw = self.url, self.password


    def test_02_login(self):

        url, pw = self.url, self.password

        def login_from_url(url, email):
            driver.get(url)
            driver.find_element_by_xpath("/html/body/header/nav/div/div/a").click()
            input_email = driver.find_element_by_id("emailAuthorisation")
            input_pw = driver.find_element_by_id("passwordAuthorisation")

            input_email.send_keys(email)
            input_pw.send_keys(pw)
            driver.find_element_by_id("authButton").click()

        def logout():
            driver.find_element_by_css_selector("button.btn:nth-child(1)").click()
            driver.find_element_by_id("logoutButton").click()

        login_from_url(url, self.consumer.email)
        logout()
        login_from_url(url, self.producer.email)


    def test_03_logout(self):
        driver.find_element_by_css_selector("button.btn:nth-child(1)").click()
        driver.find_element_by_id("logoutButton").click()


    # def tearDown(self):
    #     driver.close()

if __name__ == "__main__":
    unittest.main()