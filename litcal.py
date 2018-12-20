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
        self.fixed_feasts = self._convert_json_to_dict(self.fixed_feasts)

        with open(os.path.join(self.dirname, 'traditional_feasts.json')) as json_file:
            self.traditional_feasts = json.load(json_file)

        self._mark_solemnities()
        self._mark_sundays()
        self._mark_feasts_memorials_and_commemorations()
        self._mark_traditional_feasts()

    def _convert_json_to_dict(self, json_obj):
        d = {}
        for elem in json_obj:
            elem_date = dt.datetime.strptime(elem['date'], '%B %d')
            elem_date = elem_date.replace(self.year, elem_date.month, elem_date.day)
            if elem_date not in d:
                d[elem_date] = elem
            else:
                if type(d[elem_date) is list:
                    d[elem_date = d[elem_date + [elem]
                else:
                    d[elem_date = [d[elem_date, elem]
        return d

    def _mark_solemnities(self):
        # Advent
        self.calendar[dt.date(self.year, 12, 8)] = self.fixed_feasts[
