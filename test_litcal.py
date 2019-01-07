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

class TestLiturgicalCalendarMovableFeastDates(unittest.TestCase):
    
    def setUp(self):
        self.litcal_2004 = LiturgicalCalendar(2004)
        self.litcal_2018 = LiturgicalCalendar(2018)
        self.litcal_2019 = LiturgicalCalendar(2019)
        self.litcal_2050 = LiturgicalCalendar(2050)

    def test_liturgical_year_start_date(self):
        self.assertEqual(self.litcal_2004.liturgical_year_start, dt.date(2003, 11, 30))
        self.assertEqual(self.litcal_2018.liturgical_year_start, dt.date(2017, 12, 3))
        self.assertEqual(self.litcal_2019.liturgical_year_start, dt.date(2018, 12, 2))

    def test_liturgical_year_end_date(self):
        self.assertEqual(self.litcal_2004.liturgical_year_end, dt.date(2004, 11, 27))
        self.assertEqual(self.litcal_2018.liturgical_year_end, dt.date(2018, 12, 1))
        self.assertEqual(self.litcal_2019.liturgical_year_end, dt.date(2019, 11, 30))

    def test_epiphany_date(self):
        computed_epiphany_name = self.litcal_2019[dt.date(2019, 1, 6)][0]['name']
        self.assertEqual(computed_epiphany_name, 'Three Kings Day')

    def test_candlemas_date(self):
        computed_epiphany_name = self.litcal_2019[dt.date(2019, 2, 2)][0]['name']
        self.assertEqual(computed_epiphany_name, 'Candlemas')

    def test_gaudete_sunday_date(self):
        self.assertEqual(self.litcal_2018.gaudete_sunday_date, dt.date(2017, 12, 17))

    def test_advent_embertide_dates(self):
        self.assertListEqual(
            self.litcal_2018.advent_embertide_dates,
            [dt.date(2017, 12, 20), dt.date(2017, 12, 22), dt.date(2017, 12, 23)],
        )

    def test_holy_name_date(self):
        self.assertEqual(self.litcal_2018.holy_name_date, dt.date(2018, 1, 2))
        self.assertEqual(self.litcal_2019.holy_name_date, dt.date(2019, 1, 2))

    def test_holy_family_date(self):
        self.assertEqual(self.litcal_2018.holy_family_date, dt.date(2018, 1, 7))
        self.assertEqual(self.litcal_2019.holy_family_date, dt.date(2019, 1, 13))

    def test_plough_monday_date(self):
        self.assertEqual(self.litcal_2018.plough_monday_date, dt.date(2018, 1, 8))
        self.assertEqual(self.litcal_2019.plough_monday_date, dt.date(2019, 1, 7))

    def test_ash_wednesday_date(self):
        self.assertEqual(self.litcal_2004.ash_wednesday_date, dt.date(2004, 2, 25))
        self.assertEqual(self.litcal_2018.ash_wednesday_date, dt.date(2018, 2, 14))
        self.assertEqual(self.litcal_2050.ash_wednesday_date, dt.date(2050, 2, 23))

    def test_septuagesima_date(self):
        self.assertEqual(self.litcal_2004.septuagesima_date, dt.date(2004, 2, 8))
        self.assertEqual(self.litcal_2018.septuagesima_date, dt.date(2018, 1, 28))
        self.assertEqual(self.litcal_2050.septuagesima_date, dt.date(2050, 2, 6))

    def test_sexagesima_date(self):
        self.assertEqual(self.litcal_2018.sexagesima_date, dt.date(2018, 2, 4))

    def test_quinquagesima_date(self):
        self.assertEqual(self.litcal_2018.quinquagesima_date, dt.date(2018, 2, 11))

    def test_shrove_monday_date(self):
        self.assertEqual(self.litcal_2018.shrove_monday_date, dt.date(2018, 2, 12))

    def test_mardi_gras_date(self):
        self.assertEqual(self.litcal_2018.mardi_gras_date, dt.date(2018, 2, 13))

    def test_lenten_embertide_dates(self):
        self.assertListEqual(
            self.litcal_2018.lenten_embertide_dates,
            [dt.date(2018, 2, 21), dt.date(2018, 2, 23), dt.date(2018, 2, 24)],
        )

    def test_st_matthias_date(self):
        self.assertEqual(self.litcal_2018.st_matthias_date, dt.date(2018, 2, 24))

    def test_st_gabriel_of_our_lady_of_sorrows_date(self):
        self.assertEqual(
            self.litcal_2018.st_gabriel_of_our_lady_of_sorrows_date, dt.date(2018, 2, 27))

    def test_laetare_sunday_date(self):
        self.assertEqual(self.litcal_2018.laetare_sunday_date, dt.date(2018, 3, 11))

    def test_passion_sunday_date(self):
        self.assertEqual(self.litcal_2018.passion_sunday_date, dt.date(2018, 3, 18))

    def test_seven_sorrows_date(self):
        self.assertEqual(self.litcal_2018.seven_sorrows_date, dt.date(2018, 3, 23))

    def test_palm_sunday_date(self):
        self.assertEqual(self.litcal_2018.palm_sunday_date, dt.date(2018, 3, 25))

    def test_lady_day_date(self):
        self.assertEqual(self.litcal_2018.lady_day_date, dt.date(2018, 4, 9))

    def test_spy_wednesday_date(self):
        self.assertEqual(self.litcal_2018.spy_wednesday_date, dt.date(2018, 3, 28))

    def test_maundy_thursday_date(self):
        self.assertEqual(self.litcal_2018.maundy_thursday_date, dt.date(2018, 3, 29))

    def test_good_friday_date(self):
        self.assertEqual(self.litcal_2018.good_friday_date, dt.date(2018, 3, 30))

    def test_holy_saturday_date(self):
        self.assertEqual(self.litcal_2018.holy_saturday_date, dt.date(2018, 3, 31))

    def test_easter_date(self):
        self.assertEqual(self.litcal_2018.easter_date, dt.date(2018, 4, 1))

    def test_quasimodo_sunday_date(self):
        self.assertEqual(self.litcal_2018.quasimodo_sunday_date, dt.date(2018, 4, 8))

    def test_jubilate_sunday_date(self):
        self.assertEqual(self.litcal_2018.jubilate_sunday_date, dt.date(2018, 4, 15))

    def test_misericordia_sunday_date(self):
        self.assertEqual(self.litcal_2018.misericordia_sunday_date, dt.date(2018, 4, 22))

    def test_cantate_sunday_date(self):
        self.assertEqual(self.litcal_2018.cantate_sunday_date, dt.date(2018, 4, 29))

    def test_major_rogation_date(self):
        self.assertEqual(self.litcal_2018.major_rogation_date, dt.date(2018, 4, 25))

    def test_ascension_date(self):
        self.assertEqual(self.litcal_2018.ascension_date, dt.date(2018, 5, 10))

    def test_minor_rogation_dates(self):
        self.assertListEqual(
            self.litcal_2018.minor_rogation_dates,
            [dt.date(2018, 5, 7), dt.date(2018, 5, 8), dt.date(2018, 5, 9)],
        )

    def test_pentecost_date(self):
        self.assertEqual(self.litcal_2018.pentecost_date, dt.date(2018, 5, 20))

    def test_whit_embertide_dates(self):
        self.assertListEqual(
            self.litcal_2018.whit_embertide_dates,
            [dt.date(2018, 5, 23), dt.date(2018, 5, 25), dt.date(2018, 5, 26)],
        )

    def test_trinity_sunday_date(self):
        self.assertEqual(self.litcal_2018.trinity_sunday_date, dt.date(2018, 5, 27))

    def test_corpus_christi_date(self):
        self.assertEqual(self.litcal_2018.corpus_christi_date, dt.date(2018, 5, 31))

    def test_sacred_heart_date(self):
        self.assertEqual(self.litcal_2018.sacred_heart_date, dt.date(2018, 6, 8))

    def test_peters_pence_date(self):
        self.assertEqual(self.litcal_2004.peters_pence_date, dt.date(2004, 6, 27))
        self.assertEqual(self.litcal_2018.peters_pence_date, dt.date(2018, 7, 1))

    def test_michaelmas_embertide_dates(self):
        self.assertListEqual(
            self.litcal_2018.michaelmas_embertide_dates,
            [dt.date(2018, 9, 19), dt.date(2018, 9, 21), dt.date(2018, 9, 22)],
        )

    def test_christ_the_king_date(self):
        self.assertEqual(self.litcal_2018.christ_the_king_date, dt.date(2018, 10, 28))


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
