import os
from docx import Document
import pandas as pd
import csv, json

type_name = 'ВО'
filename = 'АПК и ПП программы ПК НМО.docx'

printed = False


def csv_to_json(csv_file, json_file):
	global printed
	jsonArray = []
	try:
		os.makedirs(f'{os.getcwd()}\\data\\json')
	except:
		if printed == False and not printed:
			print(f'Сохранено в: {json_file}')
			printed = True
	with open(csv_file, encoding='utf-8') as csvf:
		# print(f"\n{csvf}\n")
		csvReaader = csv.DictReader(csvf)
		for row in csvReaader:
			jsonArray.append(row)

		for k, v in enumerate(jsonArray):
			jsonArray.pop(k)
			# print(jsonArray)
		#convert python jsonArray to JSON String and write to file
		with open(json_file, 'w', encoding='utf-8') as jsonf:

			jsonString = json.dumps(jsonArray, ensure_ascii=False, indent=4)
			jsonf.write(jsonString)


def docx2csv(filename):
	global printed
	document = Document(filename)
	type_name = ''

	for index, table in enumerate(document.tables):
		df = [['' for i in range(len(table.columns))] for j in range(len(table.rows))]
		if index == 0:
			type_name = 'ВО'
			print(f'Current index:{index} type:{type_name}')
		elif index == 1:
			type_name = 'СПО'
			print(f'Current index:{index} type:{type_name}')
		elif index == 2:
			type_name = 'НМП'
			print(f'Current index:{index} type:{type_name}')
		else:
			type_name = 'none'
			print(f'Current index:{index} type:{type_name}')
		count_vo = 0
		count_spo = 0
		count_nmp = 0
		for i, row in enumerate(table.rows):

			for j, cell in enumerate(row.cells):
				df[i][j] = cell.text.replace('\n', ' ')
				df[i][j] = cell.text.strip()
				df[i][j] = cell.text.replace(',',';')
				df[i][j] = cell.text.strip()
			if index == 0:
				type_name = 'ВО'
				program_path = f"{os.getcwd()}\\data\\csv\\program_{type_name}.csv"

				try:
					os.makedirs(f'{os.getcwd()}\\data\\csv')
				except:
					if printed == False and not printed:
						print(f'Сохранено в: {program_path}')
						printed = True
				pd.DataFrame(df).to_csv(program_path, index=False, header=False)
				csv_to_json(program_path, f'{os.getcwd()}\\data\\json\\program_{type_name}.json')
				count_vo = count_vo + 1

			if index == 1:
				type_name = 'СПО'
				program_path = f"{os.getcwd()}\data\\csv\\program_{type_name}.csv"
				try:
					os.makedirs(f'{os.getcwd()}\\data\\csv')
				except:
					if printed == False and printed:
						print(f'Сохранено в: {program_path}')
						printed = True
				pd.DataFrame(df).to_csv(program_path, index=False, header=False)
				csv_to_json(program_path, f'{os.getcwd()}\data\\json\\program_{type_name}.json')
				count_spo = count_spo + 1
			if index == 2:
				type_name = 'НМП'
				program_path = f"{os.getcwd()}\data\\csv\\program_{type_name}.csv"
				try:
					os.makedirs(f'{os.getcwd()}\\data\\csv')
				except:
					if printed == False and printed:
						print(f'Сохранено в: {program_path}')
						printed = True
				pd.DataFrame(df).to_csv(program_path, index=False, header=False)
				csv_to_json(program_path, f'{os.getcwd()}\data\\json\\program_{type_name}.json')
				count_nmp = count_nmp + 1

		print(f"VO_items: {count_vo}, SPO_items: {count_spo}, NMP_items: {count_nmp}")
if __name__ == "__main__":
	docx2csv(filename)
	# os.makedirs(f'{os.getcwd()}\\data\\csv')