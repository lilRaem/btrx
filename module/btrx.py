import json, os
from time import sleep
from turtle import back
from fast_bitrix24 import Bitrix
from colorama import Fore, Back, Style

webhook = 'https://b24-vejk6x.bitrix24.ru/rest/1/di28gta836z3xn50/'
btrx = Bitrix(webhook=webhook)

COUNT_PROGRAMS = 0

def save_to_json(datalist=list(), filename='file', path=str()) -> list:
	data = []
	if datalist == None or type(datalist) != list:
		raise TypeError(f'тип datalist({type(datalist)}) должен быть list')
	elif filename == None or type(filename) != str:
		raise TypeError(f'тип filename({type(filename)}) должен быть str')
	elif path == None or type(path) != str:
		raise TypeError(f'тип path({type(path)}) должен быть str')
	try:
		if (os.path.exists(path)):
			with open(os.path.join(path, f"{filename}"), 'w', encoding='utf-8') as file:
				sleep(1)
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


def load_from_jsonFile(filename='*.json', path=str()) -> list:
	sleep(2)
	data_from_file = []
	if type(filename) != str:
		raise TypeError('тип filename должен быть str')
	elif type(path) != str:
		raise TypeError('тип path должен быть str')
	try:
		if (os.path.exists(path)):
			with open(filename, 'r', encoding='utf-8') as file:
				data_from_file = json.load(file)
				print(Style.RESET_ALL + Fore.BLACK + f'\nLoad from {filename}' + Style.RESET_ALL)
			return list(data_from_file)
		else:
			os.mkdir(path)
		return list(data_from_file)
	except Exception as e:
		print(Fore.RED + f'Error in load_from_jsonFile {e}')
		raise TypeError(f'Error in load_from_jsonFile')


def get_product_list(btrx=Bitrix(webhook)) -> list:
	"""Load	from btrx24	all	data (id, name,	price, hours)\n
		hours data in field: ['PROPERTY_213'] => ['value']"""
	products = []
	try:
		products = btrx.get_all('crm.product.list',
			params={'select': ['ID', 'NAME', 'PRICE', 'PROPERTY_213']})
		return list(products)
	except Exception as e:
		print(Fore.RED + f'\nGet products error: {e}\n')
	return list(products)


def get_product_id(data):
	for item in data:
		yield item['ID']


def get_product_name(data):
	for item in data:
		yield item['NAME']


def get_product_price(data):
	for item in data:
		yield item['PRICE']


def get_product_hour(data):
	for item in data:
		i = item['PROPERTY_213']
		yield i['value']


def get_all_data(data, datalist=list()):
	"""Get all data	(id, name, price, hours) with hours\n
		in description and exclude ['PROPERTY_213']	= None"""
	if (data == None or type(data) != list):
		raise TypeError(f'expect type of data = list')
	if (datalist == None or type(datalist) != list):
		raise TypeError(f'expect type of datalist = list')

	datadict = dict()
	wh = 0
	woh = 0
	try:
		for item in data:
			hours = item['PROPERTY_213']
			if (hours != None):
				hour = hours.get('value')
				id = item['ID']
				name = item['NAME']
				price = item['PRICE']
				if (price != None):
					price = price.replace('.00', '')
				datadict = {
					'id': id,
					'name': name,
					'price': price,
					'hour': hour,
				}
				datalist.append(datadict)
				wh = wh + 1
			else:
				id = item['ID']
				name = item['NAME']
				price = item['PRICE']
				if (price != None):
					price = price.replace('.00', '')
				datadict = {
					'id': id,
					'name': name,
					'price': price,
				}
				datalist.append(datadict)
				woh = woh + 1

		print(Fore.LIGHTCYAN_EX +  f'\n####\n{Back.CYAN}Find{Style.RESET_ALL} {wh} {Back.CYAN}items{Style.RESET_ALL} {Back.GREEN+Fore.BLACK}with hours' + Style.RESET_ALL)
		print(Fore.BLUE + f'\nFind {woh} items without hours')
		print(Fore.CYAN + f'\nFind {wh+woh} items all\n####\n')
		COUNT_PROGRAMS = wh+woh
		return list(datalist)
	except Exception as e:
		print(Fore.RED + f'get_all_data error {e}')
		raise TypeError(f'Ошибка в get_all_data. type of data({type(data)}), datalist({type(datalist)}), expect data(list) and datalist(list)' )


def words_search(words_list=list, name=str, price=str, datalist=list) -> list:
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
								# print(Back.RESET + Fore.RESET + Style.DIM + Fore.BLACK + Back.LIGHTGREEN_EX +
								# 	f"^По слову '{word}' и цене {k_price}(из найденной программы) Сохранено в tmpfile.json^"
								# 		+Style.RESET_ALL)
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
									# print('find_all_count (word in k_name)',find_all_count)
									# print(Style.RESET_ALL+f'Current word: {word} and program in search: {datalist[name_price]}')
									print(Fore.LIGHTYELLOW_EX + f'\nпо слову {word}:',
										datalist[find_all_count], '\n' + Fore.RESET + Style.RESET_ALL)
									find_word_count = find_word_count + 1

								except Exception as e:
									print(Fore.RED + f'ошибка {e}')
									return 'ошибка'
					find_all_count = find_all_count + 1
		print('find_allcount: ',find_all_count)
		print(Style.RESET_ALL + f'\nВсего по словам из названия которые есть в др. программах {find_word_count+find_name_price_count},по слову {find_word_count} , по слову и цене {find_name_price_count}.\n')
	return data_list
def find_list_compare_words(searched_wrods):
	list_one = searched_wrods
	list_two = searched_wrods
	print(enumerate(list_one))
	for_counter = 0
	for k,v in enumerate(searched_wrods):
		print("list_one=",k)
	print(f'find wrods compare: {searched_wrods}')

def check_product(name=str, price=str, datalist=list) -> int:
	global COUNT_PROGRAMS
	try:
		if name != None and name != '':
			print(Back.YELLOW + Fore.BLACK + 'Start check')
			name = name.strip()
			name = name.lower()
			if ' ' in name:
				name_space = name.count(' ')
				if name_space == 1 or name_space >= 2:
					list_name = name.split(' ')
					searched_words = words_search(list_name, name, price, datalist)
					find_list_compare_words(searched_words)
			else:
				pass
			i = 0
			for k in datalist:
				k_name = k['name']
				k_price = k['price']
				k_name = k_name.lower()
				if name in k_name and price in k_price:
					try:
						test=0
						# print(Back.LIGHTCYAN_EX + Fore.BLACK + Style.DIM +
						# 	f'\n=====\nПо названию {name} и цене {price}: {datalist[i]}\n=====')
					except:
						print(Fore.RED + 'ошибка')
				else:
					if name in k_name:
						try:
							test = 0
							# print(Style.RESET_ALL + 'по названию:', datalist[i])
						except:
							print(Fore.RED + 'ошибка')
				i = i + 1
			print(Style.RESET_ALL + f'Всего программ: {i}')
			COUNT_PROGRAMS = i
		else:
			print(Fore.RED+f'Проверте правильность введенных данных. Скорее всего имя не ЗАДАНО (это текст исключения на пустоту переменной "name": {type(name)}={name})')
	except Exception as e:
		print(Fore.RED+f'{e}')