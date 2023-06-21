import json
import os
from time import sleep
from docx.api import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT

filename = 'docForparse\\Квалификационные возможности врачей и провизоров и пути их изменения 2023.docx'
document = Document(filename)
table = document.tables[0]
data = []
keys = None
rels = document.part.rels

table.columns[0].cells[0].text = 'title_spec'
table.columns[1].cells[0].text = 'title_program'
table.columns[2].cells[0].text = 'hour'
table.columns[3].cells[0].text = 'price'
table.columns[4].cells[0].text = 'date'
table.columns[5].cells[0].text = 'linkNmo'

"""
# Second step:
Use to extract data from docx table to json

TODO make rebuild this model for extract automaticaly all tables and data
- [ ] extract all tables to json
- [ ] automatic remove hyperlinks

"""

def iter_hyperlink_rels(rels):
	link_c = 0
	for rel in rels:
		if rels[rel].reltype == RT.HYPERLINK:
			rels[rel]._target
			link_c = link_c + 1
	# print(f'links {link_c}')


def main():
	iter_hyperlink_rels(rels)
	items = 0
	col_title = 0
	for i, col in enumerate(table.rows):
		for cell in col.cells:
			new_text = cell.text
			rep_text = new_text.split()
			rep_text = new_text.replace('\n', '')
			# if rep_text == 'Основная специальность(дополнительные специальности)' or rep_text == 'Основная специальность (дополнительные специальности)':
			# 	cell.text = 'title_spec'
			# if rep_text == 'Название программы':
			# 	cell.text = 'title_programm'
			# if rep_text == 'Трудоемкость, ЗЕТ':
			# 	cell.text = 'hour'
			# if rep_text == 'Стоимость обучения':
			# 	cell.text = 'price'
			# if rep_text == 'Дата утв' or rep_text == 'Датаутв':
			# 	cell.text = 'date'
			# if rep_text == 'Ссылка на курс' or rep_text == 'Ссылка накурс' or rep_text == 'Ссылка на курс ' or rep_text == 'Ссылка на курс\n':
			# 	rep_text.text = 'link'
		col_title = col_title + 1

	for i, row in enumerate(table.rows):
		text = (cell.text.replace('\n', ' ').strip() for cell in row.cells)
		# Establish the mapping based on the first row
		# headers; these will become the keys of our dictionary
		if i == 0:
			keys = tuple(text)
			continue
		# Construct a dictionary for this row, mapping
		# keys to values for this row
		row_data = dict(zip(keys, text))
		data.append(row_data)
		items = i
	print(f'items {items}')
	try:
		with open(f'{os.getcwd()}\\data\\json\\docx.json', 'w', encoding='utf-8') as file:
			doc = json.dumps(data, ensure_ascii=False, indent=4)
			file.write(doc)
			document.save(filename)
	except:
		os.mkdir(f'{os.getcwd()}\\data\\json\\')
		with open(f'{os.getcwd()}\\data\\json\\docx.json', 'w', encoding='utf-8') as file:
			doc = json.dumps(data, ensure_ascii=False, indent=4)
			file.write(doc)
			document.save(filename)


if __name__ == "__main__":
	main()