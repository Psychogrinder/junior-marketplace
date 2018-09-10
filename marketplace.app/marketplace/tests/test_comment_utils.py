from path_file import *


from testMethods import parseApiRoutes, replaceUserId, replaceProductId, getResponse, getCookiesFromResponse, getUserIdAndEntity

from marketplace.api_folder.utils.comment_utils import get_comment_by_id, get_comments_by_product_id, \
    get_comments_by_consumer_id, post_comment, delete_comment_by_id

import unittest
from mock import Mock

class TestCase(unittest.TestCase):
    unittest.TestLoader.sortTestMethodsUsing = None

    def setUp(self):

        self.routes = parseApiRoutes('../api_routes.py')
        self.consumer = Mock()
        self.producer = Mock()

        self.consumer.email = '2mail.ru'
        self.producer.email = 'fabiola.thomas@example.com'
        self.pw = '123123'



    def test_post_comment(self):
        import requests
        url = 'http://127.0.0.1:8000/api/v1/'


        s = '{}/{}/{}'
        s.format('consumers', id, 'comments')

        #user_id, user_entity = getUserIdAndEntity(response)

        #response = requests.Session().post(url)
        #data = json.loads(response.content)

        routes = self.routes['comments']

        test_url = url + routes[1]
        test_url.replace()
        print(test_url)



        # response = requests.Session().put(url + str(user.id), data=load_args)
        # data = json.loads(response.content)







if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
