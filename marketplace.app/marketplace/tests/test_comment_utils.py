from path_file import *

from testMethods import parseApiRoutes, replaceUserId, replaceProductId, getResponse, getCookiesFromResponse, getUserIdAndEntity

from marketplace.api_folder.utils.comment_utils import get_comment_by_id, get_comments_by_product_id, \
    get_comments_by_consumer_id, post_comment, delete_comment_by_id

import requests
import json

import unittest
import werkzeug.exceptions as we

class TestCase(unittest.TestCase):
    unittest.TestLoader.sortTestMethodsUsing = None

    def setUp(self):
        self.ids = [1, 2, 3, 5, 0, 10, 15, 40, 60, -1, 100, 10000, -11.0]


    def test_get_comment(self):

        "TODO: for all products"
        product_id = 1
        url = 'http://127.0.0.1:8000/api/v1/products/{}/comments'.format(product_id)

        response = requests.Session().get(url)
        data = json.loads(response.content)

        "TODO: for all pages"
        for comment in data['body']:
            self.assertEqual(product_id, comment['product_id'],
                             'id товара с комментарием  не соотвествует id карточки товара.')
            self.assertFalse(comment['body'].isspace(),
                             'пустое тело комментария (пробелы/tab/new line).')
            self.assertFalse(comment['consumer_name'].isspace(),
                             'пустое имя пользователя, оставившего комментарий (пробелы/tab/new line)')
            self.assertIsNotNone(comment['body'], 'комментарий is None.')


    def test_post_comment(self):

        login_url = 'http://127.0.0.1:8000/api/v1/login?email=10mail.ru&password=123123'
        s = requests.Session()

        user_id = json.loads(s.post(login_url).content)['id']
        product_id = 3
        url = 'http://127.0.0.1:8000/api/v1/products/{}/comments'.format(product_id)

        response = s.post(url, data={'body': 'Raise of naa'})
        data = json.loads(response.content)

        self.assertEqual(product_id, data['product_id'],
                         'id товара в опубликованном комментарии и id карточки товара различны.')
        self.assertEqual(user_id, data['consumer_id'],
                         'id авторизованного покупателя и id покупателя, опубликовавшего комментарий, различны.')
        self.assertIsNotNone(data['body'], 'posted comment body is None.')


    def test_get_comment_by_id(self):

        for comment_id in self.ids:
            try:
                comment = get_comment_by_id(comment_id)
                self.assertEqual(comment_id, comment.id)
            except we.NotFound:
                pass


    def test_get_comments_by_product_id(self):

        for product_id in self.ids:
            try:
                comments = get_comments_by_product_id(product_id)
                total, items = False, False

                if comments.total and comments.items:
                    total, items = True, True

                self.assertEqual(total, items)
            except we.NotFound:
                pass




if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
