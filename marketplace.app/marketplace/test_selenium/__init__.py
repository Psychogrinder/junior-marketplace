from test_authorize import Authorization
from test_products import TestProducts
from test_consumer import TestConsumer
from test_producer import TestProducer
import unittest


auth = unittest.TestLoader().loadTestsFromTestCase(Authorization)
order = unittest.TestLoader().loadTestsFromTestCase(TestProducts)
consumer = unittest.TestLoader().loadTestsFromTestCase(TestConsumer)
producer = unittest.TestLoader().loadTestsFromTestCase(TestProducer)


test_suite = unittest.TestSuite([auth, order, consumer, producer])


unittest.TextTestRunner(verbosity=2).run(test_suite)
