"""The movable feasts of the liturgical calendar.

These feasts are represented as objects with a `name` and a `date`.  The `name` attribute links the
feast to the other data in `movable_feasts_ferias_et_al.json`.

This module contains the function `get_movable_feasts` which will introspect this module to find all
the movable feasts in the calendar.  Any `MovableFeast` objects added to this module will therefore
be added to the calendor generated by `tridentine_calendar`.

"""

import calendar
import datetime as dt
import functools
import sys
from abc import ABCMeta
from abc import abstractmethod


@functools.lru_cache()
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


class MovableFeast(metaclass=ABCMeta):
    """An abstract class for a movable feast.

    A movable feast must have two attributes:

    1. A name.
    2. A date.

    The name must correspond to the feast data in `movable_feasts_ferias_et_al.json`.

    """

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError('A movable feast must have a name.')
    
    @abstractmethod
    def date(year):
        raise NotImplementedError('A movable feast must have a date.')
    
    def __repr__(self):
        return self.name


class GaudeteSunday(MovableFeast):
    """Represents Gaudete Sunday."""

    name = 'Gaudete Sunday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Gaudete Sunday.

        Gaudete Sunday is the third Sunday of Advent.
        
        """
        xmas = dt.date(year - 1, 12, 25)
        return xmas - dt.timedelta(xmas.weekday() + 8)


class AdventEmbertide(MovableFeast):
    """Represents Advent Embertide."""

    name = 'Advent Embertide'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Advent Embertide.
        
        Advent Embertide is the Wednesday, Friday, and Saturday after Gaudete Sunday.

        """
        return sorted([GaudeteSunday.date(year) + dt.timedelta(i) for i in [3, 5, 6]])


class SundayWithinTheOctaveOfXmas(MovableFeast):
    """Represents Sunday within the Octave of Christmas."""

    name = 'Sunday within the Octave of Christmas'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of the Sunday within the Octave of Easter."""
        xmas = dt.date(year - 1, 12, 25)
        sunday = xmas + dt.timedelta(6 - xmas.weekday())
        if sunday == xmas:
            sunday += dt.timedelta(7)
        return sunday


class HolyName(MovableFeast):
    """Represents the Feast of the Holy Name."""

    name = 'The Holy Name'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of the Feast of the Holy Name.

        The Feast of the Holy Name is generally the first Sunday of the year, unless the first
        Sunday falls on January 1, January 6, or January 7, in which case the Feast of the Holy Name
        is moved to January 2.

        """
        new_years_day = dt.date(year, 1, 1)
        holy_name = new_years_day + dt.timedelta(6 - new_years_day.weekday())
        if holy_name in [new_years_day, dt.date(year, 1, 6), dt.date(year, 1, 7)]:
            return dt.date(year, 1, 2)
        return holy_name


class HolyFamily(MovableFeast):
    """Represents the Feast of the Holy Family."""

    name = 'The Holy Family'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of the Feast of the Holy Family.

        The Feast of the Holy Family is the first Sunday after Three Kings Day.

        """
        epiphany = dt.date(year, 1, 6)
        delta = dt.timedelta(6 - epiphany.weekday())
        if delta == dt.timedelta(0):
            delta = dt.timedelta(7)
        return epiphany + delta


class PloughMonday(MovableFeast):
    """Represents Plough Monday."""

    name = 'Plough Monday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Plough Monday.

        Plough Monday is the first Monday after Three Kings Day.

        """
        epiphany = dt.date(year, 1, 6)
        if epiphany.weekday() == 6:
            return epiphany + dt.timedelta(1)
        return HolyFamily.date(year) + dt.timedelta(1)


class AshWednesday(MovableFeast):
    """Represents Ash Wednesday."""

    name = 'Ash Wednesday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Ash Wednesday.

        Ash Wednesday is forty days prior to Easter, excluding Sundays.

        """
        return Easter.date(year) - dt.timedelta(46)


class LentenEmbertide(MovableFeast):
    """Represents Lenten Embertide."""

    name = 'Lenten Embertide'

    @functools.lru_cache()
    def date(year):
        """Calculate the dates of Lenten Embertide.

        Lenten Embertide is the Wednesday, Friday, and Saturday after the first Sunday of Lent.

        """
        return [AshWednesday.date(year) + dt.timedelta(i) for i in [7, 9, 10]]


class Quinquagesima(MovableFeast):
    """Represents Quinquagesima."""

    name = 'Quinquagesima'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Quinquagesima.

        Quinquagesima is the Sunday before Ash Wednesday.

        """
        return AshWednesday.date(year) - dt.timedelta(3)


