import json
from testing_utils import getLoginResponse, getCookiesFromResponse, parseViews, replaceUserId, replaceProductId, login, logout

from marketplace.api_folder.utils.user_utils import get_user_by_email

from marketplace.api_folder.utils.consumer_utils import get_consumer_by_id, get_all_consumers, \
    post_consumer, put_consumer, delete_consumer_by_id, upload_consumer_image, get_all_consumers

from marketplace.models import Consumer, User
import requests
import unittest
from mock import Mock


class TestCase(unittest.TestCase):
    unittest.TestLoader.sortTestMethodsUsing = None
    
    def setUp(self):
        self.consumer = Mock()
        self.producer = Mock()
        # login data
        self.consumer.email = '10mail.ru'
        self.producer.email = 'example@mail.com'
        self.pw = '123123'
        self.product_id = 3

        # edit profile
        self.user_email = 'sd@kn.ru'

        self.base_url = 'http://127.0.0.1:8000'


    def test_01_post_consumer(self):
        args = {'email': self.user_email,
                'password': self.pw,
                'first_name': 'Abdullah',
                'last_name': 'Azamat',
                'phone_number': '21212121',
                'address': 'pushkin 82',
                }
        user = get_user_by_email(args['email'])

        if user:
            delete_consumer_by_id(user.id)
            print('Re-posted consumer')

        self.assertIn(post_consumer(args), get_all_consumers())


    def test_02_get_user_by_email(self):
        user = get_user_by_email(self.user_email)
        self.assertEqual(user.email, self.user_email)


    def test_03_get_consumer_by_id(self):
        user = get_user_by_email(self.user_email)

        consumer = get_consumer_by_id(user.id)
        self.assertEqual(consumer.id, user.id)


    @unittest.skip
    def test_04_put_consumer(self):
        url = 'http://127.0.0.1:8000/api/v1/consumers/'
        user = get_user_by_email(self.user_email)

        load_args = {
            'last_name': 'Bawbara',
            'first_name': 'JNf',
            'patronymic': 'Львоer',
            'phone_number': '71111111111',
            'address': 'Мойя1 Улиця 17@1#1',
        }

        login(user.email, '123123')
        response = requests.put(url + str(user.id), data=load_args)
        data = json.loads(response.content)
        print(data)

        for i in load_args:
            self.assertEqual(load_args[i], data[i])


    def test_05_delete_consumer_by_id(self):
        user = get_user_by_email(self.user_email)
        consumer = get_consumer_by_id(user.id)
        self.assertIn(consumer, get_all_consumers())

        delete_consumer_by_id(user.id)
        self.assertNotIn(consumer, get_all_consumers())


    def test_06_get_all_consumers(self):

        self.assertEqual(len(User.query.filter_by(entity='consumer').all()),
                         len(get_all_consumers()))



if __name__ == '__main__':
    unittest.main()