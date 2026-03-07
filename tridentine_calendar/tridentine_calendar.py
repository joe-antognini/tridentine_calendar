"""Generate a liturgical calendar using the 1962 Roman Catholic rubrics."""

import argparse
import calendar
import csv
import datetime as dt
import io
import json
import os
import urllib

import icalendar as ical

from importlib import resources

from . import movable_feasts as mf
from . import utils
from .i18n import Translator
from .utils import add_domain_to_url_description
from .utils import gen_uid
from .utils import iterate_liturgical_year
from .utils import liturgical_year_end
from .utils import liturgical_year_start

# Load the JSON data.
MF_DATA = json.loads(resources.read_text(__name__, 'movable_feasts_ferias_et_al.json'))
FIXED_FEASTS_DATA = json.loads(
    resources.read_text(__name__, 'fixed_feasts_ferias_et_al.json'))
SEASON_DATA = json.loads(resources.read_text(__name__, 'seasons.json'))


def get_args():
    """Define the command line arguments."""
    parser = argparse.ArgumentParser(description='Calculate a liturgical calendar.')
    parser.add_argument(
        '--year', type=int, help='The year for which to calculate the calendar.')
    parser.add_argument('--file', help='Name of the ICS file to write the calendar to.')
    return parser.parse_args()


class LiturgicalCalendarEventUrl:
    """Contains information about a URL describing a feast, feria, or other event."""

    def __init__(self, url, description):
        """Instantiate a `LiturgicalCalendarEventUrl`.

        Args:
            url: str
                A string with the URL.
            description: A string describing the URL that should be shown with the link.

        """
        self.url = url
        self.description = description

    @classmethod
    def from_json(cls, json_obj, default=None):
        """Instantiate a `LiturgicalCalendarEventUrl` object from a JSON object.

        Args:
            json_obj:
                An object resulting from parsing the JSON string describing the URL.

        Returns:
            A `LiturgicalCalendarEventUrl` object with the URL and description
            appropriately set.

        """
        if isinstance(json_obj, dict):
            description = add_domain_to_url_description(
                json_obj['url'], json_obj['description'])
            liturgical_calendar_event_url = cls(json_obj['url'], description)
        elif isinstance(json_obj, str):
            domain = urllib.parse.urlparse(json_obj).netloc
            if domain == 'en.wikipedia.org':
                description = os.path.basename(json_obj).replace('_', ' ')
                description = urllib.parse.unquote(description)
                description = add_domain_to_url_description(json_obj, description)
            else:
                description = add_domain_to_url_description(json_obj, default)
            liturgical_calendar_event_url = cls(json_obj, description)
        else:
            raise ValueError(f'json_obj must be dict or str, found {type(json_obj)}.')

        return liturgical_calendar_event_url

    def to_href(self):
        """Return the URL as an HTML HREF string."""
        return f'<a href={self.url}>{self.description}</a>'


