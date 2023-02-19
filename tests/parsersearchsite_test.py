from unittest import TestCase
from module.parsersearchsite import searchInSite, getProgramUrl

class ParserSearchSite(TestCase):

    def test_searchInSite(self):
        self.assertEqual(type(searchInSite()),tuple)
        self.assertEqual(type(searchInSite()[0]),int)
        self.assertEqual(type(searchInSite()[1]),list)

    def test_getProgramUrl(self):
        self.assertEqual(type(getProgramUrl(price=-6400)), list)
        self.assertEqual(type(getProgramUrl(price=-0)), list)
        self.assertEqual(type(getProgramUrl(price=0)), list)
        self.assertEqual(type(getProgramUrl(price=3000)), list)
        self.assertEqual(type(getProgramUrl(price=6400)), list)
        self.assertEqual(type(getProgramUrl(price=9800)), list)
        self.assertEqual(type(getProgramUrl(price=19600)), list)
        self.assertEqual(type(getProgramUrl(price=29600)), list)