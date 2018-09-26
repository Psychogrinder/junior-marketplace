from append_path import *
from testing_utils import uniqueEmail, uniqueShopName, login, logout, getPhoneMask, getEditElements, setDictValues, \
    getDataFromElements, setNewKeysForDict
import unittest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

unique_email = uniqueEmail()
unique_shop_name = uniqueShopName()
driver = webdriver.Firefox()

class TestProducer(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000'

        self.password = "123123"
        self.reg_data = {"email": unique_email,
                         "password": self.password,
                         "shop_name": unique_shop_name,
                         "contact": "contact",
                         "phone": "9991234455",
                         "address": "hahha ya tut zhivu 15",
                         "desc": ""}


    def test_01_producer_register(self):
        driver.get(self.url)
        data = self.reg_data

        driver.find_element_by_xpath(
            "/html/body/footer/div/div/div[2]/p[1]/a").click() #reg Producer
        driver.find_element_by_id("emailRegProducer").send_keys(data["email"])
        driver.find_element_by_id("passwordRegProducer").send_keys(data["password"])
        driver.find_element_by_id("rePasswordRegProducer").send_keys(data["password"])
        driver.find_element_by_id("nameRegProducer").send_keys(data["shop_name"])
        driver.find_element_by_id("contactPersonRegProducer").send_keys(data["contact"])
        driver.find_element_by_id("phoneRegProducer").send_keys(data["phone"])
        driver.find_element_by_id("addressRegProducer").send_keys(data["address"])
        driver.find_element_by_id("descriptionRegProducer").send_keys(data["desc"])
        driver.find_element_by_id("registrationProducer").click()


    def test_02_producer_logout(self):
        logout(driver)


    def test_03_producer_login(self):
        email, pw = self.reg_data["email"], self.reg_data["password"]
        login(driver, email, pw)


    def test_04_producer_go_to_edit_profile(self):
        driver.implicitly_wait(2)
        driver.find_element_by_xpath("/html/body/header/nav/div/div/div/button").click()  # user menu
        driver.find_element_by_xpath("/html/body/header/nav/div/div/div/div/a[1]").click()  # go to profile


    def test_05_producer_profile_is_data_correct(self):
        driver.implicitly_wait(2)
        shop_name = driver.find_element_by_css_selector(".col-md-8 > h1:nth-child(1)").text

        keys = driver.find_elements_by_class_name("profile-keys")
        values = driver.find_elements_by_class_name("profile-values")
        text = [list(map(lambda x: x.text, keys)), list(map(lambda x: x.text, values))]

        profile_data = setNewKeysForDict(text)
        profile_data['shop_name'] = shop_name

        for key in profile_data:
            if key == 'phone':
                self.assertEqual(profile_data[key], getPhoneMask(self.reg_data[key]))
            else:
                self.assertEqual(profile_data[key], self.reg_data[key])

        driver.close()






    # def test_05_producer_edit_profile(self):
    #     pass


    # def test_06_delete_producer(self):
    #     driver.find_element_by_xpath("/html/body/header/nav/div/div/div/button").click() # user menu
    #     driver.find_element_by_xpath("/html/body/header/nav/div/div/div/div/a[1]").click() # go to profile




