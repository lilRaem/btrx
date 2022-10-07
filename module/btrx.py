import json, os
from typing import Optional
from pydantic import BaseModel, StrictStr
from fast_bitrix24 import Bitrix
from colorama import Fore, Back, Style
try:
	from config import FinalData
except:
	from module.config import FinalData
webhook = 'https://b24-vejk6x.bitrix24.ru/rest/1/di28gta836z3xn50/'
btrx = Bitrix(webhook=webhook,respect_velocity_policy=False)

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

def load_from_jsonFile(filename='*.json', path=str()) -> list:
	# sleep(2)
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

def get_users_with_innerPhone(btrx=Bitrix(webhook)) -> list:
	users = []
	try:
		users = btrx.get_all('user.get',{
			'select': ['ID','ACTIVE','NAME','LAST_NAME','EMAIL','UF_DEPARTMENT','WORK_POSITION','UF_PHONE_INNER']
		})
		return list(users)
	except Exception as e:
		print(e)
		raise TypeError('get_users_with_innerPhone error')

def get_product_id(data):
	for item in data:
		yield item['ID']

def get_product_name(data):
	for item in data:
		yield item['NAME']

def get_product_hour(data):
	for item in data:
		i = item['PROPERTY_213']
		yield i['value']

def get_product_price(data):
	for item in data:
		yield item['PRICE']
def set_product_price(btrx=Bitrix(webhook),id=str(),price=0):
	try:
		params = {"ID": id, "fields":{
			'PRICE': price
		}}
		res = btrx.call('crm.product.update',params)
		print(f'Price {price} for {id} is SET {res}'+Style.RESET_ALL+"\n")
	except Exception as e:
		print(e)

def get_all_data(data):
	"""Get all data	(id, name, price, hours) with hours\n
		in description and exclude ['PROPERTY_213']	= None"""
	if (data == None or type(data) != list):
		raise TypeError(f'expect type of data = list')
	datalist=list()
	final_data = FinalData()
	wh = 0
	woh = 0
	try:
		for item in data:

			id = item['ID']
			name = item['NAME']
			price = item['PRICE']
			hour = item['PROPERTY_213']
			linkNmo = ''
			url = ''

			if id != '' or id != None:
				id = item['ID']
			else:
				id = None
			if name == '' or name == None:
				name = None
			else:
				name = item['NAME']
			if price == '' or price == None:
				price = None
			else:
				price = price = item['PRICE']
				price = price.replace('.00', '')
			if hour == '' or hour == None:
				hour = None
			else:
				hour = hour.get('value')
			if linkNmo == '' or linkNmo == None:
				linkNmo = None
			else:
				linkNmo = 'linkNmo'
			if url == '' or url == None:
				url = None
			else:
				url = 'url'

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
									# print('find_all_count (word in k_name)',find_all_count)
									# print(Style.RESET_ALL+f'Current word: {word} and program in search: {datalist[name_price]}')
									# print(Fore.LIGHTYELLOW_EX + f'\nпо слову {word}:',
									# 	datalist[find_all_count], '\n' + Fore.RESET + Style.RESET_ALL)
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

