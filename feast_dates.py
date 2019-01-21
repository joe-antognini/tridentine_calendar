"""Functions to calculate the dates of movable feasts."""

import calendar
import datetime as dt
import functools


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


@functools.lru_cache()
def liturgical_year_start(year):
    """Calculate the start of the liturgical year.

    The start of the liturgical year is the First Sunday of Advent.  This date is calculated for the
    liturgical year for which Easter falls in the given year.  As a consequence, the start of the
    liturgical year will fall on the previous year.  For example, if the year 2000 is provided as an
    argument, the resulting start of the liturgical year will be in late November 1999.

    Args:
        year: int

    Returns:
        A `datetime.date` object.

    """
    xmas = dt.date(year - 1, 12, 25)
    return xmas - dt.timedelta(xmas.weekday() + 22)


@functools.lru_cache()
def liturgical_year_end(year):
    """Calculate the last day of the liturgical year.

    The end of the liturgical year is the Saturday before the First Sunday of Advent of the
    following liturgical year.

    Args:
        year: int

    Returns:
        A `datetime.date` object.

    """
    next_xmas = dt.date(year, 12, 25)
    return next_xmas - dt.timedelta(next_xmas.weekday() + 23)


@functools.lru_cache()
def gaudete_sunday_date(year):
    """Calculate the date of Gaudete Sunday.

    Gaudete Sunday is the third Sunday of Advent.

    """
    xmas = dt.date(year - 1, 12, 25)
    return xmas - dt.timedelta(xmas.weekday() + 8)


@functools.lru_cache()
def advent_embertide_dates(year):
    """Calculate the dates of Advent Embertide.

    Advent Embertide is the Wednesday, Friday, and Saturday after Gaudete Sunday.

    """
    return sorted([gaudete_sunday_date(year) + dt.timedelta(i) for i in [3, 5, 6]])


@functools.lru_cache()
def holy_name_date(year):
    """"Calculate the date of the Feast of the Holy Name.

    The Feast of the Holy Name is generally the first Sunday of the year, unless the first
    Sunday falls on January 1, January 6, or January 7, in which case the Feast of the Holy Name
    is moved to January 2.

    """
    new_years_day = dt.date(year, 1, 1)
    holy_name = new_years_day + dt.timedelta(6 - new_years_day.weekday())
    if holy_name in [new_years_day, dt.date(year, 1, 6), dt.date(year, 1, 7)]:
        return dt.date(year, 1, 2)
    return holy_name


@functools.lru_cache()
def holy_family_date(year):
    """Calculate the date of the Feast of the Holy Family.

    The Feast of the Holy Family is the first Sunday after Three Kings Day.

    """
    epiphany = dt.date(year, 1, 6)
    delta = dt.timedelta(6 - epiphany.weekday())
    if delta == dt.timedelta(0):
        delta = dt.timedelta(7)
    return epiphany + delta


@functools.lru_cache()
def plough_monday_date(year):
    """Calculate the date of Plough Monday.

    Plough Monday is the first Monday after Three Kings Day.

    """
    epiphany = dt.date(year, 1, 6)
    if epiphany.weekday() == 6:
        return epiphany + dt.timedelta(1)
    return holy_family_date(year) + dt.timedelta(1)


@functools.lru_cache()
def ash_wednesday_date(year):
    """Calculate the date of Ash Wednesday.

    Ash Wednesday is forty days prior to Easter, excluding Sundays.

    """
    return easter_date(year) - dt.timedelta(46)


@functools.lru_cache()
def lenten_embertide_dates(year):
    """Calculate the dates of Lenten Embertide.

    Lenten Embertide is the Wednesday, Friday, and Saturday after the first Sunday of Lent.

    """
    return [ash_wednesday_date(year) + dt.timedelta(i) for i in [7, 9, 10]]


@functools.lru_cache()
def quinquagesima_date(year):
    """Calculate the date of Quinquagesima.

    Quinquagesima is the Sunday before Ash Wednesday.

    """
    return ash_wednesday_date(year) - dt.timedelta(3)


@functools.lru_cache()
def fat_thursday_date(year):
    """Calculate the date of Fat Thursday.

    Fat Thursday is the Thursday before Ash Wednesday.

    """
    return ash_wednesday_date(year) - dt.timedelta(6)


