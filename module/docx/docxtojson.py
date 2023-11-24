import json
import os
from docx import Document
import pandas as pd
from pydantic import BaseModel,StrictInt,StrictStr
from typing import Optional

"""
# TODO Docx to json
Extract tables form docx
"""


class Data(BaseModel):
	spec: Optional[StrictStr] = None
	job: Optional[list] = None
	pp: Optional[list] = None

def main():
	global name
	path="docForparse"
	name="Перечень экспертных специальностей, по которым предоставляется право самостоятельного производства судебных экспертиз"
	filename = f'{path}\\{name}.docx'
	document = Document(filename)
	data = {}
	tables = []
	for table in document.tables:
		print(table)
		if table:
			print(table.rows[0])
			df = [['' for i in range(len(table.columns))] for j in range(len(table.rows))]
			for i, row in enumerate(table.rows):
				for j, cell in enumerate(row.cells):
					if cell.text:
						df[i][j] = cell.text
		tables.append(df)

	f = []
	for i,row in enumerate(tables[0]):
		print(i,row)
		main = Data()
		# main.spec = tables[0][i][0].strip().split(";")
		# main.job = tables[0][i][1].strip().replace(" \n","").replace("\n","").strip().split(";")
		# if tables[0][i][2].strip().replace("\n","").strip().split(";") != "" or tables[0][i][2].strip().replace("\n","").strip().split(";") != None:
		# 	main.pp = tables[0][i][2].strip().replace(" \n","").replace("\n","").strip().split(";")
		pp_list=list()
		# for d in main.pp:
		# 	if d != "":
		# 		pp_list.append(d.strip())
		# main.pp = pp_list
		f.append(main.dict())

	return f


if __name__ == "__main__":
	li = main()
	p =f'{os.getcwd()}'
	os.chdir(p)
	with open(f"{p}\\data\\json\\docx_converted\\{name}.json",'w',encoding='utf-8') as file:
		json.dump(li[1:],file,ensure_ascii=False,indent=4)