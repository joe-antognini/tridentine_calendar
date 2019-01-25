"""Generate a liturgical calendar using the 1962 Roman Catholic rubrics."""

import argparse
import calendar
import datetime as dt
import json
import os
import urllib
from pkg_resources import resource_string

import icalendar as ical

from . import feast_dates
from .utils import ORDINALS
from .utils import add_domain_to_url_description

# Load the JSON data.
MOVABLE_FEASTS_DATA = json.loads(resource_string(__name__, 'movable_feasts_ferias_et_al.json'))
FIXED_FEASTS_DATA = json.loads(resource_string(__name__, 'fixed_feasts_ferias_et_al.json'))
SEASON_DATA = json.loads(resource_string(__name__, 'seasons.json'))


def get_args():
    """Define the command line arguments."""
    parser = argparse.ArgumentParser(description='Calculate a liturgical calendar.')
    parser.add_argument('--year', type=int, help='The year for which to calculate the calendar.')
    parser.add_argument('--file', help='Name of the ICS file to write the calendar to.')
    return parser.parse_args()


class LiturgicalCalendarEventUrl:
    """Contains information about a URL describing a feast, feria, or other event."""

    def __init__(self, url, description):
        """Instantiate a `LiturgicalCalendarEventUrl`.

        Args:
            url: A string with the URL.
            description: A string describing the URL that should be shown with the link.

        """
        self.url = url
        self.description = description

    @classmethod
    def from_json(cls, json_obj, default=None):
        """Instantiate a `LiturgicalCalendarEventUrl` object from a JSON object.

        Args:
            json_obj: An object resulting from parsing the JSON string describing the URL.

        Returns:
            A `LiturgicalCalendarEventUrl` object with the URL and description appropriately set.

        """
        if type(json_obj) is dict:
            description = add_domain_to_url_description(json_obj['url'], json_obj['description'])
            liturgical_calendar_event_url = cls(json_obj['url'], description)
        elif type(json_obj) is str:
            domain = urllib.parse.urlparse(json_obj).netloc
            if domain == 'en.wikipedia.org':
                description = os.path.basename(json_obj).replace('_', ' ')
                description = urllib.parse.unquote(description)
                description = add_domain_to_url_description(json_obj, description)
            else:
                description = add_domain_to_url_description(json_obj, default)
            liturgical_calendar_event_url = cls(json_obj, description)
        else:
            raise ValueError('json_obj must be dict or str, found {}.'.format(type(json_obj)))

        return liturgical_calendar_event_url

    def to_href(self):
        """Return the URL as an HTML HREF string."""
        return '<a href={url}>{description}</a>'.format(url=self.url, description=self.description)


