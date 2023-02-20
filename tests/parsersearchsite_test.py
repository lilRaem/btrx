from unittest import TestCase
from module.parsersearchsite import searchInSite, getProgramUrl

class ParserSearchSite(TestCase):

    datalist:list[dict[str,str|int|None]] = list()
    listdict:list[dict] = list()

    def test_searchInSite(self):
        self.assertEqual(type(searchInSite()),tuple)
        self.assertEqual(type(searchInSite()[0]),int)
        self.assertEqual(type(searchInSite()[1]),type(self.listdict))

    def test_getProgramUrl(self):
        self.assertEqual(type(getProgramUrl(price=-6400)), type(self.datalist))
        self.assertEqual(type(getProgramUrl(price=-0)), type(self.datalist))
        self.assertEqual(type(getProgramUrl(price=0)), type(self.datalist))
        self.assertEqual(type(getProgramUrl(price=3000)), type(self.datalist))
        self.assertEqual(type(getProgramUrl(price=6400)), type(self.datalist))
        self.assertEqual(type(getProgramUrl(price=9800)), type(self.datalist))
        self.assertEqual(type(getProgramUrl(price=19600)), type(self.datalist))
        self.assertEqual(type(getProgramUrl(price=29600)), type(self.datalist))