"""Command-line interface to `tridentine_calendar`."""

import argparse
import os

from .tridentine_calendar import LiturgicalCalendar


def get_args():
    parser = argparse.ArgumentParser(
        description='Generate a liturgical calendar using the 1962 Roman Catholic rubrics.')
    parser.add_argument(
        '--output',
        required=True,
        help=('Name of the ICS file to write the calendar out to.  If a file already exists this '
              'script will attempt to extend the calendar with the years provided.'),
    )
    parser.add_argument(
        '--years', nargs='+', metavar='YYYY', help='Liturgical years to generate the calendar for.')
    parser.add_argument(
        '--overwrite_existing',
        action='store_true',
        default=False,
        help='Whether to overwrite an existing ICS file with the same name as the given output.',
    )

    return parser.parse_args()


def main():
    args = get_args()

    liturgical_calendar = LiturgicalCalendar(args.years)
    if os.path.isfile(args.output) and not args.overwrite_existing:
        liturgical_calendar.extend_existing_ical(args.output)
    else:
        with open(args.output, 'wb') as fp:
            fp.write(liturgical_calendar.to_ical())


if __name__ == '__main__':
    main()
