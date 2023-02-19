from unittest import TestCase
from module.html_pars.parserhtml import parseSiteUrl
class ParserHtml(TestCase):

    def test_parseSiteUrl(self):
        self.assertEqual(type(parseSiteUrl(price=-6400)),list)
        self.assertEqual(type(parseSiteUrl(price=-0)),list)
        self.assertEqual(type(parseSiteUrl(price=0)),list)
        self.assertEqual(type(parseSiteUrl(price=39)),list)
        self.assertEqual(type(parseSiteUrl(price=6400)),list)
        self.assertEqual(type(parseSiteUrl(price=99000)),list)