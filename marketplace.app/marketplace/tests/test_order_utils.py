from path_file import *



from marketplace.api_folder.utils.order_utils import get_order_by_id, get_products_by_order_id


import requests, json
import unittest
import werkzeug.exceptions as we


class TestCase(unittest.TestCase):
    unittest.TestLoader.sortTestMethodsUsing = None

    def setUp(self):
        pass


    def test_get_order_by_id(self):

        for order_id in [1, 0, 10, -10, 50, 100]:
            try:
                if order_id:
                    self.assertIsNotNone(get_order_by_id(order_id))
                else:
                    self.assertIsNone(get_order_by_id(order_id))

            except we.NotFound:
                pass

    #TODO: add to cart products, change status and compare products from order and cart
    def test_get_products_by_order_id(self):
        products_from_order = get_products_by_order_id(5)

        for product in products_from_order:
            pass
            # product.name
            # product.id
            # product.producer_id
            # product.category_id
            # product.price
            # product.measurement_unit


if __name__ == '__main__':
    unittest.main()