def check_product(name=str, price=str, datalist=list) -> list:
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
					k_name = data_list['name']
					k_price = data_list['price']
					k_name = k_name.lower()
					if name.lower() in k_name and price == k_price and price != '':
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
					k_name = data_list['name']
					k_price = data_list['price']
					k_name = k_name.lower()

					if name.lower() in k_name and price == k_price and price != '':

						try:
							if count_name_price == 1 and price != '':
								if name.lower() == k_name:
									print("\n"+Back.LIGHTCYAN_EX + Fore.BLACK + Style.DIM +
										f'=====\nПо названию {name} и цене {price}:\n{datalist[i]}\n====='+Style.RESET_ALL+"\n")
									found_data_by_name_price.append(datalist[i])
								else:
									print("\n"+Back.CYAN + Fore.BLACK + Style.DIM +
										f'=====\nПо содержанию названия {name} и цене {price}:\n{datalist[i]}\n====='+Style.RESET_ALL+"\n")
									found_data_by_name_price.append(datalist[i])
							else:
								print(Back.LIGHTMAGENTA_EX + Fore.BLACK + Style.DIM +
									f'\n=====\nПо названию {name} и цене {price}: {datalist[i]}\n====='+Style.RESET_ALL+"\n")
								found_data_by_name_price.append(datalist[i])
						except:
							print(Fore.RED + 'Ошибка при поиске названия и цены')

					else:

						if name.lower() in k_name:
							try:
								# print(Style.RESET_ALL + Fore.LIGHTBLACK_EX + f'[{Back.GREEN + v["id"] + Back.RESET}] "{k_name}"\n')

								if count_name == 1:
									print("\n"+Style.RESET_ALL + Fore.BLACK + f'[{Back.LIGHTGREEN_EX + Fore.BLACK  + v["id"] + Back.RESET}]' + f' {Fore.RESET}"{k_name}"')
									found_data_by_name.append(datalist[i])
								else:
									print(Style.RESET_ALL + Fore.BLACK + f'[ {Back.GREEN + Fore.BLACK  + v["id"] + Back.RESET} ]' + f' {Fore.LIGHTBLACK_EX}"{v["name"]}|{v["hour"]}|{v["price"]}"')
									found_data_by_name.append(datalist[i])
							except:
								print(Fore.RED + 'Ошибка при поиске названия')

			except Exception as e:
				print(e)
			print(Style.RESET_ALL + f'Всего программ: {i}')

			if found_data_by_name_price != []:
				count_fdbnp = 0
				for data in found_data_by_name_price:
					count_fdbnp = count_fdbnp + 1
				if count_fdbnp == 1:
					return found_data_by_name_price[0]
				else:
					print(f"Найдено {count_fdbnp} программ с одинаковым названием и ценой\
					\n(или содержания слова в названии и цена)")
					for data in found_data_by_name_price:
						print(Fore.YELLOW+f'{data}'+Fore.RESET)
						if name.lower() in data['name'].lower():
							if name.lower() in data['name'].lower():
								if price == data['price'].lower():
									return found_data_by_name_price[0]
			elif found_data_by_name != []:
				count_dbn = 0
				for data in found_data_by_name:
					count_dbn = count_dbn + 1
				if count_dbn == 1:
					return found_data_by_name[0]
				else:
					list_by_name = []
					print(f"Найдено {count_dbn} программ с одинаковым названием\
					\n(или содержания слова в названии)")

					count_by_name = 0
					for data_ in found_data_by_name:
						count_by_name = count_by_name + 1
					if count_by_name != 0:
						for data in found_data_by_name:
							# final_data here. i think...
							print(Fore.LIGHTYELLOW_EX+f'\n{data}'+Fore.RESET)
							product_id = data['id']

							product_spec = None
							product_name = data['name']
							product_price = data['price']
							product_hour = data['hour']
							product_linkNmo = data['linkNmo']
							product_url = data['url']

							dictData = {
								'id': product_id,
								'spec': product_spec,
								'name': product_name,
								'price': product_price,
								'hour': product_hour,
								'linkNmo': product_linkNmo,
								'url': product_url
							}
							list_by_name.append(dictData)
						count_list_data_by_name = 0
						for data in list_by_name:
							count_list_data_by_name = count_list_data_by_name + 1
						if count_list_data_by_name == 1:
							dictData = {
								'id': None,
								'spec': None,
								'name': product_name,
								'price': None,
								'hour': None,
								'linkNmo': None,
								'url': None
							}
							return dictData
						else:
							dictData = {
								'id': None,
								'spec': None,
								'name': product_name,
								'price': None,
								'hour': None,
								'linkNmo': None,
								'url': None
							}
							return dictData
			else:
				print('Not found')
				return None
		else:
			print(Fore.RED+f'Проверте правильность введенных данных. Скорее всего имя не ЗАДАНО (это текст исключения на пустоту переменной "name": {type(name)}={name})')

	except Exception as e:
		print(Fore.RED+f'{e}')