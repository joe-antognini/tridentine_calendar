"""Utility functions."""

import os
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


def description_from_url(url, default=None):
    """Try to reate a URL description from the URL itself.

    For Wikipedia pages this will parse the title of the page from the URL and use that as the
    description.  For other domains this will return `None`.

    Args:
        json_obj: An object that results from parsing the JSON string of the URL.  This should
            be either a `dict` or a `str`.

    Returns:
        A string with the title of the webpage for Wikipedia domains and `None` otherwise.

    """
    netloc = urllib.parse.urlparse(url).netloc
    if netloc == 'en.wikipedia.org':
        return os.path.basename(url) + ' (Wikipedia)'
    elif netloc == 'www.newadvent.org':
        return default + ' (New Advent)'
    elif netloc == 'fisheaters.com':
        return default + ' (Fish Eaters)'
    else:
        return default
