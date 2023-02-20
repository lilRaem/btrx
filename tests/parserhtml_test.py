from unittest import TestCase
from module.html_pars.parserhtml import parseSiteUrl
class ParserHtml(TestCase):
    datalist: list[dict[str,str|int|None]] = list()
    def test_parseSiteUrl(self):
        self.assertEqual(type(parseSiteUrl(price=-6400)),type(self.datalist))
        self.assertEqual(type(parseSiteUrl(price=-0)),type(self.datalist))
        self.assertEqual(type(parseSiteUrl(price=0)),type(self.datalist))
        self.assertEqual(type(parseSiteUrl(price=39)),type(self.datalist))
        self.assertEqual(type(parseSiteUrl(price=6400)),type(self.datalist))
        self.assertEqual(type(parseSiteUrl(price=99000)),type(self.datalist))