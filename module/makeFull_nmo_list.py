import json
import os
from unicodedata import name




def loadJsonfile():
	with open(f'{os.getcwd()}\\data\\json\\program_СПО.json','r',encoding='utf-8') as file:
		programSPO = json.load(file)
	temper_json = {}
	temper_list = []
	js=[]
	count = 0
	tmp = {}
	i = 0
	sp = 0
	for k in programSPO:
		spec_c = 0
		tit_spec = k['title_spec']
		temper_list.append({
			"title_spec": programSPO[i]['title_spec'],
			"title_program": programSPO[i]['title_program'],
			"hour": programSPO[i]['hour'],
			"date": programSPO[i]['date'],
			'linkNmo': programSPO[i]['linkNmo']
			}
		)

		if  programSPO[spec_c]['title_spec'] == tit_spec :
			if tit_spec == programSPO[sp]['title_spec']:
				temper_json = {
					"title_spec": tit_spec,
					"programs":temper_list
				}
				spec_c = spec_c + 1
				sp = sp + 1
			js.append(temper_json)
			with open(f'{os.getcwd()}\\data\\json\\tempetOPT_NMO.json','w',encoding='utf-8') as file:
				json.dump(js,file,indent=4,ensure_ascii=False)
		i = i + 1
		count = count + 1
def main():
	loadJsonfile()

if __name__ == "__main__":
	main()