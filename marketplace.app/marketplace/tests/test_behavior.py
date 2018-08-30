from path_file import *

import unittest
from mock import Mock
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox


class TestCase(unittest.TestCase):

    def setUp(self):
        self.user = Mock
        self.user.id = 1
        self.user.first_name = 'Abra'
        self.user.last_nmae = 'Cadabra'
        self.user.patronymic = '111'
        self.user.email = 'vera.cook@example.com'
        self.user.password = '1234'
        self.user.entity = 'consumer'
        self.user.phone_number = '89992272169'

    def testWebpage(self):
        opts = Options()
        self.browser = Firefox(options=opts)
        #opts.set_headless() браузер без интерфейса
        #assert opts.headless  # без графического интерфейса.

        user = self.user
        browser = self.browser
        browser.maximize_window()
        browser.get('http://127.0.0.1:8000')

        # signUpUser
        #browser.find_element_by_id('emailRegistration')#.send_keys('abba@mail.ru')

        browser.find_element_by_id('emailAuthorisation').send_keys(user.email)
        browser.find_element_by_id('passwordAuthorisation').send_keys(user.password)
        browser.find_element_by_id('authButton').click()



    def tearDown(self):
        self.browser.close()


if __name__ == '__main__':
    unittest.main()