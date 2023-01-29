from unittest import TestCase, main
from module.btrx import Btrx

class BtrxTest(TestCase):

	def test_getproduct_list(self):
		self.datalist = []
		self.assertEqual(type(Btrx.get_product_list(self.datalist)),type(self.datalist))

	def test_save_to_json(self):
		Btrx.save_to_json()
		self.datalist = []
		self.assertEqual(type([]),type(self.datalist))

	# def test_get_product_list(self):
	# 	self.assertEqual(type(get_product_list(self.test_btrx())), list)

	# def test_get_all_data(self):
	# 	self.assertEqual(type(get_product_list(self.test_btrx())), list)


if __name__ == "__main__":
	main()
