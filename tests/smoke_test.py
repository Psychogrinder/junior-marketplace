#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
#import sparkey
import pytest
import unittest
import urllib.request

class TestSmoke(unittest.TestCase):

    def setUp(self):
        self.url = "http://127.0.0.1:5000/"

    def testConnection(self):
        self.assertEqual(200, (urllib.request.urlopen(self.url).getcode()))



if __name__ == '__main__':
    unittest.main()