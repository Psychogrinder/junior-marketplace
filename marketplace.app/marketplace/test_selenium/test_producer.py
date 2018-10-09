from append_path import *

from testing_utils import init_driver_and_display, uniqueEmail, uniqueShopName, login, logout, getPhoneMask, getEditElements, setDictValues, \
    getDataFromElements, setNewKeysForDict

from marketplace.models import User

import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.common import exceptions as ex


url = "http://127.0.0.1:8000"

driver, display = init_driver_and_display()

try:
    driver.get(url=url)
except ex.TimeoutException:
    print('url {} is not available'.format(url))

unique_email, unique_shop = uniqueEmail(), uniqueShopName()


class TestProducer(unittest.TestCase):

    def setUp(self):
        self.url = url
        self.producer = User.query.filter_by(entity='producer').order_by(User.id.desc()).first()

        self.password = "123123"
        self.reg_data = {"email": unique_email,
                         "password": self.password,
                         "shop_name": unique_shop,
                         "contact": "АллА бОрисовна Дергачева",
                         "phone": "9991234455",
                         "address": "hahha ya tut zhivu 15",
                         "desc": ""}


    def test_01_get_home_page(self):
        driver.get(self.url)
        self.assertIn('маркетплейс', driver.title.lower(), 'no name of marketplace in the website title')


    def test_02_producer_open_registration_page(self):
        driver.find_element_by_css_selector(
            "div.col-12:nth-child(2) > p:nth-child(2) > a:nth-child(1)").click()
        self.assertIsNotNone(driver.find_element_by_id("registrationProducer")) #button reg


    def test_03_producer_enter_registrtion_data(self):
        data = self.reg_data
        driver.find_element_by_id("emailRegProducer").send_keys(data["email"])
        driver.find_element_by_id("passwordRegProducer").send_keys(data["password"])
        driver.find_element_by_id("rePasswordRegProducer").send_keys(data["password"])
        driver.find_element_by_id("nameRegProducer").send_keys(data["shop_name"])
        driver.find_element_by_id("contactPersonRegProducer").send_keys(data["contact"])
        driver.find_element_by_id("phoneRegProducer").send_keys(data["phone"])
        driver.find_element_by_id("addressRegProducer").send_keys(data["address"])
        driver.find_element_by_id("descriptionRegProducer").send_keys(data["desc"])



    def test_04_producer_submit_form(self):
        driver.find_element_by_id("registrationProducer").click()

        user_menu = None
        try:
            user_menu = Wait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/header/nav/div/div/div/button"))
            )
        finally:
            self.assertIsNotNone(user_menu, "producer is not logined after registration")


    # def test_05_producer_open_catalog(self):
    #     driver.find_element_by_xpath("/html/body/footer/div/div/div[1]/p[1]/a").click()


    def test_06_producer_logout(self):
        logout(driver)
        btn_auth = None
        try:
            btn_auth = Wait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".header-login > img:nth-child(1)"))
            )
        finally:
            self.assertIsNotNone(btn_auth, "no auth button after logout")


    def test_07_producer_login(self):
        email, pw = self.reg_data["email"], self.reg_data["password"]
        login(driver, email, pw)
        self.assertIsNotNone(driver.find_element_by_css_selector("button.btn:nth-child(1)")) #user menu button


    def test_08_producer_open_edit_profile(self):
        driver.find_element_by_css_selector(".dropdown-toggle").click()  # user menu
        driver.find_element_by_css_selector("a.dropdown-item:nth-child(1)").click()  # go to profile
        self.assertIn("редактировать", driver.find_element_by_xpath("/html/body/main/div[2]/div/p").text.lower())
        self.assertIsNotNone(driver.find_element_by_css_selector("button.btn:nth-child(1)")) #is still logined


    def test_09_producer_profile_is_data_correct(self):
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


    #TODO add edit case


    def test_10_producer_open_the_delete_page(self):
        driver.find_element_by_css_selector(".edit-profile > a:nth-child(1)").click() #edit button
        driver.find_element_by_css_selector(".out-of-stock > a:nth-child(1)").click() # go to modal delete

        btn_cancel = driver.find_element_by_xpath("/html/body/div[5]/div/div/div[3]/button[1]")
        btn_delete = driver.find_element_by_id("deleteProducerBtn")

        self.assertIsNotNone(btn_cancel, "can not find cancel button")
        self.assertIn("отменить", btn_cancel.text.lower())

        self.assertIsNotNone(btn_delete, "can not find delete button")
        self.assertIn("удалить", btn_delete.text.lower())


        # TODO cancel button click; attach id to the button
        # driver.find_element_by_xpath("/html/body/div[5]/div/div/div[3]/button[1]").click()
        # driver.find_element_by_css_selector(
        #     "deleteProfileProducer > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > button:nth-child(1)")\
        #     .click()


    def test_11_producer_delete_confirm(self):
        driver.find_element_by_id("deleteProducerBtn").click()
        self.assertIsNone(User.query.filter_by(id=self.producer.id).first())


    def the_end(self):
        driver.quit()
        display.stop()


if __name__ == "__main__":
    unittest.main()
