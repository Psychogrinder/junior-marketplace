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


    @unittest.skip #return only last product from order
    def test_get_products_by_order_id(self):
        products = get_products_by_order_id(6)
        print((products))

if __name__ == '__main__':
    unittest.main()
