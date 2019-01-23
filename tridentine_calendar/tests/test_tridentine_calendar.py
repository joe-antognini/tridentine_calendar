import datetime as dt
import unittest

from ..tridentine_calendar import LiturgicalCalendar
from ..tridentine_calendar import LiturgicalCalendarEvent
from ..tridentine_calendar import LiturgicalCalendarEventUrl
from ..tridentine_calendar import LiturgicalSeason


class TestLiturgicalCalendarEventUrl(unittest.TestCase):

    def test_init(self):
        feast_link = LiturgicalCalendarEventUrl('https://en.wikipedia.org/Saturnin', 'Saturnin')
        self.assertEqual(feast_link.url, 'https://en.wikipedia.org/Saturnin')
        self.assertEqual(feast_link.description, 'Saturnin')

    def test_from_json(self):
        json_obj = {
            'url': 'https://en.wikipedia.org/Saturnin',
            'description': 'Saturnin',
        }
        feast_link = LiturgicalCalendarEventUrl.from_json(json_obj)
        self.assertEqual(feast_link.url, 'https://en.wikipedia.org/Saturnin')
        self.assertEqual(feast_link.description, 'Saturnin (Wikipedia)')

        json_obj = 'https://en.wikipedia.org/Saturnin'
        feast_link = LiturgicalCalendarEventUrl.from_json(json_obj)
        self.assertEqual(feast_link.url, 'https://en.wikipedia.org/Saturnin')
        self.assertEqual(feast_link.description, 'Saturnin (Wikipedia)')

        json_obj = 'http://www.newadvent.org/cathen/01471a.htm'
        feast_link = LiturgicalCalendarEventUrl.from_json(json_obj, default='Saturninus')
        self.assertEqual(feast_link.url, 'http://www.newadvent.org/cathen/01471a.htm')
        self.assertEqual(feast_link.description, 'Saturninus (New Advent)')

        json_obj = 'https://fisheaters.com/customsadvent2a.html'
        feast_link = LiturgicalCalendarEventUrl.from_json(json_obj, default='St. Barbara')
        self.assertEqual(feast_link.url, 'https://fisheaters.com/customsadvent2a.html')
        self.assertEqual(feast_link.description, 'St. Barbara (Fish Eaters)')

        json_obj = 'https://en.wikipedia.org/Saint_Nicholas'
        feast_link = LiturgicalCalendarEventUrl.from_json(json_obj)
        self.assertEqual(feast_link.url, 'https://en.wikipedia.org/Saint_Nicholas')
        self.assertEqual(feast_link.description, 'Saint Nicholas (Wikipedia)')

        json_obj = 'https://en.wikipedia.org/wiki/Saint_Sylvester%27s_Day'
        feast_link = LiturgicalCalendarEventUrl.from_json(json_obj)
        self.assertEqual(feast_link.url, 'https://en.wikipedia.org/wiki/Saint_Sylvester%27s_Day')
        self.assertEqual(feast_link.description, 'Saint Sylvester\'s Day (Wikipedia)')

    def test_to_href(self):
        feast_link = LiturgicalCalendarEventUrl(
            'https://en.wikipedia.org/Saturnin', 'Saturnin (Wikipedia)')
        self.assertEqual(
            feast_link.to_href(),
            '<a href=https://en.wikipedia.org/Saturnin>Saturnin (Wikipedia)</a>',
        )


class TestLiturgicalCalendarSeason(unittest.TestCase):

    def test_init(self):
        season = LiturgicalSeason('Advent')
        self.assertEqual(season.name, 'Advent')

    def test_from_json_key(self):
        season = LiturgicalSeason.from_json_key('Advent')
        self.assertEqual(season.name, 'Advent')
        self.assertEqual(season.color, 'Violet')

    def test_from_date(self):
        date = dt.date(2018, 12, 4)
        season = LiturgicalSeason.from_date(date)
        self.assertEqual(season.name, 'Advent')
        self.assertEqual(season.color, 'Violet')

        date = dt.date(2018, 12, 25)
        season = LiturgicalSeason.from_date(date)
        self.assertEqual(season.name, 'Christmastide')
        self.assertEqual(season.color, 'White')

        date = dt.date(2019, 1, 25)
        season = LiturgicalSeason.from_date(date)
        self.assertEqual(season.name, 'Time after Epiphany')
        self.assertEqual(season.color, 'Green')

        date = dt.date(2019, 2, 25)
        season = LiturgicalSeason.from_date(date)
        self.assertEqual(season.name, 'Septuagesima')
        self.assertEqual(season.color, 'Violet')

        date = dt.date(2019, 3, 25)
        season = LiturgicalSeason.from_date(date)
        self.assertEqual(season.name, 'Lent')
        self.assertEqual(season.color, 'Violet')

        date = dt.date(2019, 4, 8)
        season = LiturgicalSeason.from_date(date)
        self.assertEqual(season.name, 'Passiontide')
        self.assertEqual(season.color, 'Violet')

        date = dt.date(2019, 4, 15)
        season = LiturgicalSeason.from_date(date)
        self.assertEqual(season.name, 'Holy Week')
        self.assertEqual(season.color, 'Violet')

        date = dt.date(2019, 4, 25)
        season = LiturgicalSeason.from_date(date)
        self.assertEqual(season.name, 'Eastertide')
        self.assertEqual(season.color, 'White')

        date = dt.date(2019, 6, 25)
        season = LiturgicalSeason.from_date(date)
        self.assertEqual(season.name, 'Time after Pentecost')
        self.assertEqual(season.color, 'Green')

        date = dt.date(2019, 11, 2)
        season = LiturgicalSeason.from_date(date)
        self.assertEqual(season.name, 'Hallowtide')

    def test_full_name(self):
        season = LiturgicalSeason('Advent')
        self.assertEqual(season.full_name(capitalize=True), 'Advent')

        season = LiturgicalSeason('Time after Pentecost')
        self.assertEqual(season.full_name(capitalize=True), 'The Time after Pentecost')

        season = LiturgicalSeason('Time after Epiphany')
        self.assertEqual(season.full_name(capitalize=False), 'the Time after Epiphany')


