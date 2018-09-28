from test_products import TestProducts
from test_consumer import TestConsumer
from test_producer import TestProducer
import unittest


products = unittest.TestLoader().loadTestsFromTestCase(TestProducts)
consumer = unittest.TestLoader().loadTestsFromTestCase(TestConsumer)
producer = unittest.TestLoader().loadTestsFromTestCase(TestProducer)


test_suite = unittest.TestSuite([products, consumer, producer])


unittest.TextTestRunner(verbosity=2).run(test_suite)
