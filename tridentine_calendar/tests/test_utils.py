import datetime as dt
import unittest

from ..utils import add_domain_to_url_description
from ..utils import computus
from ..utils import feria_name
from ..utils import liturgical_year
from ..utils import liturgical_year_end
from ..utils import liturgical_year_start


class TestComputus(unittest.TestCase):

    def test_computus(self):
        self.assertEqual(fd.computus(2004), dt.date(2004, 4, 11))
        self.assertEqual(fd.computus(2018), dt.date(2018, 4, 1))
        self.assertEqual(fd.computus(2019), dt.date(2019, 4, 21))
        self.assertEqual(fd.computus(2027), dt.date(2027, 3, 28))
        self.assertEqual(fd.computus(2050), dt.date(2050, 4, 10))


class TestLiturgicalYearStartEnd(unittest.TestCase):

    def test_liturgical_year_start_date(self):
        self.assertEqual(liturgical_year_start(2004), dt.date(2003, 11, 30))
        self.assertEqual(liturgical_year_start(2018), dt.date(2017, 12, 3))
        self.assertEqual(liturgical_year_start(2019), dt.date(2018, 12, 2))

    def test_liturgical_year_end_date(self):
        self.assertEqual(liturgical_year_end(2004), dt.date(2004, 11, 27))
        self.assertEqual(liturgical_year_end(2018), dt.date(2018, 12, 1))
        self.assertEqual(liturgical_year_end(2019), dt.date(2019, 11, 30))

    def test_liturgical_year(self):
        self.assertEqual(liturgical_year(dt.date(2018, 1, 25)), 2018)
        self.assertEqual(liturgical_year(dt.date(2018, 12, 25)), 2019)

        self.assertEqual(liturgical_year(dt.date(2018, 12, 2)), 2019)
        self.assertEqual(liturgical_year(dt.date(2018, 12, 1)), 2018)


class TestFeriaName(unittest.TestCase):

    def test_feria_name(self):
        name = feria_name(dt.date(2019, 3, 11))
        self.assertEqual(name, 'Monday in the first week of Lent')


class TestAddDomainToUrlDescription(unittest.TestCase):

    def test_add_domain_to_url_description(self):
        url = 'https://en.wikipedia.org/Saturnin'
        output = add_domain_to_url_description(url, 'Saturnin')
        self.assertEqual(output, 'Saturnin (Wikipedia)')

        url = 'http://www.newadvent.org/cathen/01471a.htm'
        output = add_domain_to_url_description(url, 'Saturninus')
        self.assertEqual(output, 'Saturninus (New Advent)')
