from datetime import date
import json, os
from typing import Optional
from pydantic import BaseModel, StrictStr
from fast_bitrix24 import Bitrix
from colorama import Fore, Back, Style
try:
	from config import FinalData
except:
	from module.config import FinalData


# webhook = 'https://b24-vejk6x.bitrix24.ru/rest/1/di28gta836z3xn50/'
# btrx = Bitrix(webhook=webhook,respect_velocity_policy=False)
class Btrx(Bitrix):
	def __init__(self):
		self.webhook = 'https://b24-vejk6x.bitrix24.ru/rest/1/di28gta836z3xn50/'
		super().__init__(webhook=self.webhook,respect_velocity_policy=False)
	COUNT_PROGRAMS = 0

	def save_to_json(self, datalist:list, filename: str, path: str) -> list:
		data = []
		if datalist == None or type(datalist) != list:
			raise TypeError(f'тип datalist({type(datalist)}) должен быть {list}')
		elif filename == None or type(filename) != str:
			raise TypeError(f'тип filename({type(filename)}) должен быть str')
		elif path == None or type(path) != str:
			raise TypeError(f'тип path({type(path)}) должен быть str')
		try:
			if (os.path.exists(path)):
				with open(os.path.join(path, f"{filename}"), 'w', encoding='utf-8') as file:
					# sleep(1)
					try:
						data = json.dumps(datalist, ensure_ascii=False, indent=4)
						file.write(data)
						return list(data)
					except Exception as e:
						print(Fore.RED + f'Error save to json {e}')
						raise TypeError(f'Error save to json {e}')
			return list(data)
		except Exception as e:
			raise TypeError(f'{e}')

	def load_from_jsonFile(self,filename:str = "file.json", path: str = str()) -> list:
		# sleep(2)
		data_from_file = []
		if type(filename) != str:
			raise TypeError('тип filename должен быть str')
		elif type(path) != str:
			raise TypeError('тип path должен быть str')
		try:
			if (os.path.exists(path)):
				print(f"current path: {path}")
				with open(os.getcwd()+"\\"+path+"\\"+filename, 'r', encoding='utf-8') as file:
					data_from_file = json.load(file)
					print(Style.RESET_ALL + Fore.BLACK + f'\nLoad from {filename}' + Style.RESET_ALL)
				return list(data_from_file)
			else:
				os.mkdir(path)
		except Exception as e:
			raise TypeError(Fore.RED + f'Error in load_from_jsonFile {e}'+ Fore.RESET)

	def get_product_list(self) -> list:
		"""Load	from btrx24	all	data (id, name,	price, hours)\n
			hours data in field: ['PROPERTY_213'] => ['value']"""
		try:
			products = []
			products = self.get_all('crm.product.list',
				params={'select': ['ID', 'NAME', 'PRICE', 'PROPERTY_213']})
			return list(products)
		except Exception as e:
			print(Fore.RED + f'\nGet products error: {e}\n')
		finally:
			return products

	def get_users_with_innerPhone(self) -> list:
		users = []
		try:
			users = self.get_all('user.get',params={
				'select': ['*']
			})
			return list(users)
		except Exception as e:
			print(e)
			raise TypeError('get_users_with_innerPhone error')

	def set_product_price(self,id=str(),price=0):
		try:
			params = {"ID": id, "fields":{
				'PRICE': price
			}}
			res = self.call('crm.product.update',params)
			print(f'Price {price} for {id} is SET {res}'+Style.RESET_ALL+"\n")
		except Exception as e:
			print(e)

	def get_all_data(self,data: list) -> list:

		"""
		Get all data (id, name, price, hours) with hours
		"""
		if (data == None or type(data) != list):
			raise TypeError(f'expect type of data = list.\nNow: {type(data)}')
		datalist=list()
		final_data = FinalData()
		wh = 0
		woh = 0
		try:
			for item in data:
				id = item['ID']
				id = check_null(id,item['ID'])
				name = item['NAME']
				name = check_null(name,item['NAME'])
				price = item['PRICE']
				hour = item['PROPERTY_213']

				if price == '' or price == None:
					price = None
				else:
					price = item['PRICE']
					price = price.replace('.00', '')

				if hour == '' or hour == None:
					hour = None
				else:
					hour = hour.get('value')

				final_data.id = id
				final_data.name = name
				final_data.price = price
				final_data.hour = hour
				datalist.append(final_data.json(encoder='utf-8',ensure_ascii=False))
				if (hour != None):
					wh = wh + 1
				else:
					woh = woh + 1
			print(Fore.LIGHTCYAN_EX +  f'\n####\n{Back.CYAN}Find{Style.RESET_ALL} {wh} {Back.CYAN}items{Style.RESET_ALL} {Back.GREEN+Fore.BLACK}with hours' + Style.RESET_ALL)
			print(Fore.BLUE + f'\nFind {woh} items without hours')
			print(Fore.CYAN + f'\nFind {wh+woh} items all\n####\n')
			return list(datalist)
		except Exception as e:
			print(Fore.RED + f'get_all_data error {e}')
			raise TypeError(f'Ошибка в get_all_data. type of data({type(data)}), datalist({type(datalist)}), expect data(list) and datalist(list)' )

	def words_search(self, words_list=list, name=str, price=str, datalist=list) -> list:
		words_data = []
		find_name_price_count = 0
		find_word_count = 0
		for word in words_list:
			char_count = 0

			for char in word:
				char_count = char_count + 1

				if char_count != 1:
					find_all_count = 0

					for k in datalist:
						k_name = k['name']
						k_price = k['price']
						k_name = k_name.lower()

						if word != None and word != '' and k_name != None and k_price != None:

							if word in k_name and price in k_price:

								try:
									# print('find_all_count (word in k_name and price)',find_all_count , datalist[find_all_count])
									# print(Back.GREEN + Fore.BLACK + Style.DIM +
									# 	f'=====\nСовпадение части слова "{word}" и цены "{price}" в программе: {datalist[find_all_count]}\n====='
									# 	+ Back.RESET + Fore.RESET)
									words_data.append({word: datalist[find_all_count]})
									print(Back.RESET + Fore.RESET + Style.DIM + Fore.BLACK + Back.LIGHTGREEN_EX +
										f"^По слову '{word}' и цене {k_price}(из найденной программы) Сохранено в tmpfile.json^"
											+Style.RESET_ALL)
									with open(f'{os.getcwd()}\\data\\json\\btrx_data\\tmpfile.json',
										'w',
										encoding='utf-8') as file:
										data_list = json.dumps(words_data, ensure_ascii=False, indent=4)
										file.write(data_list)
									find_name_price_count = find_name_price_count + 1
									# return list(words_data)
								except Exception as e:
									print(Fore.RED + Style.DIM + f'ошибка check_product-> if word in k_*: {e}')
									return 'ошибка'

							else:
								if word in k_name:
									try:
										find_word_count = find_word_count + 1
									except Exception as e:
										print(Fore.RED + f'ошибка {e}')
										return 'ошибка'
						find_all_count = find_all_count + 1
			print('find_allcount: ',find_all_count)
			print(Style.RESET_ALL + f'\nВсего по словам из названия которые есть в др. программах {find_word_count+find_name_price_count},по слову {find_word_count} , по слову и цене {find_name_price_count}.\n')
		return data_list

	def find_list_compare_words(self,searched_wrods):
		list_one = searched_wrods
		list_two = searched_wrods
		print(enumerate(list_one))
		for_counter = 0
		for k,v in enumerate(searched_wrods):
			print("list_one=",k)
		print(f'find wrods compare: {searched_wrods}')

	def check_product(self, name: str, price: str, datalist: list):
		final_data = FinalData()
		try:
			if name != None and name != '':
				print(Back.YELLOW + Fore.BLACK + 'Start check')

				name = name.strip()
				# if ' ' in name:
				# 	name_space = name.count(' ')
				# 	if name_space == 1 or name_space >= 2:
				# 		list_name = name.split(' ')
						# searched_words = words_search(list_name, name, price, datalist)
						# find_list_compare_words(searched_words)
				count_name_price = 0
				count_name = 0
				found_data_by_name_price = []
				found_data_by_name = []
				try:
					for i,v in enumerate(datalist):

						data_list = json.loads(v)
						final_data.name = data_list['name']
						final_data.price = data_list['price']
						k_name = final_data.name.lower()
						if name.lower() in k_name and price == final_data.price and price != '':
							count_name_price = count_name_price + 1
						else:
							if name.lower() in k_name:
								count_name = count_name + 1
					print(f'Найдено:\nИмя/цена: {count_name_price} шт\nИмя: {count_name} шт'+ Style.RESET_ALL)
				except Exception as e:
					print(e)
				try:
					for i,v in enumerate(datalist):
						data_list = json.loads(v)
						final_data.name = data_list['name']
						final_data.price = data_list['price']
						k_name = final_data.name.lower()
						if name.lower() in k_name and price == final_data.price and price != '':
							try:
								if count_name_price == 1 and price != '':
									if name.lower() == k_name:
										print("\n"+Back.LIGHTCYAN_EX + Fore.BLACK + Style.DIM +
											f'=====\nПо названию {name} и цене {price}:\n{datalist[i]}\n====='+Style.RESET_ALL+"\n")
										found_data_by_name_price.append(json.loads(datalist[i]))
									else:
										print("\n"+Back.CYAN + Fore.BLACK + Style.DIM +
											f'=====\nПо содержанию названия {name} и цене {price}:\n{datalist[i]}\n====='+Style.RESET_ALL+"\n")
										found_data_by_name_price.append(json.loads(datalist[i]))
								else:
									print(Back.LIGHTMAGENTA_EX + Fore.BLACK + Style.DIM +
										f'\n=====\nПо названию {name} цена по поиску {price}: {datalist[i]}\n====='+Style.RESET_ALL+"\n")
									found_data_by_name_price.append(json.loads(datalist[i]))
							except:
								print(Fore.RED + 'Ошибка при поиске названия и цены')

						else:
							if name.lower() in k_name:
								try:
									# print(Style.RESET_ALL + Fore.LIGHTBLACK_EX + f'[{Back.GREEN + v["id"] + Back.RESET}] "{k_name}"\n')

									if count_name == 1:
										print("\n"+Style.RESET_ALL + Fore.BLACK + f'[{Back.LIGHTGREEN_EX + Fore.BLACK  + v["id"] + Back.RESET}]' + f' {Fore.RESET}"{k_name}"')
										found_data_by_name.append(json.loads(datalist[i]))
									else:
										v_j=json.loads(v)
										print(Style.RESET_ALL + Fore.BLACK + f'[ {Back.GREEN + Fore.BLACK  + v_j["id"] + Back.RESET} ]' + f' {Fore.LIGHTBLACK_EX}"{v_j["name"]}|{v_j["hour"]}|{v_j["price"]}"')
										found_data_by_name.append(json.loads(datalist[i]))
								except Exception as e:
									print(Fore.RED + 'Ошибка при поиске названия\n'+Fore.RED+f'{e}')

				except Exception as e:
					print(e)
				print(Style.RESET_ALL + f'Всего программ: {i}')

				if found_data_by_name_price != []:
					count_fdbnp = 0
					for data in found_data_by_name_price:
						count_fdbnp = count_fdbnp + 1
					if count_fdbnp == 1:
						print(Fore.YELLOW+f'{found_data_by_name_price}'+Fore.RESET)
						return found_data_by_name_price
					else:
						print(f"Найдено {count_fdbnp} программ с одинаковым названием и ценой\
						\n(или содержания слова в названии и цена)\n")
						similar_list = []
						for i,dta in enumerate(found_data_by_name_price):
							data = dict(dta)
							if name.lower() == data['name'].lower() and price in data['price']:
								print("\n"+Fore.GREEN+f'{i+1} {data}'+Fore.RESET+"\n")
								similar_list.append(data)
							else:
								print(Fore.YELLOW+f'{i+1} {data}'+Fore.RESET+"\n")
						if similar_list != []:
							return similar_list
						else:
							return found_data_by_name_price
				elif found_data_by_name != []:
					count_dbn = 0
					for data in found_data_by_name:
						count_dbn = count_dbn + 1
					if count_dbn == 1:
						return found_data_by_name
					else:
						list_by_name = []
						print(f"Найдено {count_dbn} программ с одинаковым названием\
						\n(или содержания слова в названии)")

						count_by_name = 0
						for data_ in found_data_by_name:
							count_by_name = count_by_name + 1
						if count_by_name != 0:
							for data in found_data_by_name:
								final_data = FinalData()
								json_data=data
								print(Fore.LIGHTYELLOW_EX+f'\n{json_data}'+Fore.RESET)
								final_data.id = json_data['id']
								final_data.spec = json_data['spec']
								final_data.name = json_data['name']
								final_data.price = json_data['price']
								final_data.hour = json_data['hour']
								final_data.linkNmo = json_data['linkNmo']
								final_data.url = json_data['url']
								list_by_name.append(final_data.dict())
							return list_by_name
				else:
					print('Not found')
					return None
			else:
				print(Fore.RED+f'Проверьте правильность введенных данных. Скорее всего имя не ЗАДАНО (это текст исключения на пустоту переменной "name": {type(name)}={name})')
		except Exception as e:
			print(Fore.RED+f'{e}')

	def makefileWdateName(self) -> tuple:
		"""
		[0] = str(fileNameWithPath)
		[1] = str(filename)

		Returns:
			tuple: [fileNameWithPath,filename]
		"""
		today = date.today()
		cur_date = today.strftime("%d.%m.%Y")
		filename = f'{cur_date}_file.json'
		path = os.getcwd() + "\\data\\json\\btrx_data"
		filenameWcurDate = f"{path}\\{filename}"
		return str(filenameWcurDate), str(filename), path

def check_null(variable, iter):
	if variable != '' or variable != None:
		variable = iter
	else:
		variable = None
	return variable

if __name__ == '__main__':
		btrx = Btrx()
		data = []
		print(btrx.check_product('Онкология','39', btrx.get_all_data(btrx.get_product_list())))
