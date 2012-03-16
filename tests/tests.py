#!/usr/bin/env python

import code
import os
import sys
import unittest

## Patch sys.path to pull webalin from this checkout
TEST_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(TEST_ROOT))

import webalin

class WebalinTests(unittest.TestCase):
    def load_document(self, name):
        path = os.path.join(TEST_ROOT, 'resources', '{0}.html'.format(name))
        with open(path, 'r') as document:
            return document.read()

    def test_accessible(self, tests=None):
        markup = self.load_document('accessible')
        w = webalin.Webalin()
        results = w.analyze(markup, tests)
        self.assertEqual(len(results), 0)

    def test_inaccessible(self, tests=None):
        markup = self.load_document('inaccessible')
        w = webalin.Webalin()
        results = w.analyze(markup, tests)
        self.assertGreater(len(results), 0)





if __name__ == '__main__':
    unittest.main()
