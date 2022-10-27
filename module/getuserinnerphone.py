from datetime import datetime
import re
from colorama import Fore,Back,Style
from time import sleep
from btrx import btrx
from pydantic import BaseModel,StrictInt,StrictStr,StrictBool
from typing import Optional
import json,os
loop_while = False
clear = lambda: os.system('cls')

class UserInnerPhoneData(BaseModel):
	inner_phone: Optional[StrictInt] = None
	zdr_phone: Optional[StrictStr] = None
	password: Optional[StrictStr] = None
class UserEmailData(BaseModel):
	email: Optional[StrictStr] = None
	password: Optional[StrictStr] = None
class LastCheckDatetimeData(BaseModel):
	date: Optional[StrictStr] = None
	time: Optional[StrictStr] = None

def workwithdata():
	"""
		Build main data [list] of Pydantic {dict}
	"""

	"Data to append for main Pydantic Data() class"
	user_inner_phone_data = UserInnerPhoneData()
	user_email_data = UserEmailData()
	last_check_datetime_data = LastCheckDatetimeData()

	if os.path.exists('data/json/btrx_data/companyusers.json'):
		print('path data/json/btrx_data/companyusers.json exists')
		with open('data/json/btrx_data/companyusers.json','r',encoding='utf-8') as f:
			json_data = json.loads(f.read())
		main_js_data_list = []
		user_count = 1
		for data in json_data:
			# print(f"{data['NAME']} {data['LAST_NAME']} \ {data['UF_PHONE_INNER']}")
			# print(user_count,user,id,workposit)
			now = datetime.now()
			last_date = now.strftime("%d-%m-%Y")
			last_time = now.strftime("%H:%M:%S")
			user_inner_phone_data.inner_phone = data['UF_PHONE_INNER']
			user_email_data.email = data['EMAIL']
			last_check_datetime_data.date = last_date
			last_check_datetime_data.time = last_time

			"Main Pydantic Data() model class"
			class Data(BaseModel):
				id: Optional[StrictInt] = None
				name: Optional[StrictStr] = None
				email: dict = user_email_data.dict()
				department: Optional[StrictStr] = None
				position: Optional[StrictStr] = None
				inner_phone: dict = user_inner_phone_data.dict()
				is_active: Optional[StrictBool] = None
				last_check_datetime: dict = last_check_datetime_data.dict()
			js_data = Data()
			js_data.id = data['ID']
			js_data.name = user = f"{data['NAME']} {data['LAST_NAME']}"
			js_data.department = data['UF_DEPARTMENT']
			js_data.position = data['WORK_POSITION']
			js_data.is_active = data['ACTIVE']

			main_js_data_dict = js_data.dict()
			main_js_data_list.append(main_js_data_dict)
			user_count = user_count + 1


		with open('data/json/btrx_data/inner_phone_users.json','w',encoding='utf-8') as f:
			json.dump(main_js_data_list,f,indent=4,ensure_ascii=False)

		count_users = 0
		for i,user in enumerate(main_js_data_list):
				count_users = count_users + 1
		print(f"Всего пользователей: {count_users}")
	else:
		load_users_from_btrx(btrx)

def load_users_from_btrx(btrx):
	btrx_users = []
	try:
		btrx_users = btrx.get_all('user.get',params={"ADMIN_MODE": True})
		with open('data/json/btrx_data/companyusers.json','w',encoding='utf-8') as f:
			json.dump(btrx_users,f,ensure_ascii=False,indent=4,sort_keys=True)
		print('Сохранено в data/json/btrx_data/companyusers.json')
		workwithdata()
	except Exception as e:
		print(f"load_users_from_btrx {e}")

"Cписок всех пользователей"
def seealluser():
	clear()
	count_all_user = 0
	for i,data in enumerate(loadJsonData()):
		count_all_user = count_all_user + 1
		print(f"ID: {data['id']}\nName: {data['name']}\nEmail: {data['email']['email']}\nInner_ph: {data['inner_phone']['inner_phone']}")
	print(f'Всего показано: {count_all_user}')

