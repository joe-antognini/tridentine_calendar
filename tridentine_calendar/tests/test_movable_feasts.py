import datetime as dt
import unittest

from .. import movable_feasts as mf


class TestComputus(unittest.TestCase):

    def test_computus(self):
        self.assertEqual(mf.computus(2004), dt.date(2004, 4, 11))
        self.assertEqual(mf.computus(2018), dt.date(2018, 4, 1))
        self.assertEqual(mf.computus(2019), dt.date(2019, 4, 21))
        self.assertEqual(mf.computus(2027), dt.date(2027, 3, 28))
        self.assertEqual(mf.computus(2050), dt.date(2050, 4, 10))


class TestMovableFeastDates(unittest.TestCase):

    def test_gaudete_sunday(self):
        self.assertEqual(mf.GaudeteSunday.date(2018), dt.date(2017, 12, 17))

    def test_advent_embertide(self):
        self.assertListEqual(
            mf.AdventEmbertide.date(2018),
            [dt.date(2017, 12, 20), dt.date(2017, 12, 22), dt.date(2017, 12, 23)],
        )

    def test_sunday_within_the_octave_of_xmas(self):
        self.assertEqual(
            mf.SundayWithinTheOctaveOfXmas.date(2019), dt.date(2018, 12, 30))
        self.assertEqual(
            mf.SundayWithinTheOctaveOfXmas.date(2020), dt.date(2019, 12, 29))

    def test_holy_name(self):
        self.assertEqual(mf.HolyName.date(2018), dt.date(2018, 1, 2))
        self.assertEqual(mf.HolyName.date(2019), dt.date(2019, 1, 2))

    def test_holy_family(self):
        self.assertEqual(mf.HolyFamily.date(2018), dt.date(2018, 1, 7))
        self.assertEqual(mf.HolyFamily.date(2019), dt.date(2019, 1, 13))

    def test_plough_monday(self):
        self.assertEqual(mf.PloughMonday.date(2018), dt.date(2018, 1, 8))
        self.assertEqual(mf.PloughMonday.date(2019), dt.date(2019, 1, 7))

    def test_ash_wednesday(self):
        self.assertEqual(mf.AshWednesday.date(2004), dt.date(2004, 2, 25))
        self.assertEqual(mf.AshWednesday.date(2018), dt.date(2018, 2, 14))
        self.assertEqual(mf.AshWednesday.date(2050), dt.date(2050, 2, 23))

    def test_septuagesima(self):
        self.assertEqual(mf.Septuagesima.date(2004), dt.date(2004, 2, 8))
        self.assertEqual(mf.Septuagesima.date(2018), dt.date(2018, 1, 28))
        self.assertEqual(mf.Septuagesima.date(2050), dt.date(2050, 2, 6))

    def test_sexagesima(self):
        self.assertEqual(mf.Sexagesima.date(2018), dt.date(2018, 2, 4))

    def test_quinquagesima(self):
        self.assertEqual(mf.Quinquagesima.date(2018), dt.date(2018, 2, 11))

    def test_shrove_monday(self):
        self.assertEqual(mf.ShroveMonday.date(2018), dt.date(2018, 2, 12))

    def test_mardi_gras(self):
        self.assertEqual(mf.MardiGras.date(2018), dt.date(2018, 2, 13))

    def test_lenten_embertide(self):
        self.assertListEqual(
            mf.LentenEmbertide.date(2018),
            [dt.date(2018, 2, 21), dt.date(2018, 2, 23), dt.date(2018, 2, 24)],
        )

    def test_st_matthias(self):
        self.assertEqual(mf.StMatthias.date(2018), dt.date(2018, 2, 24))

    def test_st_gabriel_of_our_lady_of_sorrows(self):
        self.assertEqual(
            mf.StGabrielOfOurLadyOfSorrows.date(2018), dt.date(2018, 2, 27))

    def test_laetare_sunday(self):
        self.assertEqual(mf.LaetareSunday.date(2018), dt.date(2018, 3, 11))

    def test_passion_sunday(self):
        self.assertEqual(mf.PassionSunday.date(2018), dt.date(2018, 3, 18))

    def test_seven_sorrows(self):
        self.assertEqual(mf.SevenSorrows.date(2018), dt.date(2018, 3, 23))

    def test_palm_sunday(self):
        self.assertEqual(mf.PalmSunday.date(2018), dt.date(2018, 3, 25))

    def test_lady_day(self):
        self.assertEqual(mf.LadyDay.date(2018), dt.date(2018, 4, 9))

    def test_spy_wednesday(self):
        self.assertEqual(mf.SpyWednesday.date(2018), dt.date(2018, 3, 28))

    def test_maundy_thursday(self):
        self.assertEqual(mf.MaundyThursday.date(2018), dt.date(2018, 3, 29))

    def test_good_friday(self):
        self.assertEqual(mf.GoodFriday.date(2018), dt.date(2018, 3, 30))

    def test_holy_saturday(self):
        self.assertEqual(mf.HolySaturday.date(2018), dt.date(2018, 3, 31))

    def test_quasimodo_sunday(self):
        self.assertEqual(mf.QuasimodoSunday.date(2018), dt.date(2018, 4, 8))

    def test_misericordia_sunday(self):
        self.assertEqual(mf.MisericordiaSunday.date(2018), dt.date(2018, 4, 15))

    def test_jubilate_sunday(self):
        self.assertEqual(mf.JubilateSunday.date(2018), dt.date(2018, 4, 22))

    def test_cantate_sunday(self):
        self.assertEqual(mf.CantateSunday.date(2018), dt.date(2018, 4, 29))

    def test_major_rogation(self):
        self.assertEqual(mf.MajorRogation.date(2018), dt.date(2018, 4, 25))

    def test_ascension(self):
        self.assertEqual(mf.Ascension.date(2018), dt.date(2018, 5, 10))

    def test_minor_rogation(self):
        self.assertListEqual(
            mf.MinorRogation.date(2018),
            [dt.date(2018, 5, 7), dt.date(2018, 5, 8), dt.date(2018, 5, 9)],
        )

    def test_pentecost(self):
        self.assertEqual(mf.Pentecost.date(2018), dt.date(2018, 5, 20))

    def test_whit_embertide(self):
        self.assertListEqual(
            mf.WhitEmbertide.date(2018),
            [dt.date(2018, 5, 23), dt.date(2018, 5, 25), dt.date(2018, 5, 26)],
        )

    def test_trinity_sunday(self):
        self.assertEqual(mf.TrinitySunday.date(2018), dt.date(2018, 5, 27))

    def test_corpus_christi(self):
        self.assertEqual(mf.CorpusChristi.date(2018), dt.date(2018, 5, 31))

    def test_sacred_heart(self):
        self.assertEqual(mf.SacredHeart.date(2018), dt.date(2018, 6, 8))

    def test_peters_pence(self):
        self.assertEqual(mf.PetersPence.date(2004), dt.date(2004, 6, 27))
        self.assertEqual(mf.PetersPence.date(2018), dt.date(2018, 7, 1))

    def test_michaelmas_embertide(self):
        self.assertListEqual(
            mf.MichaelmasEmbertide.date(2018),
            [dt.date(2018, 9, 19), dt.date(2018, 9, 21), dt.date(2018, 9, 22)],
        )

    def test_christ_the_king(self):
        self.assertEqual(mf.ChristTheKing.date(2018), dt.date(2018, 10, 28))

    def test_st_johns_day(self):
        self.assertEqual(mf.StJohnsDay.date(2021), dt.date(2021, 6, 24))
        self.assertEqual(mf.StJohnsDay.date(2022), dt.date(2022, 6, 23))

    def test_st_johns_eve(self):
        self.assertEqual(mf.StJohnsEve.date(2021), dt.date(2021, 6, 23))
        self.assertEqual(mf.StJohnsEve.date(2022), dt.date(2022, 6, 22))
