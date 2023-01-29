from unittest import TestCase
from module.html_pars.parserhtml import parseSiteUrl
class ParserHtml(TestCase):

    def test_parseSiteUrl(self):
        self.assertEqual(type(parseSiteUrl()),list)