from path_file import *

from testing_utils import parseApiRoutes, replaceUserId, replaceProductId, getResponse, getCookiesFromResponse

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

    @unittest.skip
    def test_01_get_comment(self):

        "TODO: for all products"
        product_id = 1
        url = 'http://127.0.0.1:8000/api/v1/products/{}/comments'.format(product_id)

        response = requests.Session().get(url)

        data = json.loads(response.content)

        "TODO: for all pages (for two last comments now)"
        for comment in data['body']:
            self.assertEqual(product_id, comment['product_id'],
                             'id товара с комментарием  не соотвествует id карточки товара.')
            self.assertFalse(comment['body'].isspace(),
                             'пустое тело комментария (spaces/tabs/new line).')
            self.assertFalse(comment['consumer_name'].isspace(),
                             'пустое имя пользователя, оставившего комментарий (spaces/tabs/new line)')
            self.assertIsNotNone(comment['body'], 'комментарий is None.')


    @unittest.skip  #Статус заказа д.б. подтвержден, чтобы оставить отзыв
    def test_02_post_comment(self):
        login_url = 'http://127.0.0.1:8000/api/v1/login?email=42mail.ru&password=123123'
        s = requests.Session()
        response = s.post(login_url)

        user_id = json.loads(response.content)['id']

        product_id = 12

        url = 'http://127.0.0.1:8000/api/v1/products/{}/comments'.format(product_id)
        response = s.post(url, data={'body': 'Raise of naafss'})
        print(response)
        data = (json.loads(response.content))

        self.assertEqual(product_id, data['product_id'],
                         'id товара в опубликованном комментарии и id карточки товара различны.')
        self.assertEqual(user_id, data['consumer_id'],
                         'id авторизованного покупателя и id покупателя, опубликовавшего комментарий, различны.')
        self.assertIsNotNone(data['body'], 'posted comment body is None.')


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

    @unittest.skip
    def test_05_delete_comment_by_id(self):

        for product_id in [1, 99, -26]:

            try:
                comments = get_comments_by_product_id(product_id)

                if comments.items:
                    last_id = comments.items[-1].id
                    self.assertIsNotNone(get_comment_by_id(last_id))

                    delete_comment_by_id(last_id)
                    self.assertIsNone(get_comment_by_id(last_id),
                                      'комментарий не был удален (delete_comment_by_id)')
            except we.NotFound:
                pass


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