class FatThursday(MovableFeast):
    """Represents Fat Thursday."""

    name = 'Fat Thursday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Fat Thursday.

        Fat Thursday is the Thursday before Ash Wednesday.

        """
        return AshWednesday.date(year) - dt.timedelta(6)


class ShroveMonday(MovableFeast):
    """Represents Shrove Monday."""

    name = 'Shrove Monday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Shrove Monday.

        Shrove Monday is the Monday before Ash Wednesday.

        """
        return AshWednesday.date(year) - dt.timedelta(2)


class MardiGras(MovableFeast):
    """Represents Mardi Gras."""

    name = 'Mardi Gras'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Mardi Gras.

        Mardi Gras is the Tuesday before Ash Wednesday.

        """
        return AshWednesday.date(year) - dt.timedelta(1)


class Sexagesima(MovableFeast):
    """Represents Sexagesima."""

    name = 'Sexagesima'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Sexagesima.

        Sexagesima is the Sunday before Quinquagesima.

        """
        return Quinquagesima.date(year) - dt.timedelta(7)


class Septuagesima(MovableFeast):
    """Represents Septuagesima."""

    name = 'Septuagesima'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Septuagesima.

        Septuagesima is the Sunday before Sexagesima.

        """
        return Sexagesima.date(year) - dt.timedelta(7)


class StMatthias(MovableFeast):
    """Represents the Feast of St. Matthias."""

    name = 'St. Matthias'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of the Feast of St. Matthias.

        The Feast of St. Matthias is generally February 24, but is moved to February 25 on leap
        years.

        """
        if calendar.isleap(year):
            return dt.date(year, 2, 25)
        return dt.date(year, 2, 24)


class StGabrielOfOurLadyOfSorrows(MovableFeast):
    """Represents the Feast of St. Gabriel of Our Lady of Sorrows."""

    name = 'St. Gabriel of Our Lady of Sorrows'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of the Feast of St. Gabriel of Our Lady of Sorrows.

        The Feast of St. Gabriel of Our Lady of Sorrows is generally February 27, but is moved to
        February 28 on leap years.

        """
        if calendar.isleap(year):
            return dt.date(year, 2, 28)
        return dt.date(year, 2, 27)


class LaetareSunday(MovableFeast):
    """Represents Laetare Sunday."""

    name = 'Laetare Sunday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Laetare Sunday.

        Lateare Sunday is the fourth Sunday of Lent.

        """
        return Easter.date(year) - dt.timedelta(21)


class PassionSunday(MovableFeast):
    """Represents Passion Sunday."""

    name = 'Passion Sunday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Passion Sunday.

        Passion Sunday is the second Sunday before Easter.

        """
        return Easter.date(year) - dt.timedelta(14)


class SevenSorrows(MovableFeast):
    """Represents the Feast of the Seven Sorrows."""

    name = 'The Seven Sorrows'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of the Feast of the Seven Sorrows.

        The Feast of the Seven Sorrows of Mary is the Friday of Passion Week.

        """
        return PalmSunday.date(year) - dt.timedelta(2)


class LadyDay(MovableFeast):
    """Represents Lady Day."""

    name = 'Lady Day'

    @functools.lru_cache()
    def date(year):
        """Calcualte the date of Lady Day.

        Lady Day is generally March 25, except when March 25 falls in Holy Week or the first week of
        Eastertide, in which case it is transfered to the Monday after Quasimodo Sunday, or if it
        falls on another Sunday, in which case it is transferred to the following Monday.

        """
        lady_day = dt.date(year, 3, 25)
        if PalmSunday.date(year) <= lady_day <= QuasimodoSunday.date(year):
            return QuasimodoSunday.date(year) + dt.timedelta(1)
        elif lady_day.weekday() == 6:
            return lady_day + dt.timedelta(1)
        else:
            return lady_day


class PalmSunday(MovableFeast):
    """Represents Palm Sunday."""

    name = 'Palm Sunday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Palm Sunday.

        Palm Sunday is the Sunday before Easter.

        """
        return Easter.date(year) - dt.timedelta(7)


class MondayOfHolyWeek(MovableFeast):
    """Represents the Monday of Holy Week."""

    name = 'Monday of Holy Week'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Monday in Holy Week."""
        return PalmSunday.date(year) + dt.timedelta(1)