@functools.lru_cache()
def shrove_monday_date(year):
    """Calculate the date of Shrove Monday.

    Shrove Monday is the Monday before Ash Wednesday.

    """
    return ash_wednesday_date(year) - dt.timedelta(2)


@functools.lru_cache()
def mardi_gras_date(year):
    """Calculate the date of Mardi Gras.

    Mardi Gras is the Tuesday before Ash Wednesday.

    """
    return ash_wednesday_date(year) - dt.timedelta(1)


@functools.lru_cache()
def sexagesima_date(year):
    """Calculate the date of Sexagesima.

    Sexagesima is the Sunday before Quinquagesima.

    """
    return quinquagesima_date(year) - dt.timedelta(7)


@functools.lru_cache()
def septuagesima_date(year):
    """Calculate the date of Septuagesima.

    Septuagesima is the Sunday before Sexagesima.

    """
    return sexagesima_date(year) - dt.timedelta(7)


@functools.lru_cache()
def st_matthias_date(year):
    """Calculate the date of the Feast of St. Matthias.

    The Feast of St. Matthias is generally February 24, but is moved to February 25 on leap years.

    """
    if calendar.isleap(year):
        return dt.date(year, 2, 25)
    return dt.date(year, 2, 24)


@functools.lru_cache()
def st_gabriel_of_our_lady_of_sorrows_date(year):
    """Calculate the date of the Feast of St. Gabriel of Our Lady of Sorrows.

    The Feast of St. Gabriel of Our Lady of Sorrows is generally February 27, but is moved to
    February 28 on leap years.

    """
    if calendar.isleap(year):
        return dt.date(year, 2, 28)
    return dt.date(year, 2, 27)


@functools.lru_cache()
def laetare_sunday_date(year):
    """Calculate the date of Laetare Sunday.

    Lateare Sunday is the fourth Sunday of Lent.

    """
    easter = computus(year)
    return easter - dt.timedelta(21)


@functools.lru_cache()
def passion_sunday_date(year):
    """Calculate the date of Passion Sunday.

    Passion Sunday is the second Sunday before Easter.

    """
    easter_date = computus(year)
    return easter_date - dt.timedelta(14)


@functools.lru_cache()
def seven_sorrows_date(year):
    """Calculate the date of the Feast of the Seven Sorrows.

    The Feast of the Seven Sorrows of Mary is the Friday of Passion Week.

    """
    return palm_sunday_date(year) - dt.timedelta(2)


@functools.lru_cache()
def lady_day_date(year):
    """Calcualte the date of Lady Day.

    Lady Day is generally March 25, except when March 25 falls in Holy Week or the first week of
    Eastertide, in which case it is transfered to the Monday after Quasimodo Sunday, or if it falls
    on another Sunday, in which case it is transferred to the following Monday.

    """
    lady_day = dt.date(year, 3, 25)
    if palm_sunday_date(year) <= lady_day <= quasimodo_sunday_date(year):
        return quasimodo_sunday_date(year) + dt.timedelta(1)
    elif lady_day.weekday() == 6:
        return lady_day + dt.timedelta(1)
    else:
        return lady_day


@functools.lru_cache()
def palm_sunday_date(year):
    """Calculate the date of Palm Sunday.

    Palm Sunday is the Sunday before Easter.

    """
    return easter_date(year) - dt.timedelta(7)


@functools.lru_cache()
def spy_wednesday_date(year):
    """Calculate the date of Spy Wednesday.

    Spy Wednesday is the Wednesday before Easter.

    """
    return easter_date(year) - dt.timedelta(4)


@functools.lru_cache()
def maundy_thursday_date(year):
    """Calculate the date of Maundy Thursday.

    Maundy Thursday is the Thursday before Easter.

    """
    return easter_date(year) - dt.timedelta(3)


@functools.lru_cache()
def good_friday_date(year):
    """Calculate the date of Good Friday.

    Good Friday is the Friday before Easter.

    """
    return easter_date(year) - dt.timedelta(2)


@functools.lru_cache()
def holy_saturday_date(year):
    """Calculate the date of Holy Saturday.

    Holy Saturday is the Saturday before Easter.

    """
    return easter_date(year) - dt.timedelta(1)


@functools.lru_cache()
def easter_date(year):
    """Calculate the date of Easter.

    This is an alias for `computus`.

    """
    return computus(year)


@functools.lru_cache()
def quasimodo_sunday_date(year):
    """Calculate the date of Quasimodo Sunday.

    Quasimodo Sunday is the first Sunday after Easter.

    """
    return easter_date(year) + dt.timedelta(7)


