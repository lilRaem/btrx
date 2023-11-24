import os,json
from main_search import search

with open("docForparse\\sudeksp.json","r",encoding="utf-8") as file:
	lis_pro = json.loads(file.read())
	# print(lis_pro)
	prog_array:list[str] = list()
	for elem in lis_pro[1:]:
		prog = elem["program"]
		prog_array.append(prog.replace("\n"," "))

	page_ = list()


	for prog_ in prog_array:
		print(prog_)
		search_pro = search(prog_.strip(),28000,mail_service="mindbox")
		if search_pro and search_pro.__len__() == 1:
			page_.append(search_pro[0])

	with open("new_js.json","w",encoding="utf-8") as fle:
		json.dump(page_,fle,ensure_ascii=False,indent=4)