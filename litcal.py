from __future__ import division

import calendar
import datetime as dt
import json
import os


def computus(year):
    """Calculate the date of Easter.

    Args:
        year: Integer with the year.

    Returns:
        A `datetime.Date` object with the date of Easter.
    """
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1

    return dt.date(year, month, day)


class LiturgicalCalendar(object):
    """A liturgical calendar following the 1962 Tridentine missal."""

    def __init__(self, year):
        self.year = year
        self.calendar = {}
        self.dirname = os.path.dirname(os.path.realpath(__file__))
        
        with open(os.path.join(self.dirname, 'movable_feasts.json')) as json_file:
            self.movable_feasts = json.load(json_file)

        with open(os.path.join(self.dirname, 'fixed_feasts.json')) as json_file:
            self.fixed_feasts = json.load(json_file)

        with open(os.path.join(self.dirname, 'traditional_feasts.json')) as json_file:
            self.traditional_feasts = json.load(json_file)

        self.easter_date = computus(self.year)
        self._mark_solemnities()
        self._mark_sundays()
        self._mark_feasts_memorials_and_commemorations()
        self._mark_traditional_feasts()

    def _mark_solemnities(self):
        # First we do fixed solemnities.
        for date in self.fixed_feasts:
            if self.fixed_feasts[date]['class'] == 1:
                self.calendar[_self.convert_date(date)] = self.fixed_feasts[date]

        # Now the movable solemnities.
        function_name_pairs = (
            (self.gaudete_sunday_date, 'Gaudete Sunday'),
            (self.holy_name_date, 'Feast of the Holy Name'),
            (self.holy_family_date, 'Feast of the Holy Family'),
            (self.plough_monday_date, 'Plough Monday'),
            (self.septuagesima_date, 'Septuagesima'),
            (self.sexagesima_date, 'Sexagesima'),
            (self.quinquagesima_date, 'Quinquagesima'),
            (self.shrove_monday_date, 'Shrove Monday'),
            (self.mardi_gras_date, 'Mardi Gras'),
            (self.ash_wednesday_date, 'Ash Wednesday'),
            (self.st_matthias_date, 'St. Matthias'),
            (self.st_gabriel_of_our_lady_of_sorrows, 'St. Gabriel of Our Lady of Sorrows'),
            (self.laetare_sunday_date, 'Laetare Sunday'),
            (self.passion_sunday_date, 'Passion Sunday'),
            (self.seven_sorrows_date, 'The Seven Sorrows'),
            (self.palm_sunday_date, 'Palm Sunday'),
            (self.spy_wednesday_date, 'Spy Wednesday'),
            (self.maundy_thursday_date, 'Maundy Thursday'),
            (self.good_friday_date, 'Good Friday'),
            (self.holy_saturday_date, 'Holy Saturday'),
            (self.easter_date, 'Easter'),
            (self.quasimodo_sunday_date, 'Quasimodo Sunday'),
            (self.jubilate_sunday_date, 'Jubilate Sunday'),
            (self.misericordia_sunday_date, 'Misericordia Sunday'),
            (self.cantate_sunday_date, 'Cantate Sunday'),
            (self.major_rogation_date, 'Major Rogation'),
            (self.ascension_date, 'Ascension'),
            (self.minor_rogation_dates, 'Minor Rogation'),
            (self.pentecost_date, 'Pentecost'),
            (self.trinity_sunday_date, 'Trinity Sunday'),
            (self.corpus_christi_date, 'Corpus Christi'),
            (self.sacred_heart_date, 'Feast of the Sacred Heart'),
            (self.christ_the_king_date, 'Christ the King'),
        )

        for date_fn, name in function_name_pairs:
            self.calendar[date_fn()] = self.movable_feasts[name]

    def _convert_date(self, date_str):
        date = dt.datetime.strptime(date_str, '%B %d')
        return date.replace(self.year, date.month, date.year)

    def gaudete_sunday_date(self):
        xmas = dt.date(self.year - 1, 12, 25)
        return xmas - dt.timedelta(xmas.weekday() + 8)

    def holy_name_date(self):
        new_years_day = dt.date(self.year, 1, 1)
        holy_name = new_years_day + dt.timedelta(6 - new_years_day.weekday())
        if holy_name in [new_years_day, dt.date(self.year, 1, 6), dt.date(self.year, 1, 7)]:
            return dt.date(self.year, 1, 2)
        else:
            return holy_name

    def holy_family_date(self):
        epiphany = dt.date(self.year, 1, 6)
        delta = dt.timedelta(6 - epiphany.weekday())
        if delta == 0:
            delta = 7
        return epiphany + delta

    def plough_monday_date(self):
        return self.holy_family_date + dt.timedelta(1)

    def ash_wednesday_date(self):
        return self.easter_date - dt.timedelta(46)

    def quinquagesima_date(self):
        return self.ash_wednesday_date - dt.timedelta(3)

    def shrove_monday_date(self):
        return self.ash_wednesday_date - dt.timedelta(2)

    def mardi_gras_date(self):
        return self.ash_wednesday_date - dt.timedelta(1)

    def sexagesima_date(self):
        return self.quinquagesima_date - dt.timedelta(7)

    def septuagesima_date(self):
        return self.sexagesima_date - dt.timedelta(7)

    def st_matthias_date(self):
        if calendar.isleapyear(self.year):
            return dt.date(self.year, 2, 24)
        else:
            return dt.date(self.year, 2, 25)

    def st_gabriel_of_our_lady_of_sorrows(self):
        if calendar.isleapyear(self.year):
            return dt.date(self.year, 2, 27)
        else:
            return dt.date(self.year, 2, 28)

    def laetare_sunday_date(self):
        return self.easter_date - dt.timedelta(21)
    
    @property
    def passion_sunday_date(self):
        return self.easter_date - dt.timedelta(14)

    def seven_sorrows_date(self):
        return self.palm_sunday_date - dt.timedelta(2)

    def palm_sunday_date(self):
        return self.easter_date - dt.timedelta(7)

    def spy_wednesday_date(self):
        return self.easter_date - dt.timedelta(4)

    def maundy_thursday_date(self):
        return self.easter_date - dt.timedelta(3)

    def good_friday_date(self):
        return self.easter_date - dt.timedelta(2)

    def holy_saturday_date(self):
        return self.easter_date - dt.timedelta(1)

    def quasimodo_sunday_date(self):
        return self.easter_date + dt.timedelta(7)

    def jubilate_sunday_date(self):
        return self.easter_date + dt.timedelta(14)

    def misericordia_sunday_date(self):
        return self.easter_date + dt.timedelta(21)

    def cantate_sunday_date(self):
        return self.easter_date + dt.timedelta(28)

    def major_rogation_date(self):
        major_rogation = dt.date(self.year, 4, 25)
        if major_rogation != self.easter_date:
            return major_rogation
        else:
            return major_rogation + dt.timedelta(2)

    def ascension_date(self):
        return self.easter_date + dt.timedelta(39)

    def minor_rogation_dates(self):
        return [self.ascension_date - dt.timedelta(i) for i in range(1, 4)]

    def pentecost_date(self):
        return self.easter_date + dt.timedelta(49)

    def trinity_sunday_date(self):
        return self.pentecost_date + dt.timedelta(7)

    def corpus_christi_date(self):
        return self.trinity_sunday_date + dt.timedelta(4)

    def sacred_heart_date(self):
        return self.corpus_christi + dt.timedelta(8)

    def christ_the_king_date(self):
        halloween = dt.date(self.year, 10, 31)
        return halloween - dt.timedelta((halloween.weekday() + 1) % 7)
