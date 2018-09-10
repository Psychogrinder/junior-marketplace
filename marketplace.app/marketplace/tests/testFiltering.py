from path_file import *

from testMethods import getCategorySlugs, getResponse, getResponseCode, parseApiRoutes

from marketplace.api_folder.utils.product_utils import get_sorted_and_filtered_products

from marketplace.api_folder.utils.producer_utils import get_all_producers

import unittest


class TestCase(unittest.TestCase):
    unittest.TestLoader.sortTestMethodsUsing = None

    def setUp(self):

        self.args = {'popularity': None,    # down
                     'price': None,         # down, up
                     'category_name': None, # slugs
                     'producer_name': None,
                     'in_stock': None,      # 1
        }


    def test_filtered_price(self):
        args = self.args
        self.slugs = getCategorySlugs()

        for slug in self.slugs:
            args['category_name'] = slug

            args['price'] = 'down'
            sorted = get_sorted_and_filtered_products(args)
            self.assertTrue(check_price(sorted, args['price']), 'Problem with DOWN sorting price')

            args['price'] = 'up'
            sorted = get_sorted_and_filtered_products(args)
            self.assertTrue(check_price(sorted, args['price']), 'Problem with UP sorting price')


    def test_filtered_by_producer(self):
        args = self.args

        producers = get_all_producers()

        for producer in producers:

            args['producer_name'] = producer.name
            sorted = get_sorted_and_filtered_products(args)

            for prod in range(len(sorted)):
                self.assertEqual(producer.name, sorted[prod]['producer_name'])


    def test_filtered_popularity(self):
        args = self.args


    def suite(self):
        return suite



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
