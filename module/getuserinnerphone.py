from datetime import datetime
from colorama import Fore,Back,Style
from time import sleep
from btrx import btrx
from pydantic import BaseModel,StrictInt,StrictStr,StrictBool
from typing import Optional
import json,os
loop_while = False
clear = lambda: os.system('cls')

def workwithdata():
	class UserInnerPhoneData(BaseModel):
		inner_phone: Optional[StrictInt] = None
		zdr_phone: Optional[StrictStr] = None
		password: Optional[StrictStr] = None
	user_inner_phone_data = UserInnerPhoneData()
	class UserEmailData(BaseModel):
		email: Optional[StrictStr] = None
		password: Optional[StrictStr] = None
	user_email_data = UserEmailData()
	class LastCheckDatetimeData(BaseModel):
		date: Optional[StrictStr] = None
		time: Optional[StrictStr] = None
	last_check_datetime_data = LastCheckDatetimeData()
	if os.path.exists('data/json/btrx_data/companyusers.json'):
		print('path data/json/btrx_data/companyusers.json exists')
		with open('data/json/btrx_data/companyusers.json','r',encoding='utf-8') as f:
			json_data = json.loads(f.read())
		js_list = []
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

			d = js_data.dict()
			js_list.append(d)
			user_count = user_count + 1


		with open('data/json/btrx_data/inner_phone_users.json','w',encoding='utf-8') as f:
			json.dump(js_list,f,indent=4,ensure_ascii=False)

		# with open('data/json/btrx_data/inner_phone_users.json','r',encoding='utf-8') as f:
		# 	userdata = json.loads(f.read())

		for i,user in enumerate(js_list):
				co = i
				# print(userdata[user])
		# clear()
		print(f"Всего пользователей: {i}")
	else:
		load_users_from_btrx(btrx)

def seeallinnerphone():
	clear()
	if os.path.exists('data/json/btrx_data/inner_phone_users.json'):
		with open('data/json/btrx_data/inner_phone_users.json','r',encoding='utf-8') as f:
			json_data = json.loads(f.read())
		for i,data in enumerate(json_data):
			if data['inner_phone']['inner_phone'] is not None:
				print(Fore.YELLOW+'*'*15+Fore.RESET)
				print(f"ID: {data['id']}\nName: {data['name']}\nEmail: {data['email']['email']}\nInner_ph: {data['inner_phone']['inner_phone']}")

def seealluser():
	clear()
	if os.path.exists('data/json/btrx_data/inner_phone_users.json'):
		with open('data/json/btrx_data/inner_phone_users.json','r',encoding='utf-8') as f:
			json_data = json.loads(f.read())
		for i,data in enumerate(json_data):
			print(f"ID: {data['id']}\nName: {data['name']}\nEmail: {data['email']['email']}\nInner_ph: {data['inner_phone']['inner_phone']}")
		print(f'Всего показано: {i}')

def seeallactiveuser():
	clear()
	if os.path.exists('data/json/btrx_data/inner_phone_users.json'):
		with open('data/json/btrx_data/inner_phone_users.json','r',encoding='utf-8') as f:
			json_data = json.loads(f.read())
		for i,data in enumerate(json_data):

			if data['is_active'] == True:
				print(Fore.GREEN+'*'*15+Fore.RESET)
				print(f"ID: {data['id']}\nName: {data['name']}\nEmail: {data['email']['email']}\nInner_ph: {data['inner_phone']['inner_phone']}")


def seeallnotactiveuser():
	clear()
	if os.path.exists('data/json/btrx_data/inner_phone_users.json'):
		with open('data/json/btrx_data/inner_phone_users.json','r',encoding='utf-8') as f:
			json_data = json.loads(f.read())
		for i,data in enumerate(json_data):
			if data['is_active'] == False:
				print(Fore.LIGHTBLACK_EX+'-'*15+Fore.RESET)
				print(f"ID: {data['id']}\nName: {data['name']}\nEmail: {data['email']['email']}\nInner_ph: {data['inner_phone']['inner_phone']}")

def changevaluebyID():
	clear()
	if os.path.exists('data/json/btrx_data/inner_phone_users.json'):
		with open('data/json/btrx_data/inner_phone_users.json','r',encoding='utf-8') as f:
			json_data = json.loads(f.read())
	id= input('Select ID: ')
	old_name = '-'
	new_name = '+'
	old_js = json_data
	for i,datas in enumerate(old_js):
		if datas['id'] == id:
			old_name = datas['email']
	for i,data in enumerate(json_data):
		if data['id'] == id:
			json_data[i]['email']['password'] = input('New password: ')
			new_name = data['email']
	print(f"old: {old_name}\nnew: {new_name}")
	try:
		with open('data/json/btrx_data/inner_phone_users.json','w',encoding='utf-8') as f:
			json.dump(json_data,f,indent=4,ensure_ascii=False)
	except Exception as e:
		print(e)
def searchByID():
	clear()
	if os.path.exists('data/json/btrx_data/inner_phone_users.json'):
		with open('data/json/btrx_data/inner_phone_users.json','r',encoding='utf-8') as f:
			json_data = json.loads(f.read())
	id= input('Select ID: ')

	for i,data in enumerate(json_data):
		if data['id'] == id:
			print(f"ID: {data['id']}\nName: {data['name']}\nEmail: {data['email']['email']}\nInner_ph: {data['inner_phone']['inner_phone']}")
	opt_menu()

def load_users_from_btrx(b):
	users = []
	try:
		users = b.get_all('user.get',params={"ADMIN_MODE": True})
		with open('data/json/btrx_data/companyusers.json','w',encoding='utf-8') as f:
			json.dump(users,f,ensure_ascii=False,indent=4,sort_keys=True)
		print('Сохранено в data/json/btrx_data/companyusers.json')
		workwithdata()
		# menu()
	except Exception as e:
		print(f"load_users_from_btrx {e}")
		users = b.get_all('user.get')
		with open('data/json/btrx_data/companyusers.json','w',encoding='utf-8') as f:
			json.dump(users,f,ensure_ascii=False,indent=4,sort_keys=True)
		print('succes on second')
		# raise TypeError('get_users_with_innerPhone error')

def print_menu():
	print('1) Весь список пользователей.')
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

def print_selectOptMenu():
	print('1) Изменить пароль.')
	print('2) Изменить номер телефона (zdr).')
	print('9) Назад.')
	print('0) Выход.')

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