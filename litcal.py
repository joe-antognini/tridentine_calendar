from __future__ import division

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
        self.calendar[self.gaudete_sunday] = self.movable_feasts['Gaudete Sunday']
        self.calendar[self.holy_name_date] = self.movable_feasts['Feast of the Holy Name']
        self.calendar[self.holy_family_date] = self.movable_feasts['Feast of the Holy Family']
        self.calendar[self.plough_monday_date] = self.movable_feasts['Plough Monday']
        self.calendar[self.septuagesima_date] = self.movable_feasts['Septuagesima']
        self.calendar[self.sexagesima_date] = self.movable_feasts['Sexagesima']
        self.calendar[self.quinquagesima_date] = self.movable_feasts['Quinquagesima']

    def _convert_date(self, date_str):
        date = dt.datetime.strptime(date_str, '%B %d')
        return date.replace(self.year, date.month, date.year)

    @property
    def gaudete_sunday(self):
        xmas = dt.date(self.year - 1, 12, 25)
        return xmas - dt.timedelta(xmas.weekday() + 8)

    @property
    def holy_name_date(self):
        new_years_day = dt.date(self.year, 1, 1)
        holy_name = new_years_day + dt.timedelta(6 - new_years_day.weekday())
        if holy_name in [new_years_day, dt.date(self.year, 1, 6), dt.date(self.year, 1, 7)]:
            return dt.date(self.year, 1, 2)
        else:
            return holy_name

    @property
    def holy_family_date(self):
        epiphany = dt.date(self.year, 1, 6)
        delta = dt.timedelta(6 - epiphany.weekday())
        if delta == 0:
            delta = 7
        return epiphany + delta

    @property
    def plough_monday_date(self):
        return holy_family_date + dt.timedelta(1)

    @property
    def ash_wednesday_date(self):
        return self.easter_date - dt.timedelta(46)

    @property
    def quinquagesima_date(self):
        return ash_wednesday_date - dt.timedelta(3)

    @property
    def sexagesima_date(self):
        return quinquagesima_date - dt.timedelta(7)

    @property
    def septuagesima_date(self):
        return sexagesima_date - dt.timedelta(7)
