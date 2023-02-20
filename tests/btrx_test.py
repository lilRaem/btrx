import os
from unittest import TestCase, main
from module.btrx import Btrx


class BtrxTest(TestCase):
	path = os.getcwd()
	filename = "file.json"
	datalist: list[dict[str,str|int|None]] = list()

	def test_save_to_json(self):
		self.assertEqual(type(Btrx.save_to_json(self,self.datalist,self.filename,f"{os.getcwd()}\\tests\\btrx_save_test")),type(self.datalist))

	def test_load_from_jsonFile(self):
		self.assertEqual(type(Btrx.load_from_jsonFile(self,self.filename,f"tests\\btrx_load_test")),type(self.datalist))

	def test_getproduct_list(self):
		self.assertEqual(type(Btrx.get_product_list(self)),type(self.datalist))

	def test_get_users_with_innerPhone(self):
		self.assertEqual(type(Btrx.get_users_with_innerPhone(Btrx())),type(self.datalist))

	def test_get_all_data(self):
		self.assertEqual(type(Btrx.get_product_list(self.datalist)), type(self.datalist))

	def test_check_product(self):
		self.assertEqual(type(Btrx.check_product(self,"Ультразвуковая диагностика", -6400,Btrx.get_all_data(self, Btrx.get_product_list(Btrx())))), type(self.datalist))
		self.assertEqual(type(Btrx.check_product(self,"Ультразвуковая диагностика", -0,Btrx.get_all_data(self, Btrx.get_product_list(Btrx())))), type(self.datalist))
		self.assertEqual(type(Btrx.check_product(self,"Ультразвуковая диагностика", 0,Btrx.get_all_data(self, Btrx.get_product_list(Btrx())))), type(self.datalist))
		self.assertEqual(type(Btrx.check_product(self,"Ультразвуковая диагностика", 39,Btrx.get_all_data(self, Btrx.get_product_list(Btrx())))), type(self.datalist))
		self.assertEqual(type(Btrx.check_product(self,"Ультразвуковая диагностика", 6400,Btrx.get_all_data(self, Btrx.get_product_list(Btrx())))), type(self.datalist))
		self.assertEqual(type(Btrx.check_product(self,"Ультразвуковая диагностика", 99000,Btrx.get_all_data(self, Btrx.get_product_list(Btrx())))), type(self.datalist))
		self.assertEqual(type(Btrx.check_product(self,"Онкология", 0,Btrx.get_all_data(self, Btrx.get_product_list(Btrx())))), type(self.datalist))
		self.assertEqual(type(Btrx.check_product(self,"Онкология", 39,Btrx.get_all_data(self, Btrx.get_product_list(Btrx())))), type(self.datalist))
		self.assertEqual(type(Btrx.check_product(self,"Онкология", 6400,Btrx.get_all_data(self, Btrx.get_product_list(Btrx())))), type(self.datalist))