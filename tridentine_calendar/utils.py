"""Utility functions."""

import datetime as dt
import functools
import urllib

ORDINALS = {
    1: 'First',
    2: 'Second',
    3: 'Third',
    4: 'Fourth',
    5: 'Fifth',
    6: 'Sixth',
    7: 'Seventh',
    8: 'Eighth',
    9: 'Ninth',
    10: 'Tenth',
    11: 'Eleventh',
    12: 'Twelfth',
    13: 'Thirteenth',
    14: 'Fourteenth',
    15: 'Fifteenth',
    16: 'Sixteenth',
    17: 'Seventeenth',
    18: 'Eighteenth',
    19: 'Nineteenth',
    20: 'Twentieth',
    21: 'Twenty-first',
    22: 'Twenty-second',
    23: 'Twenty-third',
    24: 'Twenty-fourth',
    25: 'Twenty-fifth',
    26: 'Twenty-sixth',
    27: 'Twenty-seventh',
}


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


def liturgical_year(date):
    """Determine the liturgical year the date belongs to.

    For most dates this will be equal to the date's year.  However, for dates within Advent and the
    first part of Christmastide the liturgical year will be the following year.  Thus, January 1,
    2000 belongs to the liturgical year of 2000, whereas December 24, 2000 belongs to the liturgical
    year of 2001.

    Args:
        date: A `datetime.date` object.

    Returns:
        The liturgical year as an integer.
    
    """
    if date <= liturgical_year_end(date.year):
        return date.year
    else:
        return date.year + 1


def add_domain_to_url_description(url, description=None):
    """Add the domain name to the description in parentheses.

    ```
    >>> url = 'https://en.wikipedia.org/Saturnin'
    >>> add_domain_to_url_description(url)
    Saturnin (Wikipedia)
    ```

    Args:
        url: str
            The URL.
        description: str
            An optional description for the URL.  If no description exists, this function will try
            to use the URL to generate a description.  Currently this only works for Wikipedia
            domains.

    Returns:
        A string with the description and the domain name in parentheses afterwards.

    """
    domain = urllib.parse.urlparse(url).netloc
    if domain == 'en.wikipedia.org':
        domain_name = 'Wikipedia'
    elif domain == 'www.newadvent.org':
        domain_name = 'New Advent'
    elif domain == 'fisheaters.com':
        domain_name = 'Fish Eaters'
    else:
        domain_name = ''

    return '{} ({})'.format(description, domain_name)
