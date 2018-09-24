from append_path import *

from testing_utils import login, logout
import unittest
from random import randint, choice
from selenium import webdriver
from marketplace.models import Category, User


driver = webdriver.Firefox()


class Order(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000'
        self.consumer = User.query.filter_by(entity='consumer').order_by(User.id.desc()).first()
        self.producer = User.query.filter_by(entity='producer').order_by(User.id.desc()).first()
        self.users = [self.consumer, self.producer]
        self.password = "123123"
        print(self.consumer.id, self.producer.id)

    def test_01_check_auth_status(self):

        driver.get(self.url)

        # select random category and product
        category = driver.find_element_by_css_selector(
            "div.catalog-category-item:nth-child({}) > a:nth-child(1)".format(randint(1, 8)))
        category.click()
        product = choice(driver.find_elements_by_class_name("card-item"))
        product.click()
        p = driver.find_element_by_xpath("/html/body/main/div[2]/div[1]/div[2]/p")

        self.assertIn('Авторизуйтесь для добавления товара в корзину', p.text)

        driver.close()




    # def tearDown(self):
    #     self.driver.close()