@functools.lru_cache()
def jubilate_sunday_date(year):
    """Calculate the date of Jubilate Sunday.

    Jubilate Sunday is the second Sunday after Easter.

    """
    easter_date = computus(year)
    return easter_date + dt.timedelta(14)


@functools.lru_cache()
def misericordia_sunday_date(year):
    """Calculate the date of Misericordia Sunday.

    Misericordia Sunday is the third Sunday after Easter.

    """
    easter_date = computus(year)
    return easter_date + dt.timedelta(21)


@functools.lru_cache()
def cantate_sunday_date(year):
    """Calculate the date of Cantate Sunday.

    Cantate Sunday is the fourth Sunday after Easter.

    """
    easter_date = computus(year)
    return easter_date + dt.timedelta(28)


@functools.lru_cache()
def major_rogation_date(year):
    """Calculate the date of the Major Rogation.

    The Major Rogation is generally April 25, unless it falls on Easter, in which case it is
    transferred to the following Tuesday.

    """
    easter_date = computus(year)
    major_rogation = dt.date(year, 4, 25)
    if major_rogation != easter_date:
        return major_rogation
    else:
        return major_rogation + dt.timedelta(2)


@functools.lru_cache()
def ascension_date(year):
    """Calculate the date of Ascension Thursday.

    Ascension Thursday is the fourtieth day of Eastertide.

    """
    easter_date = computus(year)
    return easter_date + dt.timedelta(39)


@functools.lru_cache()
def minor_rogation_dates(year):
    """Calculate the dates of the Minor Rogation.

    The Minor Rogation is the Monday, Tuesday, and Wednesday before Ascension Thursday.

    """
    return [ascension_date(year) - dt.timedelta(i) for i in range(3, 0, -1)]


@functools.lru_cache()
def pentecost_date(year):
    """Calculate the date of Pentecost.

    Pentecost is the fiftieth and final day of Eastertide.

    """
    easter_date = computus(year)
    return easter_date + dt.timedelta(49)


@functools.lru_cache()
def whit_embertide_dates(year):
    """Calculate the dates of Whit Embertide.

    Whit Embertide is the Wednesday, Friday, and Saturday after Pentecost.

    """
    return sorted([pentecost_date(year) + dt.timedelta(i) for i in [3, 5, 6]])


@functools.lru_cache()
def trinity_sunday_date(year):
    """Calculate the date of Trinity Sunday.

    Trinity Sunday is the Sunday after Pentecost.

    """
    return pentecost_date(year) + dt.timedelta(7)


@functools.lru_cache()
def corpus_christi_date(year):
    """Calculate the date of the Feast of Corpus Christi.

    The Feast of Corpus Christi is the Thursday after Trinity Sunday.

    """
    return trinity_sunday_date(year) + dt.timedelta(4)


@functools.lru_cache()
def sacred_heart_date(year):
    """Calculate the date of the Feast of the Sacred Heart.

    The Feast of the Sacred Heart is the Friday in the week after the Feast of Corpus Christi.

    """
    return corpus_christi_date(year) + dt.timedelta(8)


@functools.lru_cache()
def peters_pence_date(year):
    """Calculate the date of Peter's Pence.

    Peter's Pence is the Sunday nearest to the Feast of SS. Peter & Paul.

    """
    ss_peter_paul = dt.date(year, 6, 29)
    return ss_peter_paul + dt.timedelta(((2 - ss_peter_paul.weekday()) % 7) - 3)


@functools.lru_cache()
def michaelmas_embertide_dates(year):
    """Calculate the dates of Michaelmas Embertide.

    Michaelmas Embertide is the Wednesday, Friday, and Saturday after the third Sunday of
    September.

    """
    first_sunday_in_september = (dt.date(year, 9, 1) +
        dt.timedelta(6 - dt.date(year, 9, 1).weekday()))
    third_sunday_in_september = first_sunday_in_september + dt.timedelta(14)
    return [third_sunday_in_september + dt.timedelta(i) for i in [3, 5, 6]]


@functools.lru_cache()
def christ_the_king_date(year):
    """Calculate the date of the Feast of Christ the King.

    The Feast of Christ the King is the last Sunday of October.

    """
    halloween = dt.date(year, 10, 31)
    return halloween - dt.timedelta((halloween.weekday() + 1) % 7)
