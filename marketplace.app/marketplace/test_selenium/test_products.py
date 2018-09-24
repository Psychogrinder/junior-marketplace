from append_path import *

from testing_utils import login, logout, getEditArgs
import unittest
from random import randint, choice
from selenium import webdriver
from marketplace.models import Category, User
from selenium.common import exceptions as ex

driver = webdriver.Firefox()


class Order(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000'
        self.consumer = User.query.filter_by(entity='consumer').order_by(User.id.desc()).first()
        self.producer = User.query.filter_by(entity='producer').order_by(User.id.desc()).first()
        self.users = [self.consumer, self.producer]
        self.password = "123123"

        self.edit_data = {"first_name": "",
                          "last_name": "",
                          "patronymic": "",
                          "phone": "",
                          "address": "",
                          }

    def test_01_check_auth_status(self):
        driver.get(self.url)

        login(driver, self.consumer.email, self.password)

        # select random category and product
        category = driver.find_element_by_css_selector(
            "div.catalog-category-item:nth-child({}) > a:nth-child(1)".format(randint(1, 8)))
        category.click()
        product = choice(driver.find_elements_by_class_name("card-item"))
        product.click()
        try:
            p = driver.find_element_by_xpath("/html/body/main/div[2]/div[1]/div[2]/p")
            self.assertIn('Авторизуйтесь для добавления товара в корзину', p.text)

        except ex.NoSuchElementException:
            btn_to_cart = driver.find_element_by_xpath("/html/body/main/div[2]/div[1]/div[2]/div/button")
            self.assertEqual('в корзину', btn_to_cart.text.lower())


    # def test_02_cart(self):
    #     login(driver, self.consumer.email, self.password)
    #
    #     driver.find_element_by_class_name("header-card").click()
    #
    #     driver.close()

    def test_03_edit_consumer(self):
        login(driver, self.consumer.email, self.password)
        driver.find_element_by_css_selector("button.btn:nth-child(1)").click() # User menu btn
        driver.find_element_by_css_selector("a.dropdown-item:nth-child(1)").click() # Profile btn
        driver.find_element_by_css_selector(".edit-profile > a:nth-child(1)").click()  # Edit profile btn

        elements, edited = getEditArgs(driver)

        save_profile = driver.find_element_by_id("save_consumer_profile")
        delete_profile = driver.find_element_by_css_selector(".out-of-stock > a:nth-child(1)") # Delete profile btn

        edit_data = self.edit_data
        edit_data["first_name"] = "Rama1"
        edit_data["last_name"] = "lava1"
        edit_data["patronymic"] = "bi1"
        edit_data["phone"] = "9991112233"
        edit_data["address"] = "fake str 55"

        keys = list(edit_data.keys())
        for arg in range(len(elements)):
            key = keys[arg]
            new_value = self.edit_data[key]
            elements[arg].clear()
            elements[arg].send_keys(new_value)

        save_profile.click()
        driver.find_element_by_xpath("/html/body/main/div[1]/div/p/a").click()

        print(edited)
        print(edit_data)
        for arg in range(len(edited)):
            key = keys[arg]
            edited, to_edit = edited[arg], edit_data[key]
            print(to_edit, edited)



    # def tearDown(self):
    #     self.driver.close()

