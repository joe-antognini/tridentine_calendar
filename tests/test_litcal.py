import datetime as dt
import unittest

from ..litcal import FeastLink
from ..litcal import LiturgicalCalendar


class TestFeastLink(unittest.TestCase):

    def test_init(self):
        feast_link = FeastLink('https://en.wikipedia.org/Saturnin', 'Saturnin')
        self.assertEqual(feast_link.url, 'https://en.wikipedia.org/Saturnin')
        self.assertEqual(feast_link.description, 'Saturnin')

    def test_from_json(self):
        json_obj = {
            'url': 'https://en.wikipedia.org/Saturnin',
            'description': 'Saturnin (Wikipedia)',
        }
        feast_link = FeastLink.from_json(json_obj)
        self.assertEqual(feast_link.url, 'https://en.wikipedia.org/Saturnin')
        self.assertEqual(feast_link.description, 'Saturnin (Wikipedia)')

        json_obj = 'https://en.wikipedia.org/Saturnin'
        feast_link = FeastLink.from_json(json_obj)
        self.assertEqual(feast_link.url, 'https://en.wikipedia.org/Saturnin')
        self.assertEqual(feast_link.description, 'Saturnin (Wikipedia)')

        json_obj = 'http://www.newadvent.org/cathen/01471a.htm'
        feast_link = FeastLink.from_json(json_obj, default='Saturninus')
        self.assertEqual(feast_link.url, 'http://www.newadvent.org/cathen/01471a.htm', 'Saturninus')
        self.assertEqual(feast_link.description, 'Saturninus (New Advent)')

    def test_to_href(self):
        feast_link = FeastLink('https://en.wikipedia.org/Saturnin', 'Saturnin (Wikipedia)')
        self.assertEqual(
            feast_link.to_href(),
            '<a href=https://en.wikipedia.org/Saturnin>Saturnin (Wikipedia)</a>',
        )


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
