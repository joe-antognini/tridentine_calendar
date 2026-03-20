"""Command-line interface to `tridentine_calendar`."""

import argparse
import os
import subprocess
import sys
import tempfile

from .tridentine_calendar import LiturgicalCalendar


def parse_args(args):
    """Set and parse the command line arguments.

    Returns:
        args: An `argparse.Namespace` object with the parsed arguments.

    """
    parser = argparse.ArgumentParser(
        description=(
            'Generate a liturgical calendar using the 1962 Roman Catholic rubrics.'
        )
    )
    parser.add_argument(
        '--use_html_formatting',
        action='store_true',
        default=False,
        help='Whether to format the URLs using <a href>s.',
    )
    parser.add_argument(
        '--output',
        required=True,
        help=(
            'Name of the ICS file to write the calendar out to.  If a file already '
            'exists this script will attempt to extend the calendar with the years '
            'provided.'
        ),
    )
    parser.add_argument(
        'years',
        nargs='+',
        type=int,
        metavar='YYYY',
        help='Liturgical years to generate the calendar for.',
    )
    parser.add_argument(
        '--overwrite_existing',
        action='store_true',
        default=False,
        help=(
            'Whether to overwrite an existing ICS file with the same name as the given '
            'output.'
        ),
    )
    parser.add_argument(
        '--remove_year',
        type=int,
        help='Remove a year from an existing calendar.',
    )
    parser.add_argument(
        '--reuse-uids-from',
        help=(
            'An optional path to an existing ICS file to reuse the UIDs from, if they '
            'can be found.'
        ),
    )
    parser.add_argument(
        '--new-years-message',
        action='store_true',
        default=False,
        help='Whether to add a custom message to the first day of the liturgical year.',
    )

    return parser.parse_args(args)


def get_message_from_editor():
    """Open the user's editor to get a message.

    Returns:
        str: The message written by the user.

    """
    editor = os.environ.get('EDITOR', 'vi')
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tf:
        tf_path = tf.name

    try:
        subprocess.run([editor, tf_path], check=True)
        with open(tf_path, 'r') as f:
            message = f.read().strip()
    finally:
        os.remove(tf_path)

    return message


def _main(args):
    new_years_message = None
    if getattr(args, 'new_years_message', False):
        new_years_message = get_message_from_editor()

    liturgical_calendar = LiturgicalCalendar(
        args.years, args.reuse_uids_from, new_years_message
    )
    if os.path.isfile(args.output) and not args.overwrite_existing:
        liturgical_calendar.extend_existing_ical(args.output, args.use_html_formatting)
        if 'remove_year' in args and args.remove_year is not None:
            liturgical_calendar.remove_existing_year(
                args.output, args.remove_year, args.use_html_formatting
            )
    else:
        with open(args.output, 'wb') as fp:
            fp.write(liturgical_calendar.to_ical(args.use_html_formatting))


def main():
    """Run the command line interface for `tridentine_calendar`."""
    args = parse_args(sys.argv[1:])
    _main(args)
