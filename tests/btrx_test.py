from unittest import TestCase, main
import btrx
from main import *


class BtrxTest(TestCase):

	def test_webhook(self):
		self.test_webhook_var = 'https://b24-vejk6x.bitrix24.ru/rest/1/di28gta836z3xn50/'
		self.assertEqual(type(btrx.webhook), type(self.test_webhook_var))
		return self.test_webhook_var

	def test_btrx(self):
		test_btrx_var = btrx.Bitrix(self.test_webhook())
		try:
			self.assertEqual(type(btrx.btrx), type(test_btrx_var))
		except:
			raise TypeError(
				f"Type of btrx = <class 'fastbtrx24.bitrtix.Bitrix'> but now:\nbtrx: {type(btrx.btrx)} != test_btrx: {type(test_btrx_var)}"
			)
		return test_btrx_var

	def test_datalist(self):
		self.datalist = [{"key": 'data'}]
		self.assertEqual(type(datalist), type(self.datalist))

	def test_filename(self):
		self.filename = 'file.json'
		self.assertEqual(type(filename), type(self.filename))
		if type(self.filename) != str:
			raise TypeError('type of filename = str')

	def test_path(self):
		self.path = 'tests\\btrx_test'
		self.assertEqual(type(path), type(self.path))
		if type(self.path) != str:
			raise TypeError('type of path = str')

	def test_save_to_json(self):
		self.datalist = [{"key": 'data'}]
		self.filename = 'file.json'
		self.path = f'{os.getcwd()}\\tests\\btrx_test'


		self.assertEqual(type(datalist), type(self.datalist))
		self.assertEqual(type(filename), type(self.filename))
		self.assertEqual(type(path), type(self.path))


	def test_load_from_jsonFile(self):
		self.filename = 'file.json'
		self.path = f'{os.getcwd()}\\tests\\btrx_test'
		self.data_from_file = []
		data_from_file = []
		self.assertEqual(type(data_from_file), list)
		self.assertEqual(type(self.data_from_file), list)
		os.chdir(self.path)
		self.assertEqual(type(load_from_jsonFile(self.filename, self.path)),list)
		self.assertEqual(load_from_jsonFile(self.filename, self.path),list)
		with self.assertRaises(Exception) as e:
			load_from_jsonFile(self.filename, 2)
		self.assertEqual('тип path должен быть str', e.exception.args[0])
		with self.assertRaises(Exception) as e:
			load_from_jsonFile(2, self.path)
		self.assertEqual('тип filename должен быть str', e.exception.args[0])

	def test_get_product_list(self):
		self.assertEqual(type(get_product_list(self.test_btrx())), list)

	def test_get_all_data(self):
		self.assertEqual(type(get_product_list(self.test_btrx())), list)


if __name__ == "__main__":
	main()
