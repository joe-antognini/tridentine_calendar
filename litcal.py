"""Generate a liturgical calendar using the 1962 Roman Catholic rubrics."""

import argparse
import calendar
import datetime as dt
import json
import os

import ics
from arrow import Arrow

from . import feast_dates
from .utils import ORDINALS
from .utils import description_from_url

FIXED_FEASTS_FNAME = 'fixed_feasts_ferias_et_al.json'
MOVABLE_FEASTS_FNAME = 'movable_feasts_ferias_et_al.json'
SEASONS_FNAME = 'seasons.json'


def get_args():
    """Define the command line arguments."""
    parser = argparse.ArgumentParser(description='Calculate a liturgical calendar.')
    parser.add_argument('--year', type=int, help='The year for which to calculate the calendar.')
    parser.add_argument('--file', help='Name of the ICS file to write the calendar to.')
    return parser.parse_args()


class FeastLink:
    """Contains information about a URL describing a feast, feria, or other event."""

    def __init__(self, url, description):
        """Instantiate a `FeastLink`.

        Args:
            url: A string with the URL.
            description: A string describing the URL that should be shown with the link.

        """
        self.url = url
        self.description = description

    @classmethod
    def from_json(cls, json_obj, default=None):
        """Instantiate a `FeastLink` object from a JSON object.

        Args:
            json_obj: An object resulting from parsing the JSON string describing the URL.

        Returns:
            A `FeastLink` object with the URL and description appropriately set.

        """
        if type(json_obj) is dict:
            return cls(json_obj['url'], json_obj['description'])
        elif type(json_obj) is str:
            description = description_from_url(json_obj, default)
            if description is None:
                description = default
            return cls(json_obj, description)

    def to_href(self):
        """Return the URL as an HTML HREF string."""
        return '<a href={}>{}</a>'.format(self.url, self.description)