class LiturgicalSeason:
    """A liturgical season."""

    def __init__(self, name, urls=None, color=None, lang='en', translator=None):
        """Instantiate a `LiturgicalSeason`.

        Args:
            name: string
                The name of the liturgical season.
            urls: list of `LiturgicalCalendarEventUrl`s.
                URLs with more information about the liturgical season.
            color: string
                The liturgical color of the season.
            lang: string
                The language of the season.
            translator: A `Translator` object.

        """
        self.name = name
        self.urls = urls
        self.color = color
        self.lang = lang
        self.translator = translator
        if self.translator is None:
            self.translator = Translator(self.lang)

    @classmethod
    def from_json_key(cls, json_key, lang='en', translator=None):
        """Instantiate a `LiturgicalSeason` object from parsed JSON data."""
        json_obj = SEASON_DATA[json_key]
        if 'urls' in json_obj:
            urls = [
                LiturgicalCalendarEventUrl.from_json(elem, json_key)
                for elem in json_obj['urls']
            ]
        if 'color' in json_obj:
            color = json_obj['color']
        elif 'season' in json_obj:
            color = LiturgicalSeason.from_json_key(json_obj['season'], lang, translator).color
        return cls(json_key, urls, color, lang, translator)

    @classmethod
    def from_date(cls, date, lang='en', translator=None):
        """Instantiate a `LiturgicalSeason` from a given date.

        Args:
            date: A `datetime.date` object.
            lang: string
            translator: A `Translator` object.

        """
        # First determine the liturgical year.
        year = utils.liturgical_year(date)

        if date in [
            mf.FatThursday.date(year),
            mf.ShroveMonday.date(year),
            mf.MardiGras.date(year),
        ]:
            season_key = 'Shrovetide'
        elif liturgical_year_start(year) <= date < dt.date(year - 1, 12, 25):
            season_key = 'Advent'
        elif dt.date(year - 1, 12, 25) <= date < dt.date(year, 1, 6):
            season_key = 'Christmastide'
        elif dt.date(year, 1, 6) <= date < mf.Septuagesima.date(year):
            season_key = 'Time after Epiphany'
        elif mf.Septuagesima.date(year) <= date < mf.AshWednesday.date(year):
            season_key = 'Septuagesima'
        elif mf.AshWednesday.date(year) <= date < mf.PassionSunday.date(year):
            season_key = 'Lent'
        elif mf.PassionSunday.date(year) <= date < mf.PalmSunday.date(year):
            season_key = 'Passiontide'
        elif mf.PalmSunday.date(date.year) <= date < mf.MaundyThursday.date(year):
            season_key = 'Holy Week'
        elif mf.MaundyThursday.date(year) <= date < mf.Easter.date(year):
            season_key = 'Paschal Triduum'
        elif mf.Easter.date(year) <= date < mf.Pentecost.date(year):
            season_key = 'Eastertide'
        elif mf.Pentecost.date(year) <= date < dt.date(year, 10, 31):
            season_key = 'Time after Pentecost'
        elif dt.date(year, 10, 31) <= date < dt.date(year, 11, 3):
            season_key = 'Hallowtide'
        elif dt.date(year, 11, 3) <= date <= liturgical_year_end(year):
            season_key = 'Time after Pentecost'
        else:
            raise ValueError(f'Wasn\'t able to calculate season for date {date}.')

        return LiturgicalSeason.from_json_key(season_key, lang, translator)

    def full_name(self, capitalize=True):
        """Return the name of the season, possibly with an article.

        Args:
            capitalize: boolean
                Whether to capitalize the first letter of the full name.

        Returns:
            A string with the name of the season, possibly with an article.

        """
        translated_name = self.translator.translate(self.name)
        if self.lang == 'ja':
            full_name = translated_name
        else:
            if self.name.startswith('Time after'):
                full_name = 'the ' + translated_name
            else:
                full_name = translated_name

        if capitalize:
            full_name = full_name[0].upper() + full_name[1:]

        return full_name


