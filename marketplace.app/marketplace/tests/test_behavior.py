from path_file import *

import unittest
from mock import Mock, patch
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

        browser.get('http://127.0.0.1:8000')

        # signUpUser
        #browser.find_element_by_id('emailRegistration')#.send_keys('abba@mail.ru')
        browser.find_element_by_css_selector('form-control mr-sm-2')#.send_keys('abba@mail.ru')
        #browser.find_element_by_class_name('form-control mr-sm-2').send_keys(Keys.RETURN)
        #browser.close()


        '''try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "emailAuthorisation"))
            )
        finally:
            browser.quit()
        print(element)
        '''

        #browser.find_element_by_id('emailAuthorisation').send_keys(user.email)
        #browser.find_element_by_id('passwordAuthorisation').send_keys(user.password)
        #browser.find_element_by_id('authButton').click()



    def tearDown(self):
     #   self.browser.close()
        self.browser.quit()

if __name__ == '__main__':
    unittest.main()