class LiturgicalSeason:
    """A liturgical season."""

    def __init__(self, name, urls=None, color=None):
        """Instantiate a `LiturgicalSeason`.

        Args:
            name: string
                The name of the liturgical season.
            urls: list of `LiturgicalCalendarEventUrl`s.
                URLs with more information about the liturgical season.
            color: string
                The liturgical color of the season.

        """
        self.name = name
        self.urls = urls
        self.color = color

    @classmethod
    def from_json_key(cls, json_key):
        """Instantiate a `LiturgicalSeason` object from parsed JSON data."""
        json_obj = SEASON_DATA[json_key]
        if 'urls' in json_obj:
            urls = [LiturgicalCalendarEventUrl.from_json(elem) for elem in json_obj['urls']]
        if 'color' in json_obj:
            color = json_obj['color']
        elif  'season' in json_obj:
            color = LiturgicalSeason.from_json_key(json_obj['season']).color
        return cls(json_key, urls, color)
    
    @classmethod
    def from_date(cls, date):
        """Instantiate a `LiturgicalSeason` from a given date.

        Args:
            date: A `datetime.date` object.
        
        """
        # First determine the liturgical year.
        if (
            feast_dates.liturgical_year_start(date.year) <= date <=
            feast_dates.liturgical_year_end(date.year)
        ):
            year = date.year
        elif (
            feast_dates.liturgical_year_start(date.year + 1) <= date <=
            feast_dates.liturgical_year_end(date.year + 1)
        ):
            year = date.year + 1

        if date in [
            feast_dates.fat_thursday(year),
            feast_dates.shrove_monday(year),
            feast_dates.mardi_gras(year),
        ]:
            season_key = 'Shrovetide'
        elif feast_dates.liturgical_year_start(year) <= date < dt.date(year - 1, 12, 25):
            season_key = 'Advent'
        elif dt.date(year - 1, 12, 25) <= date < dt.date(year, 1, 6):
            season_key = 'Christmastide'
        elif dt.date(year, 1, 6) <= date < feast_dates.septuagesima(year):
            season_key = 'Time after Epiphany'
        elif (
            feast_dates.septuagesima(year) <= date < feast_dates.ash_wednesday(year)
        ):
            season_key = 'Septuagesima'
        elif (
            feast_dates.ash_wednesday(year) <= date < feast_dates.passion_sunday(year)
        ):
            season_key = 'Lent'
        elif (
            feast_dates.passion_sunday(year) <= date < feast_dates.palm_sunday(year)
        ):
            season_key = 'Passiontide'
        elif (
            feast_dates.palm_sunday(date.year) <= date < feast_dates.maundy_thursday(year)
        ):
            season_key = 'Holy Week'
        elif (
            feast_dates.maundy_thursday(year) <= date < feast_dates.easter(year)
        ):
            season_key = 'Paschal Triduum'
        elif feast_dates.easter(year) <= date < feast_dates.pentecost(year):
            season_key = 'Eastertide'
        elif feast_dates.pentecost(year) <= date < dt.date(year, 10, 31):
            season_key = 'Time after Pentecost'
        elif dt.date(year, 10, 31) <= date < dt.date(year, 11, 3):
            season_key = 'Hallowtide'
        elif dt.date(year, 11, 3) <= date <= feast_dates.liturgical_year_end(year):
            season_key = 'Time after Pentecost'
        else:
            raise ValueError('Wasn\'t able to calculate season for date {}.'.format(date))

        return LiturgicalSeason.from_json_key(season_key)

    def full_name(self, capitalize=True):
        """Return the name of the season, possibly with an article.

        Args:
            capitalize: boolean
                Whether to capitalize the first letter of the full name.

        Returns:
            A string with the name of the season, possibly with an article.

        """
        if self.name.startswith('Time after'):
            full_name = 'the ' + self.name
        else:
            full_name = self.name

        if capitalize:
            full_name = full_name[0].upper() + full_name[1:]

        return full_name