class TestLiturgicalCalendarEvent(unittest.TestCase):

    def test_from_json_st_nicholas(self):
        date = dt.date(2018, 12, 6)
        json_obj = {
            'name': 'St. Nicholas',
            'titles': ['Bishop', 'Confessor'],
            'urls': [
                'https://fisheaters.com/customsadvent3.html',
                'https://en.wikipedia.org/wiki/Saint_Nicholas',
            ],
            'obligation': False,
            'class': 3,
            'liturgical_event': True,
        }
        event = LiturgicalCalendarEvent.from_json(date, json_obj)

        self.assertEqual(event.name, 'St. Nicholas')
        self.assertEqual(event.rank, 3)
        self.assertEqual(event.liturgical_event, True)
        self.assertEqual(event.holy_day, False)
        self.assertEqual(event.urls[0].description, 'St. Nicholas (Fish Eaters)')
        self.assertEqual(event.urls[1].description, 'Saint Nicholas (Wikipedia)')
        self.assertEqual(event.color, 'White')

    def test_from_json_st_saturninus(self):
        date = dt.date(2018, 11, 30)
        json_obj = {
            'name': 'St. Andrew',
            'titles': ['Apostle'],
            'urls': [
                'https://en.wikipedia.org/wiki/Andrew_the_Apostle',
            ],
            'obligation': False,
            'class': 2,
            'liturgical_event': True,
        }
        event = LiturgicalCalendarEvent.from_json(date, json_obj)

        self.assertEqual(event.name, 'St. Andrew')
        self.assertEqual(event.rank, 2)
        self.assertEqual(event.liturgical_event, True)
        self.assertEqual(event.holy_day, False)
        self.assertEqual(event.urls[0].description, 'Andrew the Apostle (Wikipedia)')
        self.assertEqual(event.color, 'Red')

    def test_full_name(self):
        date = dt.date(2018, 12, 6)
        event = LiturgicalCalendarEvent(date, 'St. Nicholas', rank=3)
        expected_output = 'The Feast of St. Nicholas'
        self.assertEqual(event.full_name(capitalize=True), expected_output)

        expected_output = 'the Feast of St. Nicholas'
        self.assertEqual(event.full_name(capitalize=False), expected_output)

    def test_generate_description(self):
        url = LiturgicalCalendarEventUrl(
            'https://fisheaters.com/customsadvent5.html',
            description='Feast of the Immaculate Conception',
        )
        event = LiturgicalCalendarEvent(
            dt.date(2018, 12, 8),
            'Feast of the Immaculate Conception',
            liturgical_event=True,
            holy_day=True,
            urls=[url],
            rank=1,
            color='White',
        )

        expected_description = (
            'The Feast of the Immaculate Conception is a Holy Day of Obligation.\n\n'
            'More information about the Feast of the Immaculate Conception:\n'
            '• https://fisheaters.com/customsadvent5.html\n\n'
            'More information about Advent:\n'
        )
        description = event.generate_description(html_formatting=False)
        self.assertTrue(description.startswith(expected_description))

    def test_is_fixed(self):
        event = LiturgicalCalendarEvent(
            dt.date(2018, 12, 8),
            'Feast of the Immaculate Conception',
        )
        self.assertTrue(event.is_fixed())

        event = LiturgicalCalendarEvent(dt.date(2019, 4, 21), 'Easter')
        self.assertFalse(event.is_fixed())


class TestLiturgicalCalendarSmoke(unittest.TestCase):

    def test_liturgical_calendar(self):
        self.assertIsNotNone(LiturgicalCalendar(2018))


class TestLiturgicalCalendarSundayDates(unittest.TestCase):
    
    def test_liturgical_calendar_sunday_dates(self):
        litcal_2018 = LiturgicalCalendar(2018)
        self.assertEqual(
            litcal_2018[dt.date(2018, 9, 2)][0].name,
            'Fifteenth Sunday after Pentecost',
        )
        self.assertEqual(
            litcal_2018[dt.date(2018, 11, 25)][0].name,
            'Last Sunday after Pentecost',
        )


class TestLiturgicalCalendarIcal(unittest.TestCase):
    def test_to_ical_smoke(self):
        ics_calendar = LiturgicalCalendar(2019).to_ical()
        self.assertIsNotNone(ics_calendar)


# TODO: Test the data stored in the calendar.  (Monkey patch the data files we read from.)

# TODO: Test the ICS conversion.
