from testing_utils import getCategorySlugs, is_price_sorted, check_price, parseRoutes, \
    get_route_by_name

from marketplace.api_folder.utils.product_utils import get_sorted_and_filtered_products
from marketplace.api_folder.utils.producer_utils import get_all_producers

import unittest
import requests


class TestCase(unittest.TestCase):
    unittest.TestLoader.sortTestMethodsUsing = None

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/v1'
        self.routes = parseRoutes()
        self.args = {'popularity': None,    # down
                     'price': None,         # down, up
                     'category_name': None, # slugs
                     'producer_name': None,
                     'in_stock': None,      # 1
                     'search': None,
                     'page': 1,
                     'next_page': 2,

                     }


    def test_01_filtered_price(self):
        args = self.args
        args['parent_id'] = 0

        self.slugs = getCategorySlugs(args)

        for slug in self.slugs:
            args['category_name'] = slug

            args['price'] = 'down'
            sorted = get_sorted_and_filtered_products(args)
            self.assertTrue(check_price(sorted, args['price']), 'Problem with DOWN sorting price')

            args['price'] = 'up'
            sorted = get_sorted_and_filtered_products(args)
            self.assertTrue(check_price(sorted, args['price']), 'Problem with UP sorting price')


    def test_02_filtered_by_producer(self):
        args = self.args
        producers = get_all_producers()

        for producer in producers:

            args['producer_name'] = producer.name
            sorted = get_sorted_and_filtered_products(args)

            for product in range(len(sorted)):
                self.assertEqual(producer.name, sorted['products'][product]['producer_name'])


    def test_03_search(self):
        routes = self.routes['Products']
        url = self.url + get_route_by_name(routes, 'search') + '&find='

        response = requests.get(url+"голень")

        print(response.content)



    def suite(self):
        return suite



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
