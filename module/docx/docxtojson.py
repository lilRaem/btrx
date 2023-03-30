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
	filename = 'Квалификационные возможности среднего мед пресонала и пути их изменения.docx'
	document = Document(filename)
	data = {}
	tables = []
	for table in document.tables:
		df = [['' for i in range(len(table.columns))] for j in range(len(table.rows))]
		for i, row in enumerate(table.rows):
			for j, cell in enumerate(row.cells):
				if cell.text:
					df[i][j] = cell.text
		tables.append(df)

	f = []
	for i,row in enumerate(tables[0]):
		main = Data()
		main.spec = tables[0][i][1]
		main.job = tables[0][i][2:-1][0].split("\n")
		main.pp = tables[0][i][-1].split("\n")
		f.append(main.dict())
	return f


if __name__ == "__main__":
	f = main()
	p =f'{os.getcwd()}'
	os.chdir(p)
	with open(f"{p}\\data\\json\\docx_converted\\docxtojson.json",'w',encoding='utf-8') as file:
		json.dump(f[1:],file,ensure_ascii=False,indent=4)