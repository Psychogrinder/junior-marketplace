from append_path import *
from testing_utils import uniqueEmail, uniqueShopName, login, logout, getPhoneMask, getEditElements, setDictValues, \
    getDataFromElements
import unittest
from selenium import webdriver
from marketplace.models import User

unique_email = uniqueEmail()
unique_shop_name = uniqueShopName()
driver = webdriver.Firefox()

class TestProducer(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000'
        self.producer = User.query.filter_by(entity='producer').order_by(User.id.desc()).first()
        self.password = "123123"

        self.contact = 'contact'
        self.phone = '9991234455'
        self.address = 'hahha ya tut zhivu 15'

        self.load_data = {"contact": "",
                          "phone": "",
                          "address": "",
                          "desc": "",
                          }

    def test_01_producer_register(self):
        driver.get(self.url)
        driver.find_element_by_xpath(
            "/html/body/footer/div/div/div[2]/p[1]/a").click() #reg Producer
        driver.find_element_by_id("emailRegProducer").send_keys(unique_email)
        driver.find_element_by_id("passwordRegProducer").send_keys(self.password)
        driver.find_element_by_id("rePasswordRegProducer").send_keys(self.password)
        driver.find_element_by_id("nameRegProducer").send_keys(unique_shop_name)
        driver.find_element_by_id("contactPersonRegProducer").send_keys(self.contact)
        driver.find_element_by_id("phoneRegProducer").send_keys(self.phone)
        driver.find_element_by_id("addressRegProducer").send_keys(self.address)
        driver.find_element_by_id("descriptionRegProducer").send_keys("")
        driver.find_element_by_id("registrationProducer").click()


    def test_02_producer_logout(self):
        logout(driver)


    def test_03_producer_login(self):
        login(driver, self.producer.email, self.password)


    def test_04_producer_go_to_edit_profile(self):
        driver.find_element_by_xpath("/html/body/header/nav/div/div/div/button").click()  # user menu
        driver.find_element_by_xpath("/html/body/header/nav/div/div/div/div/a[1]").click()  # go to profile


    def test_05_producer_edit_profile(self):
        pass


    # def test_06_delete_producer(self):
    #     driver.find_element_by_xpath("/html/body/header/nav/div/div/div/button").click() # user menu
    #     driver.find_element_by_xpath("/html/body/header/nav/div/div/div/div/a[1]").click() # go to profile



        driver.close()
