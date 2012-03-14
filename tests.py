#!/usr/bin/env python

import unittest
import webalin

class WebalinTests(unittest.TestCase):
    def test_main(self):
        w = webalin.Webalin()
        results = w.analyze('http://dmpayton.com')
        print results


if __name__ == '__main__':
    unittest.main()
