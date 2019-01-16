import datetime as dt
import unittest

import litcal.feast_dates as fd


class TestComputus(unittest.TestCase):

    def test_computus(self):
        self.assertEqual(fd.computus(2004), dt.date(2004, 4, 11))
        self.assertEqual(fd.computus(2018), dt.date(2018, 4, 1))
        self.assertEqual(fd.computus(2019), dt.date(2019, 4, 21))
        self.assertEqual(fd.computus(2027), dt.date(2027, 3, 28))
        self.assertEqual(fd.computus(2050), dt.date(2050, 4, 10))


class TestMovableFeastDates(unittest.TestCase):

    def test_liturgical_year_start_date(self):
        self.assertEqual(fd.liturgical_year_start(2004), dt.date(2003, 11, 30))
        self.assertEqual(fd.liturgical_year_start(2018), dt.date(2017, 12, 3))
        self.assertEqual(fd.liturgical_year_start(2019), dt.date(2018, 12, 2))

    def test_liturgical_year_end_date(self):
        self.assertEqual(fd.liturgical_year_end(2004), dt.date(2004, 11, 27))
        self.assertEqual(fd.liturgical_year_end(2018), dt.date(2018, 12, 1))
        self.assertEqual(fd.liturgical_year_end(2019), dt.date(2019, 11, 30))

    def test_gaudete_sunday_date(self):
        self.assertEqual(fd.gaudete_sunday_date(2018), dt.date(2017, 12, 17))

    def test_advent_embertide_dates(self):
        self.assertListEqual(
            fd.advent_embertide_dates(2018),
            [dt.date(2017, 12, 20), dt.date(2017, 12, 22), dt.date(2017, 12, 23)],
        )

    def test_holy_name_date(self):
        self.assertEqual(fd.holy_name_date(2018), dt.date(2018, 1, 2))
        self.assertEqual(fd.holy_name_date(2019), dt.date(2019, 1, 2))

    def test_holy_family_date(self):
        self.assertEqual(fd.holy_family_date(2018), dt.date(2018, 1, 7))
        self.assertEqual(fd.holy_family_date(2019), dt.date(2019, 1, 13))

    def test_plough_monday_date(self):
        self.assertEqual(fd.plough_monday_date(2018), dt.date(2018, 1, 8))
        self.assertEqual(fd.plough_monday_date(2019), dt.date(2019, 1, 7))

    def test_ash_wednesday_date(self):
        self.assertEqual(fd.ash_wednesday_date(2004), dt.date(2004, 2, 25))
        self.assertEqual(fd.ash_wednesday_date(2018), dt.date(2018, 2, 14))
        self.assertEqual(fd.ash_wednesday_date(2050), dt.date(2050, 2, 23))

    def test_septuagesima_date(self):
        self.assertEqual(fd.septuagesima_date(2004), dt.date(2004, 2, 8))
        self.assertEqual(fd.septuagesima_date(2018), dt.date(2018, 1, 28))
        self.assertEqual(fd.septuagesima_date(2050), dt.date(2050, 2, 6))

    def test_sexagesima_date(self):
        self.assertEqual(fd.sexagesima_date(2018), dt.date(2018, 2, 4))

    def test_quinquagesima_date(self):
        self.assertEqual(fd.quinquagesima_date(2018), dt.date(2018, 2, 11))

    def test_shrove_monday_date(self):
        self.assertEqual(fd.shrove_monday_date(2018), dt.date(2018, 2, 12))

    def test_mardi_gras_date(self):
        self.assertEqual(fd.mardi_gras_date(2018), dt.date(2018, 2, 13))

    def test_lenten_embertide_dates(self):
        self.assertListEqual(
            fd.lenten_embertide_dates(2018),
            [dt.date(2018, 2, 21), dt.date(2018, 2, 23), dt.date(2018, 2, 24)],
        )

    def test_st_matthias_date(self):
        self.assertEqual(fd.st_matthias_date(2018), dt.date(2018, 2, 24))

    def test_st_gabriel_of_our_lady_of_sorrows_date(self):
        self.assertEqual(
            fd.st_gabriel_of_our_lady_of_sorrows_date(2018), dt.date(2018, 2, 27))

    def test_laetare_sunday_date(self):
        self.assertEqual(fd.laetare_sunday_date(2018), dt.date(2018, 3, 11))

    def test_passion_sunday_date(self):
        self.assertEqual(fd.passion_sunday_date(2018), dt.date(2018, 3, 18))

    def test_seven_sorrows_date(self):
        self.assertEqual(fd.seven_sorrows_date(2018), dt.date(2018, 3, 23))

    def test_palm_sunday_date(self):
        self.assertEqual(fd.palm_sunday_date(2018), dt.date(2018, 3, 25))

    def test_lady_day_date(self):
        self.assertEqual(fd.lady_day_date(2018), dt.date(2018, 4, 9))

    def test_spy_wednesday_date(self):
        self.assertEqual(fd.spy_wednesday_date(2018), dt.date(2018, 3, 28))

    def test_maundy_thursday_date(self):
        self.assertEqual(fd.maundy_thursday_date(2018), dt.date(2018, 3, 29))

    def test_good_friday_date(self):
        self.assertEqual(fd.good_friday_date(2018), dt.date(2018, 3, 30))

    def test_holy_saturday_date(self):
        self.assertEqual(fd.holy_saturday_date(2018), dt.date(2018, 3, 31))

    def test_quasimodo_sunday_date(self):
        self.assertEqual(fd.quasimodo_sunday_date(2018), dt.date(2018, 4, 8))

    def test_jubilate_sunday_date(self):
        self.assertEqual(fd.jubilate_sunday_date(2018), dt.date(2018, 4, 15))

    def test_misericordia_sunday_date(self):
        self.assertEqual(fd.misericordia_sunday_date(2018), dt.date(2018, 4, 22))

    def test_cantate_sunday_date(self):
        self.assertEqual(fd.cantate_sunday_date(2018), dt.date(2018, 4, 29))

    def test_major_rogation_date(self):
        self.assertEqual(fd.major_rogation_date(2018), dt.date(2018, 4, 25))

    def test_ascension_date(self):
        self.assertEqual(fd.ascension_date(2018), dt.date(2018, 5, 10))

    def test_minor_rogation_dates(self):
        self.assertListEqual(
            fd.minor_rogation_dates(2018),
            [dt.date(2018, 5, 7), dt.date(2018, 5, 8), dt.date(2018, 5, 9)],
        )

    def test_pentecost_date(self):
        self.assertEqual(fd.pentecost_date(2018), dt.date(2018, 5, 20))

    def test_whit_embertide_dates(self):
        self.assertListEqual(
            fd.whit_embertide_dates(2018),
            [dt.date(2018, 5, 23), dt.date(2018, 5, 25), dt.date(2018, 5, 26)],
        )

    def test_trinity_sunday_date(self):
        self.assertEqual(fd.trinity_sunday_date(2018), dt.date(2018, 5, 27))

    def test_corpus_christi_date(self):
        self.assertEqual(fd.corpus_christi_date(2018), dt.date(2018, 5, 31))

    def test_sacred_heart_date(self):
        self.assertEqual(fd.sacred_heart_date(2018), dt.date(2018, 6, 8))

    def test_peters_pence_date(self):
        self.assertEqual(fd.peters_pence_date(2004), dt.date(2004, 6, 27))
        self.assertEqual(fd.peters_pence_date(2018), dt.date(2018, 7, 1))

    def test_michaelmas_embertide_dates(self):
        self.assertListEqual(
            fd.michaelmas_embertide_dates(2018),
            [dt.date(2018, 9, 19), dt.date(2018, 9, 21), dt.date(2018, 9, 22)],
        )

    def test_christ_the_king_date(self):
        self.assertEqual(fd.christ_the_king_date(2018), dt.date(2018, 10, 28))