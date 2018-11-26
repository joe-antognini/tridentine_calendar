import datetime as dt
import unittest

from litcal import *


class TestComputus(unittest.TestCase):

    def test_computus(self):
        self.assertEqual(computus(2004), dt.date(2004, 4, 11))
        self.assertEqual(computus(2018), dt.date(2018, 4, 1))
        self.assertEqual(computus(2019), dt.date(2019, 4, 21))
        self.assertEqual(computus(2027), dt.date(2027, 3, 28))
        self.assertEqual(computus(2050), dt.date(2050, 4, 10))