class TuesdayOfHolyWeek(MovableFeast):
    """Represents the Tuesday of Holy Week."""

    name = 'Tuesday of Holy Week'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Tuesday in Holy Week."""
        return PalmSunday.date(year) + dt.timedelta(2)


class SpyWednesday(MovableFeast):
    """Represents Spy Wednesday."""

    name = 'Spy Wednesday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Spy Wednesday.

        Spy Wednesday is the Wednesday before Easter.

        """
        return Easter.date(year) - dt.timedelta(4)


class MaundyThursday(MovableFeast):
    """Represents Maundy Thursday."""

    name = 'Maundy Thursday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Maundy Thursday.

        Maundy Thursday is the Thursday before Easter.

        """
        return Easter.date(year) - dt.timedelta(3)


class GoodFriday(MovableFeast):
    """Represents Good Friday."""

    name = 'Good Friday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Good Friday.

        Good Friday is the Friday before Easter.

        """
        return Easter.date(year) - dt.timedelta(2)


class HolySaturday(MovableFeast):
    """Represents Holy Saturday."""

    name = 'Holy Saturday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Holy Saturday.

        Holy Saturday is the Saturday before Easter.

        """
        return Easter.date(year) - dt.timedelta(1)


class Easter(MovableFeast):
    """Represents Easter."""

    name = 'Easter'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Easter.

        This is an alias for `computus`.

        """
        return computus(year)


class EasterMonday(MovableFeast):
    """Represents Easter Monday."""

    name = 'Easter Monday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Easter Monday."""
        return Easter.date(year) + dt.timedelta(1)


class EasterTuesday(MovableFeast):
    """Represents Easter Tuesday."""

    name = 'Easter Tuesday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Easter Tuesday."""
        return Easter.date(year) + dt.timedelta(2)


class EasterWednesday(MovableFeast):
    """Represents Easter Wednesday."""

    name = 'Easter Wednesday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Easter Wednesday."""
        return Easter.date(year) + dt.timedelta(3)


class EasterThursday(MovableFeast):
    """Represents Easter Thursday."""

    name = 'Easter Thursday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Easter Thursday."""
        return Easter.date(year) + dt.timedelta(4)


class EasterFriday(MovableFeast):
    """Represents Easter Friday."""

    name = 'Easter Friday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Easter Friday."""
        return Easter.date(year) + dt.timedelta(5)


class EasterSaturday(MovableFeast):
    """Represents Easter Saturday."""

    name = 'Easter Saturday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Easter Saturday."""
        return Easter.date(year) + dt.timedelta(6)


class QuasimodoSunday(MovableFeast):
    """Represents Quasimodo Sunday."""
    
    name = 'Quasimodo Sunday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Quasimodo Sunday.

        Quasimodo Sunday is the first Sunday after Easter.

        """
        return Easter.date(year) + dt.timedelta(7)


class MisericordiaSunday(MovableFeast):
    """Represents Misericordia Sunday."""

    name = 'Misericordia Sunday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Misericordia Sunday.

        Misericordia Sunday is the second Sunday after Easter.

        """
        return Easter.date(year) + dt.timedelta(14)


class JubilateSunday(MovableFeast):
    """Represents Jubilate Sunday."""

    name = 'Jubilate Sunday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Jubilate Sunday.

        Jubilate Sunday is the third Sunday after Easter.

        """
        return Easter.date(year) + dt.timedelta(21)


class CantateSunday(MovableFeast):
    """Represents Cantate Sunday."""

    name = 'Cantate Sunday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Cantate Sunday.

        Cantate Sunday is the fourth Sunday after Easter.

        """
        return Easter.date(year) + dt.timedelta(28)


class MajorRogation(MovableFeast):
    """Represents the Major Rogation."""

    name = 'Major Rogation'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of the Major Rogation.

        The Major Rogation is generally April 25, unless it falls on Easter, in which case it is
        transferred to the following Tuesday.

        """
        major_rogation = dt.date(year, 4, 25)
        if major_rogation != Easter.date(year):
            return major_rogation
        else:
            return major_rogation + dt.timedelta(2)


class Ascension(MovableFeast):
    """Represents Ascension Thursday."""

    name = 'Ascension'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Ascension Thursday.

        Ascension Thursday is the fourtieth day of Eastertide.

        """
        return Easter.date(year) + dt.timedelta(39)


