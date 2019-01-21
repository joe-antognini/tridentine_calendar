"""Utility functions."""

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