"Cписок активных пользователей"
def seeallactiveuser():
	clear()
	for i,data in enumerate(loadJsonData()):
		if data['is_active'] == True:
			print(Fore.GREEN+'*'*15+Fore.RESET)
			print(f"ID: {data['id']}\nName: {data['name']}\nEmail: {data['email']['email']}\nInner_ph: {data['inner_phone']['inner_phone']}")

"Cписок не активных пользователей"
def seeallnotactiveuser():
	clear()
	for i,data in enumerate(loadJsonData()):
		if data['is_active'] == False:
			print(Fore.LIGHTBLACK_EX+'-'*15+Fore.RESET)
			print(f"ID: {data['id']}\nName: {data['name']}\nEmail: {data['email']['email']}\nInner_ph: {data['inner_phone']['inner_phone']}\nIs_active: {data['is_active']}")

"Список занятых внутренних номеров"
def seeallinnerphone():
	clear()
	for i,data in enumerate(loadJsonData()):
		if data['inner_phone']['inner_phone'] is not None:
			print(Fore.YELLOW+'*'*15+Fore.RESET)
			print(f"ID: {data['id']}\nName: {data['name']}\nEmail: {data['email']['email']}\nInner_ph: {data['inner_phone']['inner_phone']}")

"""
TODO нужно изменять данные и сохраянять их локально
- [ ] Изменение пароля для Email
- [ ] Изменение пароля для Bitrix24
- [ ] Изменение внутреннего телефона
- [ ] Изменение пароля для внутреннего телефона
"""
"Пример изменения данных"
def changevaluebyID():
	clear()
	id= input('Select ID: ')
	old_name = '-'
	new_name = '+'
	old_js = loadJsonData()
	new_js = loadJsonData()
	for i,datas in enumerate(old_js):
		if datas['id'] == id:
			old_name = datas['email']
	for i,data in enumerate(new_js):
		if data['id'] == id:
			new_js[i]['email']['password'] = input('New password: ')
			new_name = data['email']
	print(f"old: {old_name}\nnew: {new_name}")
	try:
		with open('data/json/btrx_data/inner_phone_users.json','w',encoding='utf-8') as f:
			json.dump(new_js,f,indent=4,ensure_ascii=False)
	except Exception as e:
		print(e)

"Поиск по ID"
def searchByID():
	clear()
	id= input('Select ID: ')
	for i,data in enumerate(loadJsonData()):
		if data['id'] == id:
			print(f"ID: {data['id']}\nName: {data['name']}\nEmail: {data['email']['email']}\nInner_ph: {data['inner_phone']['inner_phone']}")
	opt_menu()

"Поиск по имени"
def searchByName():
	clear()
	search_name = input("Введите имя (неявный поиск):\n")
	json_data = loadJsonData()
	count_find_users = 0
	position_number_list = []
	for i,data in enumerate(json_data):
		if search_name.lower().strip() in data['name'].lower().strip():
			count_find_users = count_find_users + 1
	"Проверка"
	if count_find_users == 1:
		for i,data in enumerate(json_data):
			if search_name.lower().strip() in data['name'].lower().strip():
				print(Fore.GREEN+f"\
ID: {data['id']}\n\
Name: {data['name']}\n\
Email: {data['email']['email']}\n\
Inner_ph: {data['inner_phone']['inner_phone']}\nIs_active: {data['is_active']}"+ Fore.RESET)

	else:
		for i,data in enumerate(json_data):
			if search_name.lower().strip() in data['name'].lower().strip():
				position_number = i+1
				print(Fore.MAGENTA+'*'*15+Fore.RESET)
				print(f"{Fore.CYAN}[{position_number}]{Fore.RESET}\nID: {data['id']}\nName: {data['name']}\nEmail: {data['email']['email']}\nInner_ph: {data['inner_phone']['inner_phone']}\nIs_active: {data['is_active']}")
				position_number_list.append(position_number)
	count_position_number = 0
	selected_user = None
	for i_posit,data_posit in enumerate(position_number_list):
		count_position_number = count_position_number + 1
	if count_position_number >= 2:
		try:
			select_position = int(input('Выберите номер найденных клиентов (000 выбрать только с внутренним телефоном):\n'))
		except:
			print('\nВведите целое число без букв')
			select_position = int(input('Выберите номер найденного клиента (000 выбрать только с внутренним телефоном):\n'))
		if select_position == 000:
			posit_number = 0
			for i_inner,data_inner in enumerate(json_data):
				posit_number = i_inner + 1
				if search_name.lower().strip() in data_inner['name'].lower().strip():
					if data_inner['inner_phone']['inner_phone'] is not None:
							print('\n'+Fore.LIGHTBLUE_EX+'*'*15+Fore.RESET)
							print(f"{Fore.CYAN}[{posit_number}]{Fore.RESET}\nID: {data_inner['id']}\nName: {data_inner['name']}\nEmail: {data_inner['email']['email']}\nInner_ph: {data_inner['inner_phone']['inner_phone']}\nIs_active: {data_inner['is_active']}")
		for i_position,data_position in enumerate(position_number_list):
			fact_index = data_position - 1
			if select_position == data_position:
				selected_user = json_data[fact_index]
				print(Fore.GREEN+f"\
ID: {selected_user['id']}\n\
Name: {selected_user['name']}\n\
Email: {selected_user['email']['email']}\n\
Inner_ph: {selected_user['inner_phone']['inner_phone']}"+ Fore.RESET)

