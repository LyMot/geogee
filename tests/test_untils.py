#!/usr/bin/env python

"""Tests for `geogee` package.

References: 
https://youtu.be/6tNS--WetLI
https://github.com/CoreyMSchafer/code_snippets/blob/master/Python-Unit-Testing/test_calc.py
https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug
https://realpython.com/python-testing

"""

import os
import unittest

from geogee import geogee
from geogee import  utils


class Testgeogee(unittest.TestCase):
    """Tests for `geogee` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        print("setUp")
        self.in_shp = os.path.abspath("examples/data/countries.shp")

    def tearDown(self):
        """Tear down test fixtures, if any."""
        print("tearDown\n")

    def test_random_string(self):
        print("test_random_string")
        self.assertEqual(len(utils.random_string(3)), 3)

    def test_add(self):
        print("test_add")
        self.assertEqual(utils.add(-1, 1), 0)
        self.assertEqual(utils.add(-1, -1), -2)
        self.assertEqual(utils.add(10, 5), 15)

    def test_subtract(self):
        print("test_subtract")
        self.assertEqual(utils.subtract(10, 5), 5)
        self.assertEqual(utils.subtract(-1, 1), -2)
        self.assertEqual(utils.subtract(-1, -1), 0)

    def test_multiply(self):
        print("test_multiply")
        self.assertEqual(utils.multiply(10, 5), 50)
        self.assertEqual(utils.multiply(-1, 1), -1)
        self.assertEqual(utils.multiply(-1, -1), 1)

    def test_divide(self):
        print("test_divide")
        self.assertEqual(utils.divide(10, 5), 2)
        self.assertEqual(utils.divide(-1, 1), -1)
        self.assertEqual(utils.divide(-1, -1), 1)
        self.assertEqual(utils.divide(5, 2), 2.5)

        with self.assertRaises(ValueError):
            utils.divide(10, 0)

    def test_shp_to_geojson(self):
        print("test_shp_to_geojson")
        self.assertIsInstance(geogee.shp_to_geojson(self.in_shp), dict)


if __name__ == '__main__':
    unittest.main()