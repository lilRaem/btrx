from datetime import date
import json
import os
from re import T
from time import sleep

from colorama import Fore,Back,Style

from btrx import set_product_price
from parsersearchsite import searchInSite,getProgramUrl
temp_price = ""

def loadJsonfile():
	with open(f'{os.getcwd()}\\data\\json\\program_СПО.json','r',encoding='utf-8') as file:
		programNMP = json.load(file)
	today = date.today()
	cur_date = today.strftime("%d.%m.%Y")
	filename = f'{cur_date}_file.json'
	path = os.getcwd() + "\\data\\json\\btrx_data"
	with open(f"{path}\{filename}",'r',encoding='utf-8') as file:
		program = json.load(file)
	temper_list = []
	temper_json = {}
	prog_id = ''
	prog_name = ''
	prog_price = ''
	count_nmp = 0
	for i,prognmp in enumerate(programNMP):

		for a,prog in enumerate(program):

			prog_id = prog['ID']
			prog_name = prog['NAME']
			prog_price = prog['PRICE']
			# print(prognmp['title_program'])
			if prognmp['title_program'] == prog_name:

					temper_list.append({
						'id': prog_id,
						"title_spec": programNMP[i]['title_spec'].replace('\n',' '),
						"title_program": prog_name.strip(),
						"price": prog_price.replace('.00',''),
						"hour":programNMP[i]['hour'],
						"date": programNMP[i]['date'],
						'linkNmo': prognmp['linkNmo']
						}
					)


	# for i,prog in enumerate(programNMP):
	# 	tit_spec = prog['title_spec']
	# 	for it,progt in enumerate(programNMP):
	# 		tit_spect = progt['title_spec']

	# 		if  tit_spec == tit_spect:
	# 			temper_list.append({
	# 				"title_spec": progt['title_spec'],
	# 				"title_program": prog['title_program'],
	# 				"hour": prog['hour'],
	# 				"date": prog['date'],
	# 				'linkNmo': prog['linkNmo']
	# 				}
	# 			)

	# 			temper_json = {
	# 				"title_spec": tit_spec,
	# 				"programs":temper_list[sp]
	# 			}
	# 			sp = sp + 1
	# 		js.append(temper_json)

	with open(f'{os.getcwd()}\\data\\json\\tempetOPT_NMO.json','w',encoding='utf-8') as file:
		json.dump(temper_list,file,indent=4,ensure_ascii=False)


def print_menu():

	print('1) Поиск новой программы в битрикс.')
	print('2) Поиск новой программы в новом прайсе.')
	print('3) Поиск программы на сайте.')
	print('0) Выход.')


def funcfind(program,name,hour):
	global temp_price
	count_program = 0
	temp_id = ""
	for i,data in enumerate(program):
		if data['PROPERTY_213'] != None:
			if name.lower() in data['NAME'].lower() and hour in data['PROPERTY_213']['value']:
				print("\n"+Back.RESET + Fore.RESET + Style.DIM + Fore.BLACK + Back.LIGHTGREEN_EX +
				f'by name and hour: {data["ID"]}')
				temp_id = data["ID"]
				print(f"{data['NAME']} {data['PRICE'].replace('.00','')}\nhour: {data['PROPERTY_213']['value']}"+Style.RESET_ALL+"\n")
				count_program = count_program + 1
			elif name.lower() in data['NAME'].lower():
				print('by name: ',data['ID'])
				print(data['NAME'],data['PRICE'])
	if count_program == 1:
		print(f"\n======from new pricelist: {temp_price}=======")
		id = temp_id
		print(Back.LIGHTMAGENTA_EX)
		# price = input(Back.RESET + Fore.RESET + Style.DIM + Fore.BLACK + Back.LIGHTMAGENTA_EX +'\nPrice: ')
		set_product_price(id=id,price=temp_price)
	if count_program >= 2:
		id = input('id: ')
		price = temp_price
		set_product_price(id=id,price=price)

def funcfind_f(program,f,name,hour):
	global temp_price
	count_program = 0
	for i,data in enumerate(f):
		if name.lower() in f[i]['title_program'].lower() and str(hour) == str(f[i]['hour']):
			print("\n"+Back.RESET + Fore.RESET + Fore.BLACK + Back.LIGHTBLUE_EX +
				f'\nby name and hour: {f[i]["linkNmo"]}')
			print(f"{data['title_program']} {f[i]['price'].replace('.00','')}\n{f[i]['hour']}\n"+Style.RESET_ALL+"\n")
			temp_price = f[i]['price'].replace('.00','')
			count_program = count_program + 1
		if name.lower() in f[i]['title_program'].lower():
			count_program
			# print('by name: ',f[i]['linkNmo'])
			# print(f[i]['title_program'],f[i]['price'])
	if count_program == 1:
		funcfind(program,name,hour)
		insite = input("Искать страницу на сайте? (1 если да): ")
		if insite == '1':
			searchInSite(name)
			getProgramUrl(name)

va = 0
loop_while = False
def menu(f,program):
	global loop_while
	check = 0
	loop_while = False
	while not loop_while:
		sleep(1)
		print_menu()
		select_opt = input('Select optiopn: ').strip()
		if select_opt == '1':
			name = input('name: ')
			hour = input('hour: ')
			funcfind(program,name,hour)
		elif select_opt == '2':
			name = input('name: ')
			hour = input('hour: ')
			funcfind_f(program,f,name,hour)
		elif select_opt == '3':
			name = input('name: ')
			searchInSite(name)
			getProgramUrl(name)
		elif select_opt == '0':
			print('Выход')
			break

		else:
			print('input correct num')

def find():
	today = date.today()
	cur_date = today.strftime("%d.%m.%Y")
	filename = f'{cur_date}_file.json'
	path = os.getcwd() + "\\data\\json\\btrx_data"
	with open(f"{path}\{filename}",'r',encoding='utf-8') as file:
		program = json.load(file)
	with open(f'{os.getcwd()}\\data\\json\\docx.json','r',encoding='utf-8') as file:
		f = json.load(file)
	# tid = input('id: ')
	# name = input('name: ')
	# hour = input('hour: ')
	btn = True

	menu(f,program)



def main():
	loadJsonfile()
	find()
if __name__ == "__main__":
	main()