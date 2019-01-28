import argparse
import os
import tempfile
import unittest

from ..cli import get_args
from ..cli import _main


class TestGetArgs(unittest.TestCase):

    def test_get_args_one_year(self):
        args = get_args(['--output', 'foo', '2000'])
        self.assertEqual(args.output, 'foo')
        self.assertEqual(args.years, [2000])
        self.assertFalse(args.overwrite_existing)

    def test_get_args_multiple_years(self):
        tmp_file = tempfile.NamedTemporaryFile()
        args = get_args(['--output', 'foo', '2000', '2010'])
        self.assertEqual(args.output, 'foo')
        self.assertEqual(args.years, [2000, 2010])
        self.assertFalse(args.overwrite_existing)


class TestMain(unittest.TestCase):

    def test_main_new_calendar(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            args = argparse.Namespace(
                output=os.path.join(tmp_dir, 'foo'),
                years=[2018, 2019],
                overwrite_existing=False,
            )
            _main(args)

    def test_main_existing_calendar(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            args = argparse.Namespace(
                output=os.path.join(tmp_dir, 'foo'),
                years=[2018],
                overwrite_existing=False,
            )
            _main(args)

            args = argparse.Namespace(
                output=os.path.join(tmp_dir, 'foo'),
                years=[2019],
                overwrite_existing=False,
            )
            _main(args)
