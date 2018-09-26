from append_path import *
from testing_utils import uniqueEmail, uniqueShopName, login, logout, getPhoneMask, getEditElements, setDictValues, \
    getDataFromElements
import unittest
from selenium import webdriver


unique_email = uniqueEmail()
unique_shop_name = uniqueShopName()
driver = webdriver.Firefox()

class TestProducer(unittest.TestCase):


    def setUp(self):
        self.url = 'http://127.0.0.1:8000'
        self.password = "123123"
        self.load_data = {"contact": "",
                          "phone": "",
                          "address": "",
                          "desc": "",
                          }
        self.contact = 'contact'
        self.phone = '9991234455'
        self.address = 'hahha ya tut zhivu 15'


    def test_01_register_producer(self):
        driver.get(self.url)

        driver.find_element_by_xpath(
            "/html/body/footer/div/div/div[2]/p[1]/a").click() #reg Producer
        driver.find_element_by_id("emailRegProducer").send_keys(unique_shop_name)
        driver.find_element_by_id("passwordRegProducer").send_keys(self.password)
        driver.find_element_by_id("rePasswordRegProducer").send_keys(self.password)
        driver.find_element_by_id("nameRegProducer").send_keys(unique_shop_name)
        driver.find_element_by_id("contactPersonRegProducer").send_keys(self.contact)
        driver.find_element_by_id("phoneRegProducer").send_keys(self.phone)
        driver.find_element_by_id("addressRegProducer").send_keys(self.address)
        driver.find_element_by_id("descriptionRegProducer").send_keys("")
        driver.find_element_by_id("registrationProducer").click()
        logout()

