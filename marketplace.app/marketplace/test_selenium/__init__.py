from test_authorize import Authorization
import unittest
from testing_utils import logout


auth = unittest.TestLoader().loadTestsFromTestCase(Authorization)
# test_suite = unittest.TestSuite([auth])

unittest.TextTestRunner(verbosity=2).run(auth)
