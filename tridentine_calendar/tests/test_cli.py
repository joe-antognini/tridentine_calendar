import argparse
import os
import tempfile
import unittest
from unittest.mock import patch

from ..cli import _main
from ..cli import parse_args


class TestParseArgs(unittest.TestCase):

    def test_parse_args_one_year(self):
        args = parse_args(['--output', 'foo', '2000'])
        self.assertEqual(args.output, 'foo')
        self.assertEqual(args.years, [2000])
        self.assertFalse(args.overwrite_existing)

    def test_parse_args_multiple_years(self):
        args = parse_args(['--output', 'foo', '2000', '2010'])
        self.assertEqual(args.output, 'foo')
        self.assertEqual(args.years, [2000, 2010])
        self.assertFalse(args.overwrite_existing)

    def test_parse_args_new_years_message(self):
        args = parse_args(['--output', 'foo', '--new-years-message', '2000'])
        self.assertEqual(args.output, 'foo')
        self.assertEqual(args.years, [2000])
        self.assertTrue(args.new_years_message)

    def test_parse_args_help(self):
        with self.assertRaises(SystemExit):
            parse_args(['-h'])


class TestMain(unittest.TestCase):

    def test_main_new_calendar(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            args = argparse.Namespace(
                output=os.path.join(tmp_dir, 'foo'),
                years=[2018, 2019],
                overwrite_existing=False,
                use_html_formatting=False,
                reuse_uids_from=None,
            )
            _main(args)

    @patch('tridentine_calendar.cli.get_message_from_editor')
    def test_main_new_years_message(self, mock_get_message):
        mock_get_message.return_value = 'Custom message'
        with tempfile.TemporaryDirectory() as tmp_dir:
            args = argparse.Namespace(
                output=os.path.join(tmp_dir, 'foo'),
                years=[2018],
                overwrite_existing=False,
                use_html_formatting=False,
                reuse_uids_from=None,
                new_years_message=True,
            )
            _main(args)
            mock_get_message.assert_called_once()

    def test_main_existing_calendar(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            args = argparse.Namespace(
                output=os.path.join(tmp_dir, 'foo'),
                years=[2018],
                overwrite_existing=False,
                use_html_formatting=True,
                reuse_uids_from=None,
            )
            _main(args)

            args = argparse.Namespace(
                output=os.path.join(tmp_dir, 'foo'),
                years=[2019],
                overwrite_existing=False,
                use_html_formatting=True,
                reuse_uids_from=None,
            )
            _main(args)
