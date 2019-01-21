import unittest

from ..utils import add_domain_to_url_description


class TestAddDomainToUrlDescription(unittest.TestCase):

    def test_add_domain_to_url_description(self):
        url = 'https://en.wikipedia.org/Saturnin'
        output = add_domain_to_url_description(url, 'Saturnin')
        self.assertEqual(output, 'Saturnin (Wikipedia)')

        url = 'http://www.newadvent.org/cathen/01471a.htm'
        output = add_domain_to_url_description(url, 'Saturninus')
        self.assertEqual(output, 'Saturninus (New Advent)')
