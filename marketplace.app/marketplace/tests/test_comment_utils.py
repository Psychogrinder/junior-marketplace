from path_file import *


from testMethods import parseApiRoutes, replaceUserId, replaceProductId, getResponse, getCookiesFromResponse, getUserIdAndEntity

from marketplace.api_folder.utils.comment_utils import get_comment_by_id, get_comments_by_product_id, \
    get_comments_by_consumer_id, post_comment, delete_comment_by_id

import requests
import json

import unittest
from mock import Mock

class TestCase(unittest.TestCase):
    unittest.TestLoader.sortTestMethodsUsing = None

    def setUp(self):
        pass


    def test_get_comment(self):

        "TODO: сделать для всех продуктов"
        product_id = 1
        url = 'http://127.0.0.1:8000/api/v1/products/{}/comments'.format(product_id)

        response = requests.Session().get(url)
        data = json.loads(response.content)

        "TODO: для всех страниц"
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


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
