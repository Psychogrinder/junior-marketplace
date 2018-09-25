from append_path import *
from testing_utils import login, logout, getPhoneMask, getEditElements, setDictValues, \
    getDataFromElements
import unittest
from selenium import webdriver
from marketplace.models import Category, User

driver = webdriver.Firefox()

class TestConsumer(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000'
        self.consumer = User.query.filter_by(entity='consumer').order_by(User.id.desc()).first()
        self.producer = User.query.filter_by(entity='producer').order_by(User.id.desc()).first()
        self.users = [self.consumer, self.producer]
        self.password = "123123"
        self.load_data = {"first_name": "",
                          "last_name": "",
                          "patronymic": "",
                          "phone": "",
                          "address": "",
                          }

    def test_01_register_consumer(self):
        url, pw = self.url, self.password
        driver.get(url)
        driver.find_element_by_css_selector(".header-login").click()
        driver.find_element_by_css_selector(
            "p.registration-link:nth-child(4) > a:nth-child(1)").click()
        driver.find_element_by_id("emailRegistration").send_keys(email_unique)
        driver.find_element_by_id("passwordRegistration").send_keys(pw)
        driver.find_element_by_id("re_passwordRegistration").send_keys(pw)
        driver.find_element_by_id("reg_button").click()


    def test_02_edit_consumer(self):
        login(driver, self.consumer.email, self.password)
        driver.find_element_by_css_selector("button.btn:nth-child(1)").click() # User menu btn
        driver.find_element_by_css_selector("a.dropdown-item:nth-child(1)").click() # Profile btn
        driver.find_element_by_css_selector(
            ".edit-profile > a:nth-child(1)").click()  # Edit profile btn

        elements_to_edit = getEditElements(driver)
        data_to_edit = getDataFromElements(elements_to_edit)
        save_profile = driver.find_element_by_id("save_consumer_profile")

        # filling new data in the fields on the Edit User Page
        load_data = setDictValues(self.load_data)
        keys = list(load_data.keys())
        for arg in range(len(data_to_edit)):
            key = keys[arg]
            elements_to_edit[arg].clear()
            elements_to_edit[arg].send_keys(load_data[key])
        edited_data = getDataFromElements(elements_to_edit)
        save_profile.click()

        driver.find_element_by_xpath("/html/body/main/div[1]/div/p/a").click() # Edit profile btn
        # verification that saved values corresponds loading data
        for arg in range(len(edited_data)):
            key = keys[arg]
            if key == "phone":
                phone_number = getPhoneMask(load_data[key])  # in load data string of nums
                self.assertEqual(phone_number, edited_data[arg])
            else:
                self.assertEqual(load_data[key], edited_data[arg])


    def test_03_delete_consumer(self):
        driver.find_element_by_xpath("/html/body/main/div[1]/div/p/a").click()  # Edit profile btn
        driver.find_element_by_css_selector(".out-of-stock > a:nth-child(1)").click()  # Delete profile btn
        # driver.find_element_by_xpath("/html/body/div[5]/div/div/div[3]/button[1]").click() #cancel btn
        # driver.find_element_by_css_selector(".out-of-stock > a:nth-child(1)").click()  # again Delete profile btn
        driver.find_element_by_id("deleteConsumerBtn").click()

        self.assertIsNone(User.query.filter_by(id=self.consumer.id).first())
        driver.close()