class LiturgicalCalendarEvent:
    """An event on the liturgical calendar.

    This could be a feast, a feria, or something else (such as a traditional or modern feast).

    """

    def __init__(
        self,
        date,
        name,
        urls=None,
        rank=None,
        color=None,
        titles=None,
        liturgical_event=None,
        holy_day=None,
        season=None,
    ):
        """Instantiate a `LiturgicalCalendarEvent`.

        Args:
            date: datetime.dat
                The date of the feast.
            name: string
                The event's name.
            urls: list of `LiturgicalCalendarEventUrl`
                Information about the URLs associated with the event.
            rank: int or None
                The class of the feast.
            color: string
                The liturgical color associated with the event, if any.
            titles: list of string
                For feast days of one or several saints
            liturgical_event: bool
                Whether there is a special liturgy associated with this event.
            holy_day: bool
                Whether the event is a Holy Day of Obligation.
            season: `LiturgicalSeason`
                The liturgical season the event falls in.

        """
        self.date = date
        self.name = name
        self.urls = urls
        self.rank = rank
        self.color = color
        self.titles = titles
        self.liturgical_event = liturgical_event
        self.holy_day = holy_day
        self.season = LiturgicalSeason.from_date(date)

    def full_name(self, capitalize=True):
        """Return the full name of the event, possibly with an article.

        For example, if the name is 'St. Nicholas', this will return 'The Feast of St. Nicholas'.
        If the name is 'St. Saturninus' this will return 'The Commemoration of St. Saturninus'.

        Args:
            captilazie: boolean
                Whether to capitalize the first letter.

        Returns:
            The full name of the event, possibly with an article.

        """
        the_feast_of_prefixes = ['St.', 'SS.', 'Pope', 'Our Lady', 'The']
        if self.name.split()[0] in the_feast_of_prefixes:
            if self.name.startswith('The'):
                name = self.name[0].lower() + self.name[1:]
            else:
                name = self.name
            if self.rank != 4:
                full_name = 'the Feast of ' + name
            else:
                full_name = 'the Commemoration of ' + name
        elif self.name.split()[0] in ['Basilica', 'Baptism']:
            if self.rank != 4:
                full_name = 'the Feast of the ' + self.name
            else:
                full_name = 'the Commemoration of the ' + self.name
        elif (self.name.split()[0] in ORDINALS.values() or
              self.name.startswith('Last Sunday') or
              self.name.startswith('Feast')
        ):
            full_name = 'the ' + self.name
        else:
            full_name = self.name

        if capitalize:
            full_name = full_name[0].upper() + full_name[1:]
        return full_name

    @classmethod
    def from_json(cls, date, json_obj, name=None):
        """Instantiate a `LiturgicalCalendarEvent` from the parsed JSON data.

        Args:
            date: datetime.date
                The date of the event.
            json_obj: dict
                The parsed JSON data for the event.
            name: string
                The name of the event.

        """
        name = json_obj.get('name', name)
        event = cls(date, name)
        if 'urls' in json_obj:
            event.urls = [
                LiturgicalCalendarEventUrl.from_json(elem, default=event.name)
                for elem in json_obj['urls']
            ]
        event.rank = json_obj.get('class')
        event.titles = json_obj.get('titles')
        event.liturgical_event = json_obj.get('liturgical_event')
        event.holy_day = json_obj.get('holy_day', False)
        event.season = LiturgicalSeason.from_date(date)

        if 'color' in json_obj:
            event.color = json_obj['color']
        else:
            if event.liturgical_event and event.rank != 4 and event.season.name != 'Lent':
                color = 'White'
                if event.titles:
                    red_titles = ['Martyr', 'Apostle', 'Evangelist']
                    for red_title in red_titles:
                        if red_title in event.titles:
                            color = 'Red'
            else:
                color = event.season.color
            event.color = color

        return event

    def generate_description(self, html_formatting=False):
        """Create a human-readable description of the event for the ICS file.

        Args:
            html_formatting: Whether to use HTML formatting for the URLs.
        
        Returns:
            A string with the description.

        """
        description = ''
        if self.holy_day:
            description += '{} is a Holy Day of Obligation.\n\n'.format(self.full_name())

        if not self.liturgical_event:
            description += '{} has no special liturgy.\n\n'.format(self.full_name())

        if self.urls:
            description += 'More information about {}:\n'.format(self.full_name(capitalize=False))
            for url_obj in self.urls:
                if html_formatting:
                    description += '• ' + url_obj.to_href() + '\n'
                else:
                    description += '• ' + url_obj.url + '\n'

        description += '\n'
        description += 'More information about {}:\n'.format(
                self.season.full_name(capitalize=False))
        for url_obj in self.season.urls:
            if html_formatting:
                description += '• ' + url_obj.to_href() + '\n'
            else:
                description += '• ' + url_obj.url + '\n'

        return description.rstrip()

    def is_fixed(self):
        date_str = self.date.strftime('%B %-d')
        fixed_feasts_on_date = [elem['name'] for elem in FIXED_FEASTS_DATA.get(date_str, [])]
        return (self.name in fixed_feasts_on_date)