def loadJsonData() -> list:
	if os.path.exists('data/json/btrx_data/inner_phone_users.json'):
		with open('data/json/btrx_data/inner_phone_users.json','r',encoding='utf-8') as f:
			json_data = json.loads(f.read())

	return list(json_data)

def print_menu():
	print('1) Cписок всех пользователей.')
	print('2) Cписок активных пользователей.')
	print('3) Cписок не активных пользователей.')
	print('4) В меню поиска по конкретным данным ->')
	print('5) Список занятых внутренних номеров.')
	print('6) Обновить пользователей из Битрикс24.')
	print('0) Выход.')


def print_searchmenu():
	print('1) Поиск по ID.')
	print('2) Поиск по Имени.')
	print('3) Поиск по Фамилии.')
	print('4) Поиск по Внутреннему телефону.')
	print('5) Поиск по Должности.')
	print('6) Поиск по Отделу.')
	print('7) Поиск по Номеру телефона.')
	print('9) Назад.')
	print('0) Выход.')


def print_selectWhenManyUserFind():
	print('1) Изменить пароль.')
	print('2) Изменить номер телефона (zdr).')
	print('9) Назад.')
	print('0) Выход.')

def print_selectOptMenu():
	print('1) Изменить пароль.')
	print('2) Изменить номер телефона (zdr).')
	print('9) Назад.')
	print('0) Выход.')

def many_user_find_menu():
	while True:
		print_selectWhenManyUserFind()
		select_opt = int(input('Select optiopn: ').strip())
		if select_opt == 1:
			changevaluebyID()
		elif select_opt == 9:
			menu()
		elif select_opt == 0:
			exit()

def opt_menu():
	while True:
		print_selectOptMenu()
		select_opt = int(input('Select optiopn: ').strip())
		if select_opt == 1:
			changevaluebyID()
		elif select_opt == 9:
			menu()
		elif select_opt == 0:
			exit()


def search_menu():
	while True:
		print_searchmenu()
		select_opt = int(input('Select optiopn: ').strip())
		if select_opt == 1:
			searchByID()
		elif select_opt == 2:
			searchByName()
		elif select_opt == 9:
			menu()
		elif select_opt == 0:
			exit()


def menu():
	global loop_while
	check = 0
	loop_while = False
	clear()
	while not loop_while:
		sleep(1)
		print_menu()
		select_opt = int(input('Select optiopn: ').strip())
		if select_opt == 1:
			seealluser()
		elif select_opt == 2:
			seeallactiveuser()
		elif select_opt == 3:
			seeallnotactiveuser()
		elif select_opt == 4:
			search_menu()
		elif select_opt == 5:
			seeallinnerphone()
		elif select_opt == 6:
			load_users_from_btrx(btrx)
		elif select_opt == 0:
			print('Выход')
			exit()
		else:
			print('input correct num')


if __name__ == "__main__":
	# load_users_from_btrx(btrx)
	# seeallactiveuser()
	menu()
	# workwithdata()
	# changevaluebyID()
	# searchByName()