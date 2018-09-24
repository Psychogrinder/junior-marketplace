from append_path import *
from testing_utils import uniqueEmail, login, logout
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from marketplace.models import User



email_unique = uniqueEmail()
driver = webdriver.Firefox()


class TestCaseAuthorization(unittest.TestCase):

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
        logout(driver)

    def test_02_login(self):
        pw = self.password

        login(driver, self.consumer.email, pw)
        logout(driver)
        login(driver, self.producer.email, pw)


    def test_03_logout(self):
        logout(driver)


    # def tearDown(self):
    #     self.driver.close()

if __name__ == "__main__":
    unittest.main()
    driver.close()