from append_path import *
from testing_utils import login, logout
import unittest
from random import randint, choice
from selenium import webdriver
from marketplace.models import Category, User
from selenium.common import exceptions as ex


firefox_opts = webdriver.FirefoxOptions()
firefox_opts.add_argument('--headless')
driver = webdriver.Firefox(firefox_options=firefox_opts)


class TestProducts(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000'
        self.consumer = User.query.filter_by(entity='consumer').order_by(User.id.desc()).first()
        self.producer = User.query.filter_by(entity='producer').order_by(User.id.desc()).first()
        self.users = [self.consumer, self.producer]
        self.password = "123123"


    def test_01_check_auth_status_product_card(self):
        logged = False
        # for logged and non-logged states
        while self.url:

            driver.get(self.url)
            # select random category and product
            categories = driver.find_elements_by_class_name("catalog-category-item")
            choice(categories).click()

            product = choice(driver.find_elements_by_class_name("card-item"))
            product.click()
            try:
                p = driver.find_element_by_xpath("/html/body/main/div[2]/div[1]/div[2]/p")
                self.assertIn('Авторизуйтесь для добавления товара в корзину', p.text)

            except ex.NoSuchElementException:
                btn_to_cart = driver.find_element_by_xpath("/html/body/main/div[2]/div[1]/div[2]/div/button")
                self.assertEqual('в корзину', btn_to_cart.text.lower())

            if logged == True:
                break

            login(driver, self.consumer.email, self.password)
            driver.implicitly_wait(2)
            logged = True


    def test_02_enter_all_in_stock_products(self):
        in_stock = driver.find_element_by_id("allProductsInStock").text # get num of prods in stock
        driver.find_element_by_id("number").send_keys(in_stock) #input num of products to buy


    def test_03_add_products_to_cart(self):
        driver.find_element_by_css_selector("button.btn:nth-child(2)").click()


    def test_04_go_to_shopping_cart(self):
        driver.find_element_by_class_name("header-cart").click()