class LiturgicalCalendar(object):
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
        self.dirname = os.path.dirname(os.path.realpath(__file__))
        
        with open(os.path.join(self.dirname, MOVABLE_FEASTS_FNAME)) as json_file:
            self.movable_feasts = json.load(json_file)

        with open(os.path.join(self.dirname, FIXED_FEASTS_FNAME)) as json_file:
            self.fixed_feasts = json.load(json_file)

        with open(os.path.join(self.dirname, SEASONS_FNAME)) as json_file:
            self.seasons = json.load(json_file)

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
            if date_str in self.fixed_feasts:
                for elem in self.fixed_feasts[date_str]:
                    if 'class' in elem and elem['class'] == 1:
                        self.calendar[date] += [elem]
            date += dt.timedelta(1)

        # Now the movable solemnities.
        function_name_pairs = (
            (feast_dates.gaudete_sunday_date, 'Gaudete Sunday'),
            (feast_dates.advent_embertide_dates, 'Advent Embertide'),
            (feast_dates.holy_name_date, 'Feast of the Holy Name'),
            (feast_dates.holy_family_date, 'Feast of the Holy Family'),
            (feast_dates.plough_monday_date, 'Plough Monday'),
            (feast_dates.septuagesima_date, 'Septuagesima'),
            (feast_dates.sexagesima_date, 'Sexagesima'),
            (feast_dates.quinquagesima_date, 'Quinquagesima'),
            (feast_dates.fat_thursday_date, 'Fat Thursday'),
            (feast_dates.shrove_monday_date, 'Shrove Monday'),
            (feast_dates.mardi_gras_date, 'Mardi Gras'),
            (feast_dates.ash_wednesday_date, 'Ash Wednesday'),
            (feast_dates.lenten_embertide_dates, 'Lenten Embertide'),
            (feast_dates.st_matthias_date, 'St. Matthias'),
            (feast_dates.st_gabriel_of_our_lady_of_sorrows_date,
                'St. Gabriel of Our Lady of Sorrows'),
            (feast_dates.laetare_sunday_date, 'Laetare Sunday'),
            (feast_dates.passion_sunday_date, 'Passion Sunday'),
            (feast_dates.seven_sorrows_date, 'The Seven Sorrows'),
            (feast_dates.palm_sunday_date, 'Palm Sunday'),
            (lambda x: feast_dates.palm_sunday_date(x) + dt.timedelta(1), 'Monday of Holy Week'),
            (lambda x: feast_dates.palm_sunday_date(x) + dt.timedelta(2), 'Tuesday of Holy Week'),
            (feast_dates.spy_wednesday_date, 'Spy Wednesday'),
            (feast_dates.maundy_thursday_date, 'Maundy Thursday'),
            (feast_dates.good_friday_date, 'Good Friday'),
            (feast_dates.holy_saturday_date, 'Holy Saturday'),
            (feast_dates.easter_date, 'Easter'),
            (lambda x: feast_dates.easter_date(x) + dt.timedelta(1), 'Easter Monday'),
            (lambda x: feast_dates.easter_date(x) + dt.timedelta(2), 'Easter Tuesday'),
            (lambda x: feast_dates.easter_date(x) + dt.timedelta(3), 'Easter Wednesday'),
            (lambda x: feast_dates.easter_date(x) + dt.timedelta(4), 'Easter Thursday'),
            (lambda x: feast_dates.easter_date(x) + dt.timedelta(5), 'Easter Friday'),
            (lambda x: feast_dates.easter_date(x) + dt.timedelta(6), 'Easter Saturday'),
            (feast_dates.quasimodo_sunday_date, 'Quasimodo Sunday'),
            (feast_dates.jubilate_sunday_date, 'Jubilate Sunday'),
            (feast_dates.misericordia_sunday_date, 'Misericordia Sunday'),
            (feast_dates.cantate_sunday_date, 'Cantate Sunday'),
            (feast_dates.major_rogation_date, 'Major Rogation'),
            (feast_dates.ascension_date, 'Ascension'),
            (feast_dates.minor_rogation_dates, 'Minor Rogation'),
            (feast_dates.pentecost_date, 'Pentecost'),
            (feast_dates.whit_embertide_dates, 'Whit Embertide'),
            (feast_dates.trinity_sunday_date, 'Trinity Sunday'),
            (feast_dates.corpus_christi_date, 'Corpus Christi'),
            (feast_dates.sacred_heart_date, 'Feast of the Sacred Heart'),
            (feast_dates.peters_pence_date, 'Peter\'s Pence'),
            (feast_dates.michaelmas_embertide_dates, 'Michaelmas Embertide'),
            (feast_dates.christ_the_king_date, 'Christ the King'),
        )

        for date_fn, name in function_name_pairs:
            date = date_fn(self.year)
            if type(date) is list:
                for elem in date:
                    self.calendar[elem] += [self.movable_feasts[name]]
                    self.calendar[elem][-1]['name'] = name
            else:
                self.calendar[date] += [self.movable_feasts[name]]
                self.calendar[date][-1]['name'] = name

        # Mark Sundays, starting with Advent
        for i in range(1, 5):
            if i == 3:
                continue
            date = self.liturgical_year_start + dt.timedelta(7 * (i - 1))
            self.calendar[date] += [{
                'name': ORDINALS[i] + ' Sunday of Advent',
                'liturgical_event': True,
            }]

        # Time after Epiphany.
        i = 2
        date = feast_dates.holy_family_date(self.year) + dt.timedelta(7)
        while date < feast_dates.septuagesima_date(self.year):
            self.calendar[date] += [{
                'name': ORDINALS[i] + ' Sunday after Epiphany',
                'liturgical_event': True,
            }]
            i += 1
            date += dt.timedelta(7)

        # Lent.
        for i in range(1, 4):
            date = feast_dates.quinquagesima_date(self.year) + dt.timedelta(7 * i)
            self.calendar[date] += [{
                'name': ORDINALS[i] + ' Sunday of Lent',
                'liturgical_event': True,
            }]

        # Eastertide.
        self.calendar[feast_dates.cantate_sunday_date(self.year) + dt.timedelta(7)] += [{
            'name': 'Sunday after Ascension',
            'liturgical_event': True,
        }]

        # Time after Pentecost.
        i = 2
        date = feast_dates.trinity_sunday_date(self.year) + dt.timedelta(7)
        while date <= self.liturgical_year_end - dt.timedelta(7):
            self.calendar[date] += [{
                'name': ORDINALS[i] + ' Sunday after Pentecost',
                'liturgical_event': True,
            }]
            i += 1
            date += dt.timedelta(7)
        self.calendar[date] += [{
            'name': 'Last Sunday after Pentecost',
            'liturgical_event': True,
        }]

        # Then second class fixed feasts or lower.
        date = self.liturgical_year_start
        while date <= self.liturgical_year_end:
            date_str = date.strftime('%B %-d')
            if date_str in self.fixed_feasts:
                for elem in self.fixed_feasts[date_str]:
                    if elem.get('class') != 1:
                        self.calendar[date] += [elem]
            date += dt.timedelta(1)

        self._add_seasons()

    def _add_seasons(self):
        date = self.liturgical_year_start
        while date <= self.liturgical_year_end:
            if date in [
                feast_dates.fat_thursday_date(self.year),
                feast_dates.shrove_monday_date(self.year),
                feast_dates.mardi_gras_date(self.year),
            ]:
                season_key = 'Shrovetide'
            elif self.liturgical_year_start <= date < dt.date(self.year - 1, 12, 25):
                season_key = 'Advent'
            elif dt.date(self.year - 1, 12, 25) <= date < dt.date(self.year, 1, 6):
                season_key = 'Christmastide'
            elif dt.date(self.year, 1, 6) <= date < feast_dates.septuagesima_date(self.year):
                season_key = 'Time after Epiphany'
            elif (
                feast_dates.septuagesima_date(self.year) <= date <
                feast_dates.ash_wednesday_date(self.year)
            ):
                season_key = 'Septuagesima'
            elif (
                feast_dates.ash_wednesday_date(self.year) <= date <
                feast_dates.passion_sunday_date(self.year)
            ):
                season_key = 'Lent'
            elif (
                feast_dates.passion_sunday_date(self.year) <= date <
                feast_dates.palm_sunday_date(self.year)
            ):
                season_key = 'Passiontide'
            elif (
                feast_dates.palm_sunday_date(self.year) <= date <
                feast_dates.maundy_thursday_date(self.year)
            ):
                season_key = 'Holy Week'
            elif (
                feast_dates.maundy_thursday_date(self.year) <= date <
                feast_dates.easter_date(self.year)
            ):
                season_key = 'Paschal Triduum'
            elif feast_dates.easter_date(self.year) <= date < feast_dates.pentecost_date(self.year):
                season_key = 'Eastertide'
            elif feast_dates.pentecost_date(self.year) <= date < dt.date(self.year, 10, 31):
                season_key = 'Time after Pentecost'
            elif dt.date(self.year, 10, 31) <= date < dt.date(self.year, 11, 3):
                season_key = 'Hallowtide'
            elif dt.date(self.year, 11, 3) <= date <= self.liturgical_year_end:
                season_key = 'Time after Pentecost'
            else:
                raise RuntimeError(
                    'date {} exceeded liturgical year range of {} to {}.'.format(
                        self.liturgical_year_start, self.liturgical_year_end))

            for i, elem in enumerate(self.calendar[date]):
                self.calendar[date][i]['season'] = self.seasons[season_key]
                self.calendar[date][i]['season'].update({'name': season_key})

            date += dt.timedelta(1)

    def __getitem__(self, key):
        return self.calendar[key]

    def _format_urls(self, event, format_html=False):
        description = ''
        if 'urls' in event:
            description += 'More information about {}:\n'.format(
                self._name_with_article(event))
            if format_html:
                description += '<ul>'
            for url_obj in event['urls']:
                if type(url_obj) is str:
                    if format_html:
                        description += '<li>' + url_obj + '</li>'
                    else:
                        description += '• ' + url_obj + '\n'
                elif type(url_obj) is dict:
                    if format_html:
                        description += '<li>' + url_obj['url'] + '</li>'
                    else:
                        description += '• ' + url_obj['url'] + '\n'
            if format_html:
                description += '</ul>'

        if 'season' in event:
            if 'urls' in event:
                description += '\n'
            if format_html:
                description += '<ul>'
            description += 'More information about {}:\n'.format(
                self._season_with_article(event['season']['name']))
            for url_obj in event['season']['urls']:
                if type(url_obj) is str:
                    if format_html:
                        description += '<li>' + url_obj + '</li>'
                    else:
                        description += '• ' + url_obj + '\n'
                elif type(url_obj) is dict:
                    description += '• ' + url_obj['url'] + '\n'
            if format_html:
                description += '</ul>'

        return description

    def _name_with_article(self, event):
        name = event['name']
        the_feast_of_prefixes = ['St.', 'SS.', 'Pope', 'Our Lady', 'Basilica']
        if any([name.startswith(elem) for elem in the_feast_of_prefixes]):
            if event.get('class') != 4:
                return 'the Feast of ' + name
            else:
                return 'the Commemoration of ' + name
        elif (name.split()[0] in ORDINALS.values() or
              name.startswith('Last Sunday') or
              name.startswith('Feast')):
            return 'the ' + name
        else:
            return name

    def _season_with_article(self, name):
        if name.startswith('Time after'):
            return 'the ' + name
        else:
            return name

    def to_ics(self):
        """Write out the calendar to ICS format."""
        ics_calendar = ics.Calendar()
        date = self.liturgical_year_start
        while date <= self.liturgical_year_end:
            for i, elem in enumerate(self.calendar[date]):
                ics_name = elem['name']
                name_with_article = self._name_with_article(elem)
                description = ''

                if elem.get('obligation'):
                    description += 'Today is a Holy Day of Obligation.\n\n'
                
                if not elem.get('liturgical_event'):
                    capitalized_name_with_article = (
                        name_with_article[0].upper() + name_with_article[1:])
                    description += '{} has no special liturgy.\n\n'.format(
                        capitalized_name_with_article)

                if i > 0 and elem.get('liturgical_event'):
                    outranking_feast = self.calendar[date][0]
                    ics_name = '« ' + ics_name + ' »'
                    if (outranking_feast['name'] in self.movable_feasts or
                        elem['name'] in self.movable_feasts or
                        'Sunday' in outranking_feast['name']):
                        description += 'This year {} is outranked by {}.\n\n'.format(
                            name_with_article, self._name_with_article(outranking_feast))
                    else:
                        description += '{} is outranked by {}.\n\n'.format(
                            name_with_article[0].upper() + name_with_article[1:],
                            self._name_with_article(outranking_feast))

                description += self._format_urls(elem, format_html=False)
                arrow_date = Arrow.fromdate(date)
                ics_event = ics.Event(name=ics_name, begin=arrow_date, description=description)
                ics_event.make_all_day()
                ics_calendar.events.add(ics_event)
            date += dt.timedelta(1)
        return ics_calendar


if __name__ == '__main__':
    args = get_args()
    litcal = LiturgicalCalendar(args.year)
    with open(args.file, 'w') as f:
        f.writelines(litcal.to_ics())
