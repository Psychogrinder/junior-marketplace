from append_path import *
from testing_utils import login, logout
import unittest
from random import randint, choice
from selenium import webdriver
from marketplace.models import Category, User
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as ex


firefox_opts = webdriver.FirefoxOptions()
# firefox_opts.add_argument('--headless')
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
        while self.url: # for logged and non-logged states
            driver.get(self.url)

            # select random category and product
            category = choice(driver.find_elements_by_class_name("catalog-category-item"))
            category.click()
            product = choice(driver.find_elements_by_class_name("card-item"))
            product.click()
            try:
                p = driver.find_element_by_xpath("/html/body/main/div[2]/div[1]/div[2]/p")
                self.assertIn('авторизуйтесь', p.text.lower())

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
        quantity = int(in_stock[:in_stock.find(' ')]) # removing chars and getting int value

        el = driver.find_element_by_id("number")
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(quantity)  # input num of products


    def test_03_add_products_to_cart(self):
        driver.find_element_by_css_selector("button.btn:nth-child(2)").click()
        driver.implicitly_wait(2)


    def test_04_is_product_added_to_cart(self):
        is_added_to_cart = driver.find_element_by_css_selector(".hullabaloo")
        self.assertIsNotNone(is_added_to_cart, 'no message after product has been added to cart')


    def test_05_is_cost_the_same_in_cart(self):
        cost_product = driver.find_element_by_class_name("product_price_value").text
        title_product = driver.find_element_by_class_name("product_title").text

        driver.find_element_by_class_name("header-cart").click()

        # driver.find_element_by_link_text(title_product).text
        # driver.find_element_by_link_text().text

    def test_06_place_order(self):
        driver.find_element_by_id("placeOrderButton").click()


    def test_07_confirm_order(self):
        driver.find_element_by_id("orderPlacementBtn").click()
        order_status = driver.find_element_by_xpath("/html/body/main/section/h2").text
        self.assertIn("успешно оформлен", order_status.lower())

