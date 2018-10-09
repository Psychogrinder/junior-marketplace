from append_path import *
from testing_utils import init_driver_and_display, check_connection, login, logout

from random import choice
from marketplace.models import Category, User

import unittest

from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as ex


url = "http://127.0.0.1:8000"

driver, display = init_driver_and_display()
check_connection(driver, url)


class TestProducts(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000'
        self.consumer = User.query.filter_by(entity='consumer').order_by(User.id.desc()).first()
        self.producer = User.query.filter_by(entity='producer').order_by(User.id.desc()).first()
        self.users = [self.consumer, self.producer]
        self.password = "123123"


    def test_01_check_auth_status_product_card(self):
        logged = False

        while not logged: # for logged and non-logged states
            driver.get(self.url)
            
            # select random category and product
            categories = driver.find_elements_by_class_name("catalog-category-item")

            if not categories:
                print("categories are empty\n")
                raise SystemExit(1)
            choice(categories).click()

            products = driver.find_elements_by_class_name("card-item")
            choice(products).click()

            try:
                p = driver.find_element_by_xpath("/html/body/main/div[2]/div[1]/div[2]/p")
                self.assertIn('авторизуйтесь', p.text.lower())

            except ex.NoSuchElementException:
                logged = True

            else:
                login(driver, self.consumer.email, self.password)


    def test_02_goods_out_of_stock_chec(self):

        try:
            driver.find_element_by_css_selector("button.btn:nth-child(2)") # add to cart btn

        except Exception:
            self.assertIn("нет в наличии", driver.find_element_by_class_name("goods-ended").text.lower())

            driver.execute_script("window.history.go(-1)")  # open previous page
            driver.find_element_by_id("in_stock_catalog_products").click()
            product = choice(driver.find_elements_by_class_name("card-item"))
            product.click()  # open product card


    def test_03_enter_all_in_stock_products(self):
        in_stock = driver.find_element_by_id("allProductsInStock").text # get num of prods in stock
        quantity = int(in_stock[:in_stock.find(' ')]) # removing chars and getting int value

        el = driver.find_element_by_id("number")
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(1)  # input num of products


    def test_04_add_products_to_cart(self):
        driver.find_element_by_css_selector("button.btn:nth-child(2)").click()
        driver.implicitly_wait(2)


    def test_05_is_product_added_to_cart(self):
        is_added_to_cart = driver.find_element_by_css_selector(".hullabaloo")
        self.assertIsNotNone(is_added_to_cart, 'no message after product has been added to cart')

    #TODO
    def test_06_is_cost_the_same_in_cart(self):
        # cost_product = driver.find_element_by_class_name("product_price_value").text
        # title_product = driver.find_element_by_class_name("product_title").text

        driver.find_element_by_class_name("header-cart").click()

        # driver.find_element_by_link_text(title_product).text
        # driver.find_element_by_link_text().text

    def test_07_place_order(self):
        products = driver.find_elements_by_id("productIdCart") #get id of products
        products_id = [i.text for i in products]
        print('prod_id', products_id)
        driver.find_element_by_id("placeOrderButton").click()


    def test_08_select_delivery_method(self):
        deliveries = driver.find_elements_by_class_name("col-4 col-md-3")
        print(len(deliveries))

        delivery_methods = driver.find_elements_by_tag_name("option") # (курьер, самовывоз) * N {deliveries}

        for product_delivery in deliveries:
            product_delivery.click()

            method_element = choice(delivery_methods[:3])
            print(method_element.text)
            method_element.click()
            del delivery_methods[:3]



    def test_09_register_order(self):
        driver.find_element_by_id("orderPlacementBtn").click()
        order_status = driver.find_element_by_xpath("/html/body/main/section/h2").text
        self.assertIn("успешно оформлен", order_status.lower(),
                      "order-registration-button has been clicked, but no message to consumer")


    def test_10_orders_history(self):
        driver.find_element_by_xpath("/html/body/header/nav/div/div/ul/li[2]/a").click()
        info = driver.find_elements_by_class_name("order_history_info")
        card = driver.find_elements_by_class_name("cart_product_stock_info")
        quantity = driver.find_elements_by_class_name("quantity_container")

        # print(info[0].text)
        
        # print(card[0].text)
        
        # print(quantity[0].text)

if __name__ == "__main__":
    unittest.main()
