import datetime as dt
import unittest

from .. import feast_dates as fd


class TestComputus(unittest.TestCase):

    def test_computus(self):
        self.assertEqual(fd.computus(2004), dt.date(2004, 4, 11))
        self.assertEqual(fd.computus(2018), dt.date(2018, 4, 1))
        self.assertEqual(fd.computus(2019), dt.date(2019, 4, 21))
        self.assertEqual(fd.computus(2027), dt.date(2027, 3, 28))
        self.assertEqual(fd.computus(2050), dt.date(2050, 4, 10))


class TestMovableFeastDates(unittest.TestCase):

    def test_gaudete_sunday(self):
        self.assertEqual(fd.gaudete_sunday(2018), dt.date(2017, 12, 17))

    def test_advent_embertide(self):
        self.assertListEqual(
            fd.advent_embertide(2018),
            [dt.date(2017, 12, 20), dt.date(2017, 12, 22), dt.date(2017, 12, 23)],
        )

    def test_sunday_within_the_octave_of_xmas(self):
        self.assertEqual(fd.sunday_within_the_octave_of_xmas(2019), dt.date(2018, 12, 30))
        self.assertEqual(fd.sunday_within_the_octave_of_xmas(2020), dt.date(2019, 12, 29))

    def test_holy_name(self):
        self.assertEqual(fd.holy_name(2018), dt.date(2018, 1, 2))
        self.assertEqual(fd.holy_name(2019), dt.date(2019, 1, 2))

    def test_holy_family(self):
        self.assertEqual(fd.holy_family(2018), dt.date(2018, 1, 7))
        self.assertEqual(fd.holy_family(2019), dt.date(2019, 1, 13))

    def test_plough_monday(self):
        self.assertEqual(fd.plough_monday(2018), dt.date(2018, 1, 8))
        self.assertEqual(fd.plough_monday(2019), dt.date(2019, 1, 7))

    def test_ash_wednesday(self):
        self.assertEqual(fd.ash_wednesday(2004), dt.date(2004, 2, 25))
        self.assertEqual(fd.ash_wednesday(2018), dt.date(2018, 2, 14))
        self.assertEqual(fd.ash_wednesday(2050), dt.date(2050, 2, 23))

    def test_septuagesima(self):
        self.assertEqual(fd.septuagesima(2004), dt.date(2004, 2, 8))
        self.assertEqual(fd.septuagesima(2018), dt.date(2018, 1, 28))
        self.assertEqual(fd.septuagesima(2050), dt.date(2050, 2, 6))

    def test_sexagesima(self):
        self.assertEqual(fd.sexagesima(2018), dt.date(2018, 2, 4))

    def test_quinquagesima(self):
        self.assertEqual(fd.quinquagesima(2018), dt.date(2018, 2, 11))

    def test_shrove_monday(self):
        self.assertEqual(fd.shrove_monday(2018), dt.date(2018, 2, 12))

    def test_mardi_gras(self):
        self.assertEqual(fd.mardi_gras(2018), dt.date(2018, 2, 13))

    def test_lenten_embertide(self):
        self.assertListEqual(
            fd.lenten_embertide(2018),
            [dt.date(2018, 2, 21), dt.date(2018, 2, 23), dt.date(2018, 2, 24)],
        )

    def test_st_matthias(self):
        self.assertEqual(fd.st_matthias(2018), dt.date(2018, 2, 24))

    def test_st_gabriel_of_our_lady_of_sorrows(self):
        self.assertEqual(
            fd.st_gabriel_of_our_lady_of_sorrows(2018), dt.date(2018, 2, 27))

    def test_laetare_sunday(self):
        self.assertEqual(fd.laetare_sunday(2018), dt.date(2018, 3, 11))

    def test_passion_sunday(self):
        self.assertEqual(fd.passion_sunday(2018), dt.date(2018, 3, 18))

    def test_seven_sorrows(self):
        self.assertEqual(fd.seven_sorrows(2018), dt.date(2018, 3, 23))

    def test_palm_sunday(self):
        self.assertEqual(fd.palm_sunday(2018), dt.date(2018, 3, 25))

    def test_lady_day(self):
        self.assertEqual(fd.lady_day(2018), dt.date(2018, 4, 9))

    def test_spy_wednesday(self):
        self.assertEqual(fd.spy_wednesday(2018), dt.date(2018, 3, 28))

    def test_maundy_thursday(self):
        self.assertEqual(fd.maundy_thursday(2018), dt.date(2018, 3, 29))

    def test_good_friday(self):
        self.assertEqual(fd.good_friday(2018), dt.date(2018, 3, 30))

    def test_holy_saturday(self):
        self.assertEqual(fd.holy_saturday(2018), dt.date(2018, 3, 31))

    def test_quasimodo_sunday(self):
        self.assertEqual(fd.quasimodo_sunday(2018), dt.date(2018, 4, 8))

    def test_misericordia_sunday(self):
        self.assertEqual(fd.misericordia_sunday(2018), dt.date(2018, 4, 15))

    def test_jubilate_sunday(self):
        self.assertEqual(fd.jubilate_sunday(2018), dt.date(2018, 4, 22))

    def test_cantate_sunday(self):
        self.assertEqual(fd.cantate_sunday(2018), dt.date(2018, 4, 29))

    def test_major_rogation(self):
        self.assertEqual(fd.major_rogation(2018), dt.date(2018, 4, 25))

    def test_ascension(self):
        self.assertEqual(fd.ascension(2018), dt.date(2018, 5, 10))

    def test_minor_rogation(self):
        self.assertListEqual(
            fd.minor_rogation(2018),
            [dt.date(2018, 5, 7), dt.date(2018, 5, 8), dt.date(2018, 5, 9)],
        )

    def test_pentecost(self):
        self.assertEqual(fd.pentecost(2018), dt.date(2018, 5, 20))

    def test_whit_embertide(self):
        self.assertListEqual(
            fd.whit_embertide(2018),
            [dt.date(2018, 5, 23), dt.date(2018, 5, 25), dt.date(2018, 5, 26)],
        )

    def test_trinity_sunday(self):
        self.assertEqual(fd.trinity_sunday(2018), dt.date(2018, 5, 27))

    def test_corpus_christi(self):
        self.assertEqual(fd.corpus_christi(2018), dt.date(2018, 5, 31))

    def test_sacred_heart(self):
        self.assertEqual(fd.sacred_heart(2018), dt.date(2018, 6, 8))

    def test_peters_pence(self):
        self.assertEqual(fd.peters_pence(2004), dt.date(2004, 6, 27))
        self.assertEqual(fd.peters_pence(2018), dt.date(2018, 7, 1))

    def test_michaelmas_embertide(self):
        self.assertListEqual(
            fd.michaelmas_embertide(2018),
            [dt.date(2018, 9, 19), dt.date(2018, 9, 21), dt.date(2018, 9, 22)],
        )

    def test_christ_the_king(self):
        self.assertEqual(fd.christ_the_king(2018), dt.date(2018, 10, 28))