class LiturgicalCalendar:
    """A liturgical calendar following the 1962 Roman Catholic rubrics."""

    def __init__(self, year):
        """Instantiate a `LiturgicalCalendar` object.

        Note that the liturgical year starts before the year given on the first Sunday of Advent.
        If the year given is 2000, then the liturgical year will start in late November 1999 and end
        in early December 2000.

        Args:
            year: int
                The liturgical year to calculate the calendar for.

        """
        self.year = year

        self.liturgical_year_start = feast_dates.liturgical_year_start(self.year)
        self.liturgical_year_end = feast_dates.liturgical_year_end(self.year)

        self.calendar = {}
        date = self.liturgical_year_start
        while date <= self.liturgical_year_end:
            self.calendar[date] = []
            date += dt.timedelta(1)

        # First we mark fixed solemnities.
        date = self.liturgical_year_start
        while date <= self.liturgical_year_end:
            date_str = date.strftime('%B %-d')
            if date_str in FIXED_FEASTS_DATA:
                for elem in FIXED_FEASTS_DATA[date_str]:
                    if elem.get('class') == 1:
                        event = LiturgicalCalendarEvent.from_json(date, elem)
                        self.calendar[date].append(event)
            date += dt.timedelta(1)

        # Now the movable solemnities.
        function_name_pairs = (
            (feast_dates.gaudete_sunday, 'Gaudete Sunday'),
            (feast_dates.advent_embertide, 'Advent Embertide'),
            (
                feast_dates.sunday_within_the_octave_of_xmas,
                'Sunday within the Octave of Christmas',
            ),
            (feast_dates.holy_name, 'Feast of the Holy Name'),
            (feast_dates.holy_family, 'Feast of the Holy Family'),
            (feast_dates.plough_monday, 'Plough Monday'),
            (feast_dates.septuagesima, 'Septuagesima'),
            (feast_dates.sexagesima, 'Sexagesima'),
            (feast_dates.quinquagesima, 'Quinquagesima'),
            (feast_dates.fat_thursday, 'Fat Thursday'),
            (feast_dates.shrove_monday, 'Shrove Monday'),
            (feast_dates.mardi_gras, 'Mardi Gras'),
            (feast_dates.ash_wednesday, 'Ash Wednesday'),
            (feast_dates.lenten_embertide, 'Lenten Embertide'),
            (feast_dates.st_matthias, 'St. Matthias'),
            (feast_dates.st_gabriel_of_our_lady_of_sorrows, 'St. Gabriel of Our Lady of Sorrows'),
            (feast_dates.laetare_sunday, 'Laetare Sunday'),
            (feast_dates.passion_sunday, 'Passion Sunday'),
            (feast_dates.seven_sorrows, 'The Seven Sorrows'),
            (feast_dates.palm_sunday, 'Palm Sunday'),
            (lambda x: feast_dates.palm_sunday(x) + dt.timedelta(1), 'Monday of Holy Week'),
            (lambda x: feast_dates.palm_sunday(x) + dt.timedelta(2), 'Tuesday of Holy Week'),
            (feast_dates.spy_wednesday, 'Spy Wednesday'),
            (feast_dates.maundy_thursday, 'Maundy Thursday'),
            (feast_dates.good_friday, 'Good Friday'),
            (feast_dates.holy_saturday, 'Holy Saturday'),
            (feast_dates.easter, 'Easter'),
            (lambda x: feast_dates.easter(x) + dt.timedelta(1), 'Easter Monday'),
            (lambda x: feast_dates.easter(x) + dt.timedelta(2), 'Easter Tuesday'),
            (lambda x: feast_dates.easter(x) + dt.timedelta(3), 'Easter Wednesday'),
            (lambda x: feast_dates.easter(x) + dt.timedelta(4), 'Easter Thursday'),
            (lambda x: feast_dates.easter(x) + dt.timedelta(5), 'Easter Friday'),
            (lambda x: feast_dates.easter(x) + dt.timedelta(6), 'Easter Saturday'),
            (feast_dates.quasimodo_sunday, 'Quasimodo Sunday'),
            (feast_dates.jubilate_sunday, 'Jubilate Sunday'),
            (feast_dates.misericordia_sunday, 'Misericordia Sunday'),
            (feast_dates.cantate_sunday, 'Cantate Sunday'),
            (feast_dates.major_rogation, 'Major Rogation'),
            (feast_dates.ascension, 'Ascension'),
            (feast_dates.minor_rogation, 'Minor Rogation'),
            (feast_dates.pentecost, 'Pentecost'),
            (lambda x: feast_dates.pentecost(x) + dt.timedelta(1), 'Pentecost Monday'),
            (lambda x: feast_dates.pentecost(x) + dt.timedelta(2), 'Pentecost Tuesday'),
            (
                lambda x: feast_dates.pentecost(x) + dt.timedelta(4),
                'Thursday in Pentecost Week',
            ),
            (feast_dates.whit_embertide, 'Whit Embertide'),
            (feast_dates.trinity_sunday, 'Trinity Sunday'),
            (feast_dates.corpus_christi, 'Corpus Christi'),
            (feast_dates.sacred_heart, 'Feast of the Sacred Heart'),
            (feast_dates.peters_pence, 'Peter\'s Pence'),
            (feast_dates.michaelmas_embertide, 'Michaelmas Embertide'),
            (feast_dates.christ_the_king, 'Christ the King'),
        )

        for date_fn, name in function_name_pairs:
            date = date_fn(self.year)
            if type(date) is list:
                for elem in date:
                    event = LiturgicalCalendarEvent.from_json(elem, MOVABLE_FEASTS_DATA[name], name)
                    self.calendar[elem].append(event)
            else:
                event = LiturgicalCalendarEvent.from_json(date, MOVABLE_FEASTS_DATA[name], name)
                self.calendar[date].append(event)

        # Mark Sundays, starting with Advent
        for i in range(1, 5):
            if i == 3:
                continue
            date = self.liturgical_year_start + dt.timedelta(7 * (i - 1))
            event = LiturgicalCalendarEvent(
                date, 
                name=ORDINALS[i] + ' Sunday of Advent',
                liturgical_event=True,
                rank=1,
            )
            self.calendar[date].append(event)

        # Time after Epiphany.
        i = 2
        date = feast_dates.holy_family(self.year) + dt.timedelta(7)
        while date < feast_dates.septuagesima(self.year):
            event = LiturgicalCalendarEvent(
                date, 
                name=ORDINALS[i] + ' Sunday after Epiphany',
                liturgical_event=True,
                rank=2,
            )
            self.calendar[date].append(event)
            i += 1
            date += dt.timedelta(7)

        # Lent.
        for i in range(1, 4):
            date = feast_dates.quinquagesima(self.year) + dt.timedelta(7 * i)
            event = LiturgicalCalendarEvent(
                date, 
                name=ORDINALS[i] + ' Sunday of Lent',
                liturgical_event=True,
                rank=1,
            )
            self.calendar[date].append(event)

        # Eastertide.
        date = feast_dates.cantate_sunday(self.year) + dt.timedelta(7)
        event = LiturgicalCalendarEvent(date, 'Fifth Sunday after Easter', liturgical_event=True)
        self.calendar[date].append(event)

        date = feast_dates.ascension(self.year) + dt.timedelta(3)
        event = LiturgicalCalendarEvent(date, 'Sunday after Ascension', liturgical_event=True)
        self.calendar[date].append(event)

        # Time after Pentecost.
        i = 2
        date = feast_dates.trinity_sunday(self.year) + dt.timedelta(7)
        while date <= self.liturgical_year_end - dt.timedelta(7):
            event = LiturgicalCalendarEvent(
                date, 
                name=ORDINALS[i] + ' Sunday after Pentecost',
                liturgical_event=True,
                rank=2,
            )
            self.calendar[date].append(event)
            i += 1
            date += dt.timedelta(7)

        event = LiturgicalCalendarEvent(
            date, 'Last Sunday after Pentecost', liturgical_event=True, rank=2)
        self.calendar[date].append(event)

        # Then second class fixed feasts or lower.
        date = self.liturgical_year_start
        while date <= self.liturgical_year_end:
            date_str = date.strftime('%B %-d')
            if date_str in FIXED_FEASTS_DATA:
                for elem in FIXED_FEASTS_DATA[date_str]:
                    if elem.get('class') != 1:
                        event = LiturgicalCalendarEvent.from_json(date, elem)
                        self.calendar[date].append(event)
            self.calendar[date] = sorted(self.calendar[date], key=_feast_sort_key)
            date += dt.timedelta(1)

    def __getitem__(self, key):
        return self.calendar[key]

    def to_ical(self, html_formatting=False):
        """Write out the calendar to ICS format."""
        ics_calendar = ical.Calendar()
        ics_calendar.add('x-wr-calname', 'Tridentine calendar')
        ics_calendar.add(
            'x-wr-caldesc',
            'Liturgical calendar using the 1962 Roman Catholic rubrics.',
        )
        date = self.liturgical_year_start
        while date <= self.liturgical_year_end:
            for i, elem in enumerate(self.calendar[date]):
                ics_name = elem.name
                description = ''

                if i > 0 and elem.liturgical_event:
                    outranking_feast = self.calendar[date][0]
                    ics_name = '› ' + ics_name
                    if outranking_feast.is_fixed() and elem.is_fixed():
                        description += '{} is outranked by {}.\n\n'.format(
                            elem.full_name(capitalize=True),
                            outranking_feast.full_name(capitalize=False),
                        )
                    else:
                        description += 'This year {} is outranked by {}.\n\n'.format(
                            elem.full_name(capitalize=False),
                            outranking_feast.full_name(capitalize=False),
                        )
                elif not elem.liturgical_event:
                    ics_name = '» ' + ics_name

                description += elem.generate_description(html_formatting)
                description = description.strip()
                ics_event = ical.Event()
                ics_event.add('summary', ics_name)
                ics_event.add('dtstart', date)
                ics_event.add('description', description)
                ics_calendar.add_component(ics_event)
            date += dt.timedelta(1)
        return ics_calendar.to_ical()


def _feast_sort_key(feast):
    """Provides a key to help sort feasts.

    Args:
        feast: A `LiturgicalEvent` object.

    Returns:
        The rank of the feast if it has one and is a liturgical event, otherwise 4.

    """
    if not feast.liturgical_event or not feast.rank:
        return 4
    else:
        return feast.rank

    
if __name__ == '__main__':
    args = get_args()
    litcal = LiturgicalCalendar(args.year)
    with open(args.file, 'w') as f:
        f.writelines(litcal.to_ics())
