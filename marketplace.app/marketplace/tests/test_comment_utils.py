from path_file import *

from testing_utils import parseApiRoutes, replaceUserId, replaceProductId, getResponse, getCookiesFromResponse

from marketplace.api_folder.utils.comment_utils import get_comment_by_id, get_comments_by_product_id, \
    get_comments_by_consumer_id, post_comment, delete_comment_by_id

from marketplace.api_folder.utils.order_utils import get_orders_by_consumer_id, get_filtered_orders
import requests
import json

import unittest
import werkzeug.exceptions as we

class TestCase(unittest.TestCase):
    unittest.TestLoader.sortTestMethodsUsing = None

    def setUp(self):
        self.ids = [1, 2, 3, 5, 0, 10, 15, 40, 60, -1, 100, 10000, -11.0]

    @unittest.skip # FIXME add more args
    def test_01_get_comment(self):

        "TODO: for all products"
        product_id = 1
        url = 'http://127.0.0.1:8000/api/v1/comments'

        response = requests.Session().get(url)
        data = json.loads(response.content)

        #TODO: for all pages (for two last comments now)
        for comment in data['body']:
            self.assertEqual(product_id, comment['product_id'],
                             'id товара с комментарием  не соотвествует id карточки товара.')
            self.assertFalse(comment['body'].isspace(),
                             'пустое тело комментария (spaces/tabs/new line).')
            self.assertFalse(comment['consumer_name'].isspace(),
                             'пустое имя пользователя, оставившего комментарий (spaces/tabs/new line)')
            self.assertIsNotNone(comment['body'], 'комментарий is None.')


    def test_02_post_comment(self):
        login_url = 'http://127.0.0.1:8000/api/v1/login?email=42mail.ru&password=123123'
        s = requests.Session()
        response = s.post(login_url)
        user_id = json.loads(response.content)['id']
        orders = get_orders_by_consumer_id(user_id)

        product_id, order_id = False, False
        for order in orders:
            if order.status == 'Завершён':
                for key in order.order_items_json:
                    product_id = key
                    order_id = order.id

        if product_id and order_id:
            url = 'http://127.0.0.1:8000/api/v1/comments'
            response = s.post(url, data={'consumer_id': user_id,
                                         'product_id': product_id,
                                         'order_id': order_id,
                                         'body': 'Raise of NASA'}
            )
            data = json.loads(response.content)
            print(data)


    def test_03_get_comment_by_id(self):

        for comment_id in self.ids:
            try:
                comment = get_comment_by_id(comment_id)
                self.assertEqual(comment_id, comment.id)
            except we.NotFound:
                pass


    def test_04_get_comments_by_product_id(self):

        for product_id in self.ids:
            try:
                comments = get_comments_by_product_id(product_id)
                total, items = False, False

                if comments.total and comments.items:
                    total, items = True, True

                self.assertEqual(total, items)
            except we.NotFound:
                pass


    def test_05_delete_comment_by_id(self):

        for product_id in [1, 99, -26]:
            try:
                comments = get_comments_by_product_id(product_id)

                if comments.items:
                    last_id = comments.items[-1].id
                    self.assertIsNotNone(get_comment_by_id(last_id))

                    delete_comment_by_id(last_id)
                    print('deleted comment')
                    self.assertIsNone(get_comment_by_id(last_id),
                                      'комментарий не был удален (delete_comment_by_id)')
            except we.NotFound:
                pass


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)