class MinorRogation(MovableFeast):
    """Represents the Minor Rogation."""
    
    name = 'Minor Rogation'

    @functools.lru_cache()
    def date(year):
        """Calculate the dates of the Minor Rogation.

        The Minor Rogation is the Monday, Tuesday, and Wednesday before Ascension Thursday.

        """
        return [Ascension.date(year) - dt.timedelta(i) for i in range(3, 0, -1)]


class Pentecost(MovableFeast):
    """Represents Pentecost."""

    name = 'Pentecost'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Pentecost.

        Pentecost is the fiftieth and final day of Eastertide.

        """
        return Easter.date(year) + dt.timedelta(49)


class PentecostMonday(MovableFeast):
    """Represents Pentecost Monday."""

    name = 'Pentecost Monday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Pentecost Monday."""
        return Pentecost.date(year) + dt.timedelta(1)


class PentecostTuesday(MovableFeast):
    """Represents Pentecost Tuesday."""

    name = 'Pentecost Tuesday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Pentecost Tuesday."""
        return Pentecost.date(year) + dt.timedelta(2)


class WhitEmbertide(MovableFeast):
    """Represents Whit Embertide."""

    name = 'Whit Embertide'

    @functools.lru_cache()
    def date(year):
        """Calculate the dates of Whit Embertide.

        Whit Embertide is the Wednesday, Friday, and Saturday after Pentecost.

        """
        return sorted([Pentecost.date(year) + dt.timedelta(i) for i in [3, 5, 6]])


class ThursdayInPentecostWeek(MovableFeast):
    """Represents Thursday in Pentecost Week."""

    name = 'Thursday in Pentecost Week'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Thursday in Pentecost Week."""
        return Pentecost.date(year) + dt.timedelta(4)


class TrinitySunday(MovableFeast):
    """Represents Trinity Sunday."""

    name = 'Trinity Sunday'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Trinity Sunday.

        Trinity Sunday is the Sunday after Pentecost.

        """
        return Pentecost.date(year) + dt.timedelta(7)


class CorpusChristi(MovableFeast):
    """Represents the Feast of Corpus Christi."""

    name = 'Corpus Christi'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of the Feast of Corpus Christi.

        The Feast of Corpus Christi is the Thursday after Trinity Sunday.

        """
        return TrinitySunday.date(year) + dt.timedelta(4)


class SacredHeart(MovableFeast):
    """Represents the Feast of the Sacred Heart."""

    name = 'The Sacred Heart'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of the Feast of the Sacred Heart.

        The Feast of the Sacred Heart is the Friday in the week after the Feast of Corpus Christi.

        """
        return CorpusChristi.date(year) + dt.timedelta(8)


class PetersPence(MovableFeast):
    """Represents Peter's Pence."""

    name = 'Peter\'s Pence'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of Peter's Pence.

        Peter's Pence is the Sunday nearest to the Feast of SS. Peter & Paul.

        """
        ss_peter_paul = dt.date(year, 6, 29)
        return ss_peter_paul + dt.timedelta(((2 - ss_peter_paul.weekday()) % 7) - 3)


class MichaelmasEmbertide(MovableFeast):
    """Represents Michaelmas Embertide."""

    name = 'Michaelmas Embertide'

    @functools.lru_cache()
    def date(year):
        """Calculate the dates of Michaelmas Embertide.

        Michaelmas Embertide is the Wednesday, Friday, and Saturday after the third Sunday of
        September.

        """
        first_sunday_in_september = (dt.date(year, 9, 1) +
            dt.timedelta(6 - dt.date(year, 9, 1).weekday()))
        third_sunday_in_september = first_sunday_in_september + dt.timedelta(14)
        return [third_sunday_in_september + dt.timedelta(i) for i in [3, 5, 6]]


class ChristTheKing(MovableFeast):
    """Represents the Feast of Christ the King."""

    name = 'Christ the King'

    @functools.lru_cache()
    def date(year):
        """Calculate the date of the Feast of Christ the King.

        The Feast of Christ the King is the last Sunday of October.

        """
        halloween = dt.date(year, 10, 31)
        return halloween - dt.timedelta((halloween.weekday() + 1) % 7)
