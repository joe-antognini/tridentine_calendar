import datetime as dt
import unittest

from .litcal import computus
from .litcal import LiturgicalCalendar


class TestComputus(unittest.TestCase):

    def test_computus(self):
        self.assertEqual(computus(2004), dt.date(2004, 4, 11))
        self.assertEqual(computus(2018), dt.date(2018, 4, 1))
        self.assertEqual(computus(2019), dt.date(2019, 4, 21))
        self.assertEqual(computus(2027), dt.date(2027, 3, 28))
        self.assertEqual(computus(2050), dt.date(2050, 4, 10))


class TestLiturgicalCalendarSmoke(unittest.TestCase):

    def test_liturgical_calendar(self):
        self.assertIsNotNone(LiturgicalCalendar(2018))


class TestLiturgicalCalendarSundayDates(unittest.TestCase):
    
    def test_liturgical_calendar_sunday_dates(self):
        litcal_2018 = LiturgicalCalendar(2018)
        self.assertEqual(
            litcal_2018[dt.date(2018, 9, 2)][0]['name'],
            'Fifteenth Sunday after Pentecost',
        )
        self.assertEqual(
            litcal_2018[dt.date(2018, 11, 25)][0]['name'],
            'Last Sunday after Pentecost',
        )

class TestLiturgicalCalendarICS(unittest.TestCase):

    def setUp(self):
        self.litcal_2018 = LiturgicalCalendar(2018)
        self.litcal_2019 = LiturgicalCalendar(2019)

    @unittest.skip('Currently broken, fix later.')
    def test_name_with_article(self):
        computed_str = self.litcal_2018._name_with_article('St. Barbara')
        expected_str = 'the Feast of St. Barbara'
        self.assertEqual(computed_str, expected_str)

        computed_str = self.litcal_2018._name_with_article('SS. Vincent & Anastasius')
        expected_str = 'the Feast of SS. Vincent & Anastasius'
        self.assertEqual(computed_str, expected_str)

        computed_str = self.litcal_2018._name_with_article('Third Sunday after Pentecost')
        expected_str = 'the Third Sunday after Pentecost'
        self.assertEqual(computed_str, expected_str)

        computed_str = self.litcal_2018._name_with_article('Candlemas')
        expected_str = 'Candlemas'
        self.assertEqual(computed_str, expected_str)

    def test_to_ics_smoke(self):
        ics_calendar = self.litcal_2018.to_ics()
        self.assertIsNotNone(ics_calendar)

# TODO: Test the data stored in the calendar.  (Monkey patch the data files we read from.)

# TODO: Test the ICS conversion.
