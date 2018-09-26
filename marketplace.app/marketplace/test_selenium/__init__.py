from test_authorize import Authorization
from test_products import TestOrder
from test_consumer import TestConsumer
import unittest

auth = unittest.TestLoader().loadTestsFromTestCase(Authorization)
order = unittest.TestLoader().loadTestsFromTestCase(TestOrder)
consumer = unittest.TestLoader().loadTestsFromTestCase(TestConsumer)

test_suite = unittest.TestSuite([auth, order, consumer])

unittest.TextTestRunner(verbosity=2).run(test_suite)