class LiturgicalCalendarEvent:
    """An event on the liturgical calendar.

    This could be a feast, a feria, or something else (such as a traditional or modern
    feast).

    """

    def __init__(
        self,
        date,
        name,
        urls=None,
        rank=None,
        color=None,
        titles=None,
        liturgical_event=True,
        feast=True,
        holy_day=False,
        addition=False,
        is_vigil=False,
        season=None,
        lang='en',
        translator=None,
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
            feast: bool
                Whether the event is a feast or a feria.
            addition: bool
                Whether this event is a liturgical event that occurs in addition to any
                other liturgical event of the day (e.g., Major Rogation).  These events
                do not follow the usual rules of precedence.
            holy_day: bool
                Whether the event is a Holy Day of Obligation.
            is_vigil: bool
                Whether or not the event is a vigil.
            season: `LiturgicalSeason`
                The liturgical season the event falls in.
            lang: string
                The language of the event.
            translator: A `Translator` object.

        """
        self.date = date
        self.name = name
        self.urls = urls
        self.rank = rank
        self.color = color
        self.titles = titles
        self.liturgical_event = liturgical_event
        self.feast = feast
        self.addition = addition
        self.holy_day = holy_day
        self.is_vigil = is_vigil
        self.lang = lang
        self.translator = translator
        if self.translator is None:
            self.translator = Translator(self.lang)
        self.season = LiturgicalSeason.from_date(date, self.lang, self.translator)

        if color is None:
            if all([
                self.liturgical_event,
                self.rank != 4,
                self.is_fixed(),
                not (self.rank != 1 and self.season.name in ['Lent', 'Passiontide']),
            ]):
                self.color = 'White'
                if self.titles:
                    red_titles = ['Martyr', 'Apostle', 'Evangelist']
                    for red_title in red_titles:
                        if red_title in self.titles:
                            self.color = 'Red'
            else:
                self.color = self.season.color

    def full_name(self, capitalize=True):
        """Return the full name of the event, possibly with an article.

        For example, if the name is 'St. Nicholas', this will return 'The Feast of St.
        Nicholas'.  If the name is 'St. Saturninus' this will return 'The Commemoration
        of St. Saturninus'.

        Args:
            capitalize: boolean
                Whether to capitalize the first letter.

        Returns:
            The full name of the event, possibly with an article.

        """
        full_name = self.translator.format_feast_full_name(self.name, self.rank)

        if capitalize:
            full_name = full_name[0].upper() + full_name[1:]
        return full_name

    @classmethod
    def from_json(cls, date, json_obj, name=None, lang='en', translator=None):
        """Instantiate a `LiturgicalCalendarEvent` from the parsed JSON data.

        Args:
            date: datetime.date
                The date of the event.
            json_obj: dict
                The parsed JSON data for the event.
            name: string
                The name of the event.
            lang: string
            translator: A `Translator` object.

        """
        name = json_obj.get('name', name)
        event = cls(
            date,
            name,
            rank=json_obj.get('class'),
            titles=json_obj.get('titles'),
            liturgical_event=json_obj.get('liturgical_event'),
            feast=json_obj.get('feast', True),
            addition=json_obj.get('addition', False),
            holy_day=json_obj.get('obligation', False),
            is_vigil=json_obj.get('is_vigil', False),
            lang=lang,
            translator=translator,
        )
        if 'urls' in json_obj:
            event.urls = [
                LiturgicalCalendarEventUrl.from_json(elem, default=event.name)
                for elem in json_obj['urls']
            ]

        if 'color' in json_obj:
            event.color = json_obj['color']

        return event

    def generate_description(self, html_formatting=False, ranking_feast=True):
        """Create a human-readable description of the event for the ICS file.

        Args:
            html_formatting: boolean
                Whether to use HTML formatting for the URLs.
            ranking_feast: booleanc
                Whether the feast is the highest-ranking feast of the day.  The highest
                ranking feast will have extra information about the liturgical color.

        Returns:
            A string with the description.

        """
        description = ''
        if self.holy_day:
            description += self.translator.format_holy_day(self.full_name())

        if description != '' and description[-1] == '.':
            description += ' '

        if self.liturgical_event and self.rank < 4:
            if self.holy_day:
                if self.lang == 'ja':
                    name = '今日'
                else:
                    name = 'Today'
            elif not ranking_feast:
                if self.lang == 'ja':
                    name = 'この祝日' if self.feast else 'この平休日'
                else:
                    name = 'This {}'.format('feast' if self.feast else 'feria')
            else:
                name = self.full_name(capitalize=True)
            description += self.translator.format_class_feria(name, self.rank, self.feast)
        elif self.liturgical_event and self.rank == 4 and ranking_feast:
            description += self.translator.format_commemoration()
        elif not self.liturgical_event:
            description += self.translator.format_no_special_liturgy(self.full_name())
        if all([
            ranking_feast,
            self.season.name in ['Lent', 'Passiontide'],
            self.liturgical_event,
            self.feast,
            self.rank and 1 < self.rank < 4,
        ]):
            if description != '' and description[-1] == '.':
                description += ' '
            description += self.translator.format_lent_commemoration(
                self.full_name(capitalize=False),
                utils.feria_name(self.date, self.translator)
            )
        if ranking_feast:
            if len(description) > 0 and description[-1] == '.':
                description += ' '
            description += self.translator.format_color(self.color)

        if self.titles:
            titles_str = self.translator.format_titles(self.titles)
            if description != '' and description[-1] != '\n':
                description += ' '
            description += titles_str + ('.' if self.lang == 'en' else '')

        if description != '':
            description += '\n\n'

        if self.urls:
            description += self.translator.format_more_info(
                self.full_name(capitalize=False)) + '\n'
            for url_obj in self.urls:
                if html_formatting:
                    description += '• ' + url_obj.to_href() + '\n'
                else:
                    description += '• ' + url_obj.url + '\n'
            description += '\n'

        description += self.translator.format_more_info(
            self.season.full_name(capitalize=False)) + '\n'
        for url_obj in self.season.urls:
            if html_formatting:
                description += '• ' + url_obj.to_href() + '\n'
            else:
                description += '• ' + url_obj.url + '\n'

        return description.rstrip()

    def is_fixed(self):
        """Determine whether the event has a fixed date.

        Returns:
            True if the event has a fixed date.

        """
        date_str = self.date.strftime('%B %-d')
        fixed_feasts_on_date = [
            elem['name'] for elem in FIXED_FEASTS_DATA.get(date_str, [])
        ]
        return (self.name in fixed_feasts_on_date)


class LiturgicalYear:
    """A liturgical year following the 1962 Roman Catholic rubrics."""

    def __init__(self, year, uid_map=None, lang='en', translator=None):
        """Instantiate a `LiturgicalYear` object.

        Note that the liturgical year starts before the year given on the first Sunday
        of Advent.  If the year given is 2000, then the liturgical year will start in
        late November 1999 and end in early December 2000.

        Args:
            year: int
                The liturgical year to calculate the calendar for.
            lang: string
            translator: A `Translator` object.

        """
        self.year = year
        self.uid_map = uid_map
        self.lang = lang
        self.translator = translator
        if self.translator is None:
            self.translator = Translator(self.lang)

        self.liturgical_year_start = liturgical_year_start(self.year)
        self.liturgical_year_end = liturgical_year_end(self.year)

        self.calendar = {}
        for date in iterate_liturgical_year(self.year):
            self.calendar[date] = []

        # First we mark fixed solemnities.
        for date in iterate_liturgical_year(self.year):
            date_str = date.strftime('%B %-d')
            if date_str in FIXED_FEASTS_DATA:
                for elem in FIXED_FEASTS_DATA[date_str]:
                    if elem.get('class') == 1:
                        event = LiturgicalCalendarEvent.from_json(
                            date, elem, lang=self.lang, translator=self.translator)
                        self.calendar[date].append(event)

        # Mark movable feasts except for vigils.
        for name, date in utils.get_movable_feast_names_and_dates(self.year):
            if isinstance(date, list):
                for elem in date:
                    event = LiturgicalCalendarEvent.from_json(
                        elem, MF_DATA[name], name, lang=self.lang, translator=self.translator)
                    self.calendar[elem].append(event)
            else:
                event = LiturgicalCalendarEvent.from_json(
                    date, MF_DATA[name], name, lang=self.lang, translator=self.translator)
                self.calendar[date].append(event)

        # Mark Sundays, starting with Advent
        for i in range(1, 5):
            if i == 3:
                continue
            date = self.liturgical_year_start + dt.timedelta(7 * (i - 1))
            ordinal = self.translator.get_ordinal(i)
            season = self.translator.translate('Advent')
            name = self.translator.templates['ordinal_sunday_full_name'].format(
                ordinal=ordinal, season=season)
            event = LiturgicalCalendarEvent(
                date, name=name, rank=1, lang=self.lang, translator=self.translator)
            self.calendar[date].append(event)

        # Time after Epiphany.
        i = 2
        date = mf.HolyFamily.date(self.year) + dt.timedelta(7)
        while date < mf.Septuagesima.date(self.year):
            ordinal = self.translator.get_ordinal(i)
            event_name = self.translator.translate('Epiphany')
            name = self.translator.templates['ordinal_sunday_after_full_name'].format(
                ordinal=ordinal, event=event_name)
            event = LiturgicalCalendarEvent(
                date, name=name, rank=2, lang=self.lang, translator=self.translator)
            self.calendar[date].append(event)
            i += 1
            date += dt.timedelta(7)

        # Lent.
        for i in range(1, 4):
            date = mf.Quinquagesima.date(self.year) + dt.timedelta(7 * i)
            ordinal = self.translator.get_ordinal(i)
            season = self.translator.translate('Lent')
            name = self.translator.templates['ordinal_sunday_full_name'].format(
                ordinal=ordinal, season=season)
            event = LiturgicalCalendarEvent(
                date, name=name, rank=1, lang=self.lang, translator=self.translator)
            self.calendar[date].append(event)

        # Eastertide.
        date = mf.CantateSunday.date(self.year) + dt.timedelta(7)
        ordinal = self.translator.get_ordinal(5)
        event_name = self.translator.translate('Easter')
        name = self.translator.templates['ordinal_sunday_after_full_name'].format(
            ordinal=ordinal, event=event_name)
        event = LiturgicalCalendarEvent(
            date, name=name, rank=1, lang=self.lang, translator=self.translator)
        self.calendar[date].append(event)

        date = mf.Ascension.date(self.year) + dt.timedelta(3)
        event_name = self.translator.translate('Ascension')
        name = self.translator.templates['ordinal_sunday_after_full_name'].format(
            ordinal='', event=event_name).replace('  ', ' ').strip()
        # In Japanese, ''後主日 works. In English ' Sunday after Ascension' works.
        event = LiturgicalCalendarEvent(
            date, name=name, rank=1, lang=self.lang, translator=self.translator)
        self.calendar[date].append(event)

        # Time after Pentecost.
        i = 2
        date = mf.TrinitySunday.date(self.year) + dt.timedelta(7)
        while date <= self.liturgical_year_end - dt.timedelta(7):
            ordinal = self.translator.get_ordinal(i)
            event_name = self.translator.translate('Pentecost')
            name = self.translator.templates['ordinal_sunday_after_full_name'].format(
                ordinal=ordinal, event=event_name)
            event = LiturgicalCalendarEvent(
                date, name=name, rank=2, lang=self.lang, translator=self.translator)
            self.calendar[date].append(event)
            i += 1
            date += dt.timedelta(7)

        event_name = self.translator.translate('Pentecost')
        name = self.translator.templates['last_sunday_full_name'].format(event=event_name)
        event = LiturgicalCalendarEvent(
            date, name=name, rank=2, lang=self.lang, translator=self.translator)
        self.calendar[date].append(event)

        # Then second class fixed feasts or lower.
        for date in iterate_liturgical_year(self.year):
            date_str = date.strftime('%B %-d')
            if date_str in FIXED_FEASTS_DATA:
                for elem in FIXED_FEASTS_DATA[date_str]:
                    if elem.get('class') != 1:
                        event = LiturgicalCalendarEvent.from_json(
                            date, elem, lang=self.lang, translator=self.translator)
                        self.calendar[date].append(event)

        if self.lang == 'ja':
            self._load_extra_ja_feasts()

        for date in iterate_liturgical_year(self.year):
            self.calendar[date] = sorted(self.calendar[date], key=_feast_sort_key)

    def _load_extra_ja_feasts(self):
        extra_files = [
            'i18n/ja/fixed_feasts_local.csv',
            'i18n/ja/fixed_feasts_missing.csv',
        ]

        for resource_path in extra_files:
            try:
                package_path = resource_path.split('/')
                filename = package_path[-1]
                directory = '.'.join(['tridentine_calendar'] + package_path[:-1])
                content = resources.read_binary(directory, filename)
                decoded_content = content.decode('shift_jis')
                reader = csv.DictReader(io.StringIO(decoded_content))
                for row in reader:
                    date_en = row.get('dates_en')
                    if not date_en:
                        continue
                    try:
                        day, month_str = date_en.split('-')
                        month = list(calendar.month_abbr).index(month_str)
                        for date in iterate_liturgical_year(self.year):
                            if date.month == month and date.day == int(day):
                                titles = []
                                if row.get('titles_1'):
                                    titles.append(row.get('titles_1'))
                                if row.get('titles_2'):
                                    titles.append(row.get('titles_2'))

                                event_name = row.get('en')
                                event_ja_name = row.get('ja')

                                rank = row.get('class')
                                rank = int(rank) if rank and rank.isdigit() else 4

                                event = LiturgicalCalendarEvent(
                                    date,
                                    name=event_name,
                                    rank=rank,
                                    titles=titles if titles else None,
                                    color=row.get('color'),
                                    lang=self.lang,
                                    translator=self.translator
                                )
                                if event_ja_name:
                                    self.translator.translations[event_name] = event_ja_name

                                self.calendar[date].append(event)
                    except (ValueError, KeyError, IndexError):
                        continue
            except (FileNotFoundError, UnicodeDecodeError, ModuleNotFoundError):
                continue

        # Load movable local feast
        resource_path = 'i18n/ja/movable_feasts_local.csv'
        try:
            package_path = resource_path.split('/')
            filename = package_path[-1]
            directory = '.'.join(['tridentine_calendar'] + package_path[:-1])
            content = resources.read_binary(directory, filename)
            decoded_content = content.decode('shift_jis')
            reader = csv.DictReader(io.StringIO(decoded_content))
            for row in reader:
                if calendar.isleap(self.year):
                    target_date = dt.date(self.year, 2, 26)
                else:
                    target_date = dt.date(self.year, 2, 25)

                if target_date in self.calendar:
                    event_name = row.get('en')
                    event_ja_name = row.get('ja')
                    titles = []
                    if row.get('titles_1'):
                        titles.append(row.get('titles_1'))
                    if row.get('titles_2'):
                        titles.append(row.get('titles_2'))

                    event = LiturgicalCalendarEvent(
                        target_date,
                        name=event_name,
                        rank=4,
                        titles=titles if titles else None,
                        color=row.get('color'),
                        lang=self.lang,
                        translator=self.translator
                    )
                    if event_ja_name:
                        self.translator.translations[event_name] = event_ja_name
                    self.calendar[target_date].append(event)
        except (FileNotFoundError, UnicodeDecodeError, ModuleNotFoundError):
            pass

    def __getitem__(self, key):
        """Return the events for a given day.

        Args:
            key: A `datetime.date` object.

        Returns:
            A list of `LiturgicalCalendarEvent` objects.

        """
        return self.calendar[key]

    def to_ical(self, html_formatting=False):
        """Write out the calendar to ICS format.

        Args:
            html_formatting: Whether to write out the URLs using `<a href>...</a>`
                formatting.  This will render nicely on many web-based calendars but not
                on desktop calendar applications.

        """
        ics_calendar = ical.Calendar()
        for date in iterate_liturgical_year(self.year):
            for i, elem in enumerate(self.calendar[date]):
                ics_name = self.translator.translate(elem.name)
                description = ''

                if i > 0 and elem.liturgical_event and not elem.addition:
                    outranking_feast = self.calendar[date][0]
                    if self.lang == 'ja':
                        ics_name = '› ' + ics_name
                    else:
                        ics_name = '› ' + ics_name

                    description += self.translator.format_outranking(
                        elem.full_name(capitalize=True),
                        outranking_feast.full_name(capitalize=False),
                        outranking_feast.is_fixed() and elem.is_fixed()
                    )

                if not elem.liturgical_event:
                    ics_name = '» ' + ics_name

                feast_description = elem.generate_description(
                    html_formatting, ranking_feast=(i == 0))
                if feast_description.startswith('More information about'):
                    description += '\n\n'
                elif description != '' and description[-1] == '.':
                    description += ' '
                description += feast_description
                description = description.strip()
                ics_event = ical.Event()
                ics_event.add('summary', ics_name)
                ics_event.add('dtstart', date)
                ics_event.add('description', description)
                ics_event.add('dtstamp', dt.datetime.now())
                if self.uid_map is not None:
                    key = (ics_name, date)
                    if key in self.uid_map:
                        uid = self.uid_map[key]
                    else:
                        uid = gen_uid()
                else:
                    uid = gen_uid()
                ics_event.add('uid', uid)
                ics_calendar.add_component(ics_event)
        return ics_calendar


def _feast_sort_key(feast):
    """Provide a key to help sort feasts.

    Args:
        feast: A `LiturgicalEvent` object.

    Returns:
        The rank of the feast if it has one and is a liturgical event, otherwise 4.

    """
    if not feast.liturgical_event or not feast.rank:
        return 4
    elif feast.addition:
        return feast.rank + .5
    elif feast.rank == 2 and feast.is_vigil:
        return feast.rank + .5
    else:
        return feast.rank


class LiturgicalCalendar:
    """A liturgical calendar following the 1962 Roman Catholic rubrics."""

    def __init__(self, years, reuse_uids_from=None, lang='en'):
        """Instantiate a `LiturgicalCalendar` object for the given year or years.

        Args:
            years: Integer or list of integers with the years to instantiate the
            `LiturgicalCalendar` for.
            lang: string

        """
        self.lang = lang
        self.translator = Translator(self.lang)

        self.uid_map = {}
        if reuse_uids_from is not None:
            with open(reuse_uids_from) as fp:
                cal = ical.Calendar.from_ical(fp.read())
                for event in cal.walk('VEVENT'):
                    key = (
                        str(event['summary']),
                        ical.vDDDTypes.from_ical(event['dtstart']),
                    )
                    self.uid_map[key] = str(event['uid'])
        self.liturgical_years = {}
        if isinstance(years, int):
            years = [years]
        for year in years:
            self.liturgical_years[year] = LiturgicalYear(
                year, self.uid_map, self.lang, self.translator)

    def __getitem__(self, key):
        """Return the events for a given day.

        Args:
            key: A `datetime.date` object.

        Returns:
            A list of `LiturgicalCalendarEvent` objects.

        """
        return self.liturgical_years[utils.liturgical_year(key)][key]

    def to_ical(self, html_formatting=False):
        """Write out the liturgical calendar to ICS format.

        Args:
            html_formatting: Whether to write out the URLs using `<a href>...</a>`
                formatting.  This will render nicely on many web-based calendars but not
                on desktop calendar applications.

        """
        ics_calendar = ical.Calendar()
        ics_calendar.add('prodid', '-//Joe Antognini//Tridentine Calendar//EN')
        ics_calendar.add('version', '2.0')

        cal_name = self.translator.translate('Tridentine calendar')
        cal_desc = self.translator.translate(
            'Liturgical calendar using the 1962 Roman Catholic rubrics.')

        ics_calendar.add('x-wr-calname', cal_name)
        ics_calendar.add(
            'x-wr-caldesc',
            cal_desc,
        )
        for liturgical_year in self.liturgical_years:
            ics_year = self.liturgical_years[liturgical_year].to_ical(html_formatting)
            for elem in ics_year.walk():
                if isinstance(elem, ical.cal.Event):
                    ics_calendar.add_component(elem)
        return ics_calendar.to_ical()

    def extend_existing_ical(self, filename, use_html_formatting):
        """Append the liturgical calendar data to an existing ICS file.

        This will read the existing ICS file to determine if HTML formatting should be
        used for the URLs.

        Args:
            filename: The ICS file to read from and write to.
            use_html_formatting: Whether to use HTML formatting.

        """
        with open(filename, 'r') as fp:
            ics_calendar = ical.Calendar.from_ical(fp.read())

        existing_years = set()
        for elem in ics_calendar.walk():
            if 'dtstart' in elem:
                existing_years.add(ical.vDDDTypes.from_ical(elem['dtstart']).year)

        for liturgical_year in self.liturgical_years:
            if liturgical_year in existing_years:
                continue

            ics_year = self.liturgical_years[liturgical_year].to_ical(
                use_html_formatting
            )
            for elem in ics_year.walk():
                if isinstance(elem, ical.cal.Event):
                    ics_calendar.add_component(elem)

        with open(filename, 'wb') as fp:
            fp.write(ics_calendar.to_ical())

    def remove_existing_year(self, filename, year):
        """Remove a liturgical year from an existing calendar."""
        with open(filename, 'r') as fp:
            ics_calendar = ical.Calendar.from_ical(fp.read())

        start_date = liturgical_year_start(year)
        end_date = liturgical_year_end(year)

        for i in range(len(ics_calendar.subcomponents))[::-1]:
            elem = ics_calendar.subcomponents[i]
            cur_date = ical.vDDDTypes.from_ical(elem['dtstart'])
            if start_date <= cur_date <= end_date:
                ics_calendar.subcomponents.pop(i)

        with open(filename, 'wb') as fp:
            fp.write(ics_calendar.to_ical())
