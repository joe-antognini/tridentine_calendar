import unittest

from ..utils import description_from_url


class TestDescriptionFromUrl(unittest.TestCase):

    def test_description_from_url(self):
        url = 'https://en.wikipedia.org/Saturnin'
        output = description_from_url(url)
        self.assertEqual(output, 'Saturnin (Wikipedia)')

        url = 'http://www.newadvent.org/cathen/01471a.htm'
        output = description_from_url(url, 'Saturninus')
        self.assertEqual(output, 'Saturninus (New Advent)')
