import datetime as dt
import unittest

from litcal.litcal import LiturgicalCalendar


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

    def test_to_ics_smoke(self):
        ics_calendar = self.litcal_2018.to_ics()
        self.assertIsNotNone(ics_calendar)

# TODO: Test the data stored in the calendar.  (Monkey patch the data files we read from.)

# TODO: Test the ICS conversion.
