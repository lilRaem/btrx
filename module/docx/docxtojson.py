import json
from docx import Document
import pandas as pd

filename = 'АПК и ПП программы ПК НМО.docx'
document = Document(filename)
data = {}
tables = []
for table in document.tables[:2]:
    df = [['' for i in range(len(table.columns))] for j in range(len(table.rows))]
    for i, row in enumerate(table.rows):
        for j, cell in enumerate(row.cells):
            if cell.text:
                df[i][j] = cell.text
    tables.append(pd.DataFrame(df))
print(tables)

# with open('docxtojson.json','w',encoding='utf-8') as file:
# 	json.dump(tables,file,ensure_ascii=False)