import argparse
import os
import tempfile
import unittest

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
