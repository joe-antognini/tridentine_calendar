import datetime as dt
import unittest

from ..utils import add_domain_to_url_description
from ..utils import feria_name
from ..utils import get_movable_feast_names_and_dates
from ..utils import iterate_liturgical_year
from ..utils import liturgical_year
from ..utils import liturgical_year_end
from ..utils import liturgical_year_start
from ..utils import make_initial__the__lowercase


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

    def test_iterate_liturgical_year(self):
        for i, date in enumerate(iterate_liturgical_year(2018)):
            if i == 0:
                self.assertEqual(date, liturgical_year_start(2018))
        self.assertEqual(date, liturgical_year_end(2018))


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


class TestGetMovableFeastNamesAndDates(unittest.TestCase):

    def test_get_movable_feast_names_and_dates(self):
        feast_names_and_dates = list(get_movable_feast_names_and_dates(2019))
        self.assertTrue(feast_names_and_dates != [])


class TestMakeInitial_The_Lowercase(unittest.TestCase):

    def test_make_initial__the__lowercase(self):
        s = 'Hello World'
        self.assertEqual(make_initial__the__lowercase(s), 'Hello World')

        s = 'The Hello World'
        self.assertEqual(make_initial__the__lowercase(s), 'the Hello World')

        s = 'There Hello World'
        self.assertEqual(make_initial__the__lowercase(s), 'There Hello World')

        s = 'To Hello World'
        self.assertEqual(make_initial__the__lowercase(s), 'To Hello World')
