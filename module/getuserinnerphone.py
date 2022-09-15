from time import sleep
from fast_bitrix24 import Bitrix
from btrx import get_users_with_innerPhone, btrx,webhook
import json,os
loop_while = False
clear = lambda: os.system('cls')
def checkfornull(data):
	if data == '' or data is None or data == 'null':
		data = 'empty'
		# return data
	else:
		return data

def workwithdata():
	if os.path.exists('data/json/btrx_data/companyusers.json'):
		with open('data/json/btrx_data/companyusers.json','r',encoding='utf-8') as f:
			json_data = json.loads(f.read())
		js = {}
		user_count = 1
		for data in json_data:
			# print(f"{data['NAME']} {data['LAST_NAME']} \ {data['UF_PHONE_INNER']}")
			id = checkfornull(data['ID'])
			user = f"{checkfornull(data['NAME'])} {checkfornull(data['LAST_NAME'])}"
			workdepartment = checkfornull(data['UF_DEPARTMENT'])
			workposit = checkfornull(data['WORK_POSITION'])
			inner_phone = checkfornull(data['UF_PHONE_INNER'])
			# print(user_count,user,id,workposit)

			js[inner_phone] = {
				'id': id,
				'name': user,
				'email':data['EMAIL'],
				'department': workdepartment,
				'position': workposit,
				'inner_phone': inner_phone,
				'is_active': data['ACTIVE']
			}

			user_count = user_count + 1

			with open('data/json/btrx_data/inner_phone_users.json','w',encoding='utf-8') as f:
					json.dump(js,f,indent=4,ensure_ascii=False)

		with open('data/json/btrx_data/inner_phone_users.json','r',encoding='utf-8') as f:
			userdata =json.loads(f.read())

		for i,user in enumerate(userdata):
			if user != None:
				co = i
				# print(userdata[user])
		print(f"Всего пользователей: {i+1}")
	else:
		users =	get_users_with_innerPhone(btrx)
		with open('data/json/btrx_data/companyusers.json','w',encoding='utf-8') as f:
			json_data = json.dumps(users,ensure_ascii=False,indent=4)
			f.write(json_data)

def seeallinnerphone():
	clear()
	if os.path.exists('data/json/btrx_data/inner_phone_users.json'):
		with open('data/json/btrx_data/inner_phone_users.json','r',encoding='utf-8') as f:
			json_data = json.loads(f.read())
		for data in json_data:
			if json_data[data]['inner_phone'] is not None:
				print(f"innerphone: {json_data[data]['inner_phone']}, id: {json_data[data]['id']}, name: {json_data[data]['name']}")

def seealluser():
	clear()
	if os.path.exists('data/json/btrx_data/inner_phone_users.json'):
		with open('data/json/btrx_data/inner_phone_users.json','r',encoding='utf-8') as f:
			json_data = json.loads(f.read())
		for data in json_data:
			print(f"name: {json_data[data]['name']}, id: {json_data[data]['id']}, innerphone: {json_data[data]['inner_phone']}, user active?: {json_data[data]['is_active']}")

def seeallactiveuser():
	clear()
	if os.path.exists('data/json/btrx_data/inner_phone_users.json'):
		with open('data/json/btrx_data/inner_phone_users.json','r',encoding='utf-8') as f:
			json_data = json.loads(f.read())
		for data in json_data:
			if json_data[data]['is_active'] == True:
				print(f"name: {json_data[data]['name']}, id: {json_data[data]['id']}, innerphone: {json_data[data]['inner_phone']}, user active?: {json_data[data]['is_active']}")

def seeallnotactiveuser():
	clear()
	if os.path.exists('data/json/btrx_data/inner_phone_users.json'):
		with open('data/json/btrx_data/inner_phone_users.json','r',encoding='utf-8') as f:
			json_data = json.loads(f.read())
		for data in json_data:
			if json_data[data]['is_active'] == False:
				print(f"name: {json_data[data]['name']}, id: {json_data[data]['id']}, innerphone: {json_data[data]['inner_phone']}, user active?: {json_data[data]['is_active']}")

def load_users_from_btrx(b):
	users = []
	try:
		users = b.get_all('user.get',{
			'select': ['ID','ACTIVE','NAME','LAST_NAME','EMAIL','UF_DEPARTMENT','WORK_POSITION','UF_PHONE_INNER']
		})
		with open('data/json/btrx_data/companyusers.json','w',encoding='utf-8') as f:
			json_data = json.dumps(users,ensure_ascii=False,indent=4,sort_keys=True)
			f.write(json_data)
		print('Сохранено в data/json/btrx_data/companyusers.json')

		workwithdata()
		# menu()
	except Exception as e:
		print(f"load_users_from_btrx {e}")
		users = b.get_all('user.get',{
			'select': ['ID','ACTIVE','NAME','LAST_NAME','EMAIL','UF_DEPARTMENT','WORK_POSITION','UF_PHONE_INNER']
		})
		with open('data/json/btrx_data/companyusers.json','w',encoding='utf-8') as f:
			json_data = json.dumps(users,ensure_ascii=False,indent=4,sort_keys=True)
			f.write(json_data)
		print('succes')
		# raise TypeError('get_users_with_innerPhone error')


def print_menu():

	print('1) Весь список пользователей.')
	print('2) Cписок активных пользователей.')
	print('3) Cписок не активных пользователей.')
	print('4) В меню поиска по конкретным данным ->')
	print('5) Список занятых внутренних номеров.')
	print('6) Выгрузить пользователей из Битрикс24 заново (чето не работает).')
	print('0) Выход.')

def print_searchmenu():
	print('1) Поиск по ID.')
	print('2) Поиск по Имени.')
	print('3) Поиск по Фамилии.')
	print('4) Поиск по Внутреннему телефону.')
	print('5) Поиск по Должности.')
	print('6) Поиск по Отделу.')
	print('#) Поиск по Номеру телефона.')
	print('9) Назад.')
	print('0) Выход.')

def search_menu():
	while True:
		print_searchmenu()
		select_opt = int(input('Select optiopn: ').strip())
		if select_opt == 1:
			pass
		elif select_opt == 9:
			menu()

def menu():
	global loop_while
	check = 0
	loop_while = False
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
		elif select_opt == 0:
			print('Выход')
			break
		else:
			print('input correct num')


if __name__ == "__main__":
	load_users_from_btrx(btrx)
	# seeallactiveuser()
	menu()