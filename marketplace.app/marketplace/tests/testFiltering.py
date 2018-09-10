from path_file import *

from testMethods import getCategorySlugs, getResponse, getResponseCode, parseApiRoutes

from marketplace.api_folder.utils.product_utils import get_sorted_and_filtered_products

import unittest


def is_price_sorted(list, price_sort):
    if price_sort == 'up':
        return all(a <= b for a, b in zip(list, list[1:]))
    elif price_sort == 'down':
        return all(a >= b for a, b in zip(list, list[1:]))


def check_price(sorted, args_price):
    price_in_slug = []

    for product in sorted:
        if ' ₽' in product['price']:
            price = product['price'][:-2]
        else:
            price = product['price']
        price_in_slug.append(float(price))

    if price_in_slug:
        return is_price_sorted(price_in_slug, args_price)
    else:
        return True


class TestCase(unittest.TestCase):
    unittest.TestLoader.sortTestMethodsUsing = None

    def setUp(self):

        self.args = {'popularity': None,    #down
                     'price': None,         #down, up
                     'category_name': None, #slugs
                     'producer_name': None,
                     'in_stock': None,      #1 
        }

        self.slugs = getCategorySlugs()


    def test_filtered_price(self):

        args = self.args

        for slug in self.slugs:
            args['category_name'] = slug

            args['price'] = 'down'
            sorted = get_sorted_and_filtered_products(args)
            self.assertEqual(True, check_price(sorted, args['price']))


            args['price'] = 'up'
            sorted = get_sorted_and_filtered_products(args)
            self.assertEqual(True, check_price(sorted, args['price']))




if __name__ == '__main__':
    unittest.main()
