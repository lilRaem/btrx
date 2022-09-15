from datetime import date
import json
import os




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
						"title_spec": prognmp['title_spec'].replace('\n',' '),
						"title_program": prognmp['title_program'],
						"price": prog_price.replace('.00',''),
						"hour": prognmp['hour'],
						"date": prognmp['date'],
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

def funcfind(program,name,hour):
	name = input('name: ')
	hour = input('hour: ')
	for i,data in enumerate(program):
		if data['PROPERTY_213'] != None:
			if name.lower() in data['NAME'].lower() and hour in data['PROPERTY_213']['value']:
				print(f'\nby name and hour: {data["ID"]}')
				print(f"{data['NAME']} {data['PRICE'].replace('.00','')}\n")
			elif name.lower() in data['NAME'].lower():
				print('by name: ',data['ID'])
				print(data['NAME'],data['PRICE'])
va = 0
def funcmenu():

	va = input('Выбор: ')

def find():
	today = date.today()
	cur_date = today.strftime("%d.%m.%Y")
	filename = f'{cur_date}_file.json'
	path = os.getcwd() + "\\data\\json\\btrx_data"
	with open(f"{path}\{filename}",'r',encoding='utf-8') as file:
		program = json.load(file)
	# with open(f'{os.getcwd()}\\data\\json\\program_СПО.json','r',encoding='utf-8') as file:
	# 	f = json.load(file)
	# tid = input('id: ')
	# name = input('name: ')
	# hour = input('hour: ')
	btn = True

	while True:

		if va != 2:
			funcmenu()
		if va == 1:
			funcfind(program)




def main():
	loadJsonfile()
	find()
if __name__ == "__main__":
	main()