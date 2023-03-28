from datetime import date
import json, os
from fast_bitrix24 import Bitrix
from colorama import Fore, Back, Style
try:
	try:
		from module.config import FinalData, BtrxConfig
	except:
		from config import FinalData, BtrxConfig
except:
	from config import FinalData, BtrxConfig

# webhook = 'https://b24-vejk6x.bitrix24.ru/rest/1/di28gta836z3xn50/'
# btrx = Bitrix(webhook=webhook,respect_velocity_policy=False)
class Btrx(Bitrix):
	def __init__(self):
		self.webhook = f'https://b24-vejk6x.bitrix24.ru/rest/1/{BtrxConfig.id}/'
		super().__init__(webhook=self.webhook,respect_velocity_policy=False)

	def save_to_json(self, datalist:list[dict[str,str|int|None]], filename: str, path: str):

		if datalist == None or type(datalist) != list: raise TypeError(f'тип datalist({type(datalist)}) должен быть {list}')
		elif filename == None or type(filename) != str: raise TypeError(f'тип filename({type(filename)}) должен быть str')
		elif path == None or type(path) != str: raise TypeError(f'тип path({type(path)}) должен быть str')

		try:
			if (os.path.exists(path)):
				with open(os.path.join(path, f"{filename}"), 'w', encoding='utf-8') as file:
					# sleep(1)
					try:
						json.dump(datalist,file, ensure_ascii=False, indent=4)
					except Exception as e:
						raise TypeError(Fore.RED + f'Error save to json {e}'+Fore.RESET)
			return datalist
		except Exception as e:
			raise TypeError(f'{e}')

	def load_from_jsonFile(self,filename:str = "file.json", path: str = str()) -> list[dict[str,str|int|None]]:
		if type(filename) != str: raise TypeError('тип filename должен быть str')
		elif type(path) != str: raise TypeError('тип path должен быть str')
		try:
			data_from_file = list([dict[str,str|int|None]])
			if (os.path.exists(path)):
				print(f"current path: {path}")
				with open(os.getcwd()+"\\"+path+"\\"+filename, 'r', encoding='utf-8') as file:
					data_from_file = json.load(file)
					print(Style.RESET_ALL + Fore.BLACK + f'\nLoad from {filename}' + Style.RESET_ALL)
				return data_from_file
			else:
				os.mkdir(path)
		except Exception as e:
			raise TypeError(Fore.RED + f'Error in load_from_jsonFile {e}'+ Fore.RESET)

	def get_product_list(self) -> list[dict[str,str|int|None]]:
		"""Load	from btrx24	all	data (id, name,	price, hours)\n
			hours data in field: ['PROPERTY_213'] => ['value']"""
		try:
			products = list()
			products = self.get_all('crm.product.list',
				params={'select': ['ID', 'NAME', 'PRICE', 'PROPERTY_213']})
			return products
		except Exception as e: raise TypeError(Fore.RED + f'\nGet products error: {e}\n')
		finally: return products

	def get_users_with_innerPhone(self) -> list:
		try:
			users = list()
			users = self.get_all('user.get',params={
				'select': ['*']
			})
			return list(users)
		except Exception as e: raise TypeError(f'get_users_with_innerPhone error {e}')

	def get_all_client(self):
		try:
			contact = list()
			contact = self.get_all("crm.contact.list",params={
				"select": ['*']
			})
			return contact
		except Exception as e:
			raise TypeError(f"get_all_client error {e}")

	def set_product_price(self,id=str(),price=0):
		try:
			params = {"ID": id, "fields":{
				'PRICE': price
			}}
			res = self.call('crm.product.update',params)
			print(f'Price {price} for {id} is SET {res}'+Style.RESET_ALL+"\n")
		except Exception as e: raise TypeError(Fore.RED+f"Error in set_product_price(): {e}"+Fore.RESET)

	def get_all_data(self,data: list[dict[str,str|int|None]]) -> list[dict[str,str|int|None]]:
		"""
		Get all data (id, name, price, hours) with hours
		"""
		if (data == None or type(data) != list): raise TypeError(f'expect type data == list.\nNow: {type(data)}')

		with_hour = 0
		without_hour = 0

		try:
			datalist: list[dict[str,str|int|None]] = list()
			for item in data:
				final_data = FinalData()

				if item.get("ID"): final_data.id = int(item.get("ID"))
				if item.get("NAME"): final_data.name = item.get("NAME")

				if item.get("PRICE"): price = int(item.get("PRICE").replace(".00",""))
				else: price = None
				if price: final_data.price = int(price)

				if item.get('PROPERTY_213'):
					hour = item.get('PROPERTY_213')
					final_data.hour = int(hour.get('value'))

				datalist.append(final_data.dict())

				if final_data.hour: with_hour = with_hour + 1
				else: without_hour = without_hour + 1
			print(Fore.LIGHTCYAN_EX +  f'\n####\n{Back.CYAN}Find{Style.RESET_ALL} {with_hour} {Back.CYAN}items{Style.RESET_ALL} {Back.GREEN+Fore.BLACK}with hours' + Style.RESET_ALL)
			print(Fore.BLUE + f'\nFind {without_hour} items without hours')
			print(Fore.CYAN + f'\nFind {with_hour+without_hour} items all\n####\n')
			return datalist
		except Exception as e:
			raise TypeError(Fore.RED + f'Ошибка в get_all_data. type of\ndata({type(data)}), datalist({type(datalist)}),\nexpect data(list) and datalist(list)\n{e}'+Fore.RESET)

	def words_search(self, words_list=list, name=str, price=int, datalist=list[dict[str,str|int|None]]) -> list:

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
									with open(f'{os.getcwd()}\\data\\json\\btrx_data\\tmpfile.json','w', encoding='utf-8') as file:
										data_list = json.dump(words_data,file, ensure_ascii=False, indent=4)
									find_name_price_count = find_name_price_count + 1
									# return list(words_data)
								except Exception as e:
									raise TypeError(Fore.RED + Style.DIM + f'ошибка check_product-> if word in k_*: {e}')

							else:
								if word in k_name:
									try:
										find_word_count = find_word_count + 1
									except Exception as e:
										raise TypeError(Fore.RED + f'ошибка {e}')
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

	def check_product(self, name: str, price: int, datalist: list[dict[str,str|int|None]]) -> list[dict[str,str|int|None]]:

		if type(name) != str or type(price) != int: raise TypeError(f"Type name == {type(name)}\n\
							      Type price == {type(price)}\n except (str,int)")
		try:
			final_data = FinalData()
			if name:
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
				found_data_by_name_price: list[dict[str,str|int|None]] = list()
				found_data_by_name: list[dict[str,str|int|None]] = list()

				try:
					for data in datalist:
						if data.get("name"): final_data.name = data.get("name")
						if data.get("price"): final_data.price = data.get("price")
						if name.lower() in final_data.name.lower() and price == final_data.price and price != 0:
							count_name_price = count_name_price + 1
						else:
							if name.lower() in final_data.name.lower(): count_name = count_name + 1
					print(f'Найдено:\nИмя/цена: {count_name_price} шт\nИмя: {count_name} шт'+ Style.RESET_ALL)
				except Exception as e: raise TypeError(Fore.RED+f"On start check error: \n\nExeption:\n{e}")

				try:
					for data in datalist:
						if data.get("name"): final_data.name = data.get("name")
						if data.get("price"): final_data.price = data.get("price")

						if name.lower() in final_data.name.lower() and price == final_data.price and price != 0:
							try:
								if count_name_price == 1 and price != 0:
									if name.lower() == final_data.name.lower():
										print("\n"+Back.LIGHTCYAN_EX + Fore.BLACK + Style.DIM +
											f'=====\nПо названию {name} и цене {price}:\n{data}\n====='+Style.RESET_ALL+"\n")
										found_data_by_name_price.append(data)
									else:
										print("\n"+Back.CYAN + Fore.BLACK + Style.DIM +
											f'=====\nПо содержанию названия {name} и цене {price}:\n{data}\n====='+Style.RESET_ALL+"\n")
										found_data_by_name_price.append(data)
								else:
									print(Back.LIGHTMAGENTA_EX + Fore.BLACK + Style.DIM +
										f'\n=====\nПо названию {name} цена по поиску {price}: {data}\n====='+Style.RESET_ALL+"\n")
									found_data_by_name_price.append(data)
							except Exception as e:
								print(Fore.RED + f'1. Ошибка при поиске названия и цены {e}')
						else:
							if name.lower() in final_data.name.lower():
								try:
									if count_name == 1:
										print("\n"+Style.RESET_ALL + Fore.BLACK + f'[{Back.LIGHTGREEN_EX + Fore.BLACK  + str(data.get("id")) + Back.RESET}]' + f' {Fore.RESET}{data.get("name")}|{data.get("hour")}|{data.get("price")}')
										found_data_by_name.append(data)
									else:
										print(Style.RESET_ALL + Fore.BLACK + f'[ {Back.GREEN + Fore.BLACK  + str(data.get("id")) + Back.RESET} ]' + f' {Fore.LIGHTBLACK_EX}"{data.get("name")}|{data.get("hour")}|{data.get("price")}"')
										found_data_by_name.append(data)
								except Exception as e: print(Fore.RED + '2. Ошибка при поиске названия\n'+Fore.RED+f'{e}')
				except Exception as e: raise TypeError(e)

				print(Style.RESET_ALL + f'Всего программ: {datalist.__len__()}')

				if found_data_by_name_price:
					if found_data_by_name_price.__len__() == 1:
						print(Fore.YELLOW+f'{found_data_by_name_price}'+Fore.RESET)
						return found_data_by_name_price
					else:
						print(f"Найдено {found_data_by_name_price.__len__()} программ с одинаковым названием и ценой\
						\n(или содержания слова в названии и цена)\n")
						similar_list: list[dict[str,str|int|None]] = list()
						for i,data in enumerate(found_data_by_name_price):
							if name.lower() == data.get('name').lower() and price == int(data.get('price')):
								print("\n"+Fore.GREEN+f'{i+1} {data}'+Fore.RESET+"\n")
								similar_list.append(data)
							else:
								print(Fore.YELLOW+f'{i+1} {data}'+Fore.RESET+"\n")
						if similar_list:
							return similar_list
						else:
							return found_data_by_name_price
				elif found_data_by_name:
					if found_data_by_name.__len__() == 1:
						return found_data_by_name
					else:
						list_by_name: list[dict[str,str|int|None]] = list()
						print(f"Найдено {found_data_by_name.__len__()} программ с одинаковым названием\
						\n(или содержания слова в названии)")
						if found_data_by_name:
							for data in found_data_by_name:
								final_data = FinalData()
								print(Fore.LIGHTYELLOW_EX+f'\n{data}'+Fore.RESET)
								if data.get("id"): final_data.id = int(data.get("id"))
								if data.get("name"): final_data.name = data.get("name")
								if data.get("price"): final_data.price = int(data.get("price"))
								if data.get("hour"): final_data.hour = int(data.get("hour"))
								list_by_name.append(final_data.dict())
							return list_by_name
				else:
					print('Not found')
					return None
			else:
				print(Fore.RED+f'Проверьте правильность введенных данных. Скорее всего имя не ЗАДАНО (это текст исключения на пустоту переменной "name": {type(name)}={None})')
		except Exception as e:
			raise TypeError(Fore.RED+f'{e}'+Fore.RESET)

def check_null(variable, iter):
	if variable:
		variable = iter
	else:
		variable = None
	return variable

if __name__ == '__main__':
	btrx = Btrx()
	data = []
	dat = btrx.get_all_client()
	print(dat)
	with open("allcontact","w", encoding="utf-8") as file:
		file.write(dat)
