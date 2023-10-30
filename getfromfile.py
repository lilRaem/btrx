import json
from main_search import search


def main():
	data = None
	with open("parse_data.json",'r',encoding="utf-8") as f:
		data: dict[str,str] = json.loads(f.read())
	data_list = list()
	if data:
		for el in data:
			search_data = search(el.capitalize(),39600)
			if search_data:
				if search_data.__len__() == 1:
					data_list.append(search_data[0])
			print(el)
		with open("parse.json",'w',encoding="utf-8") as ff:
			json.dumps(data_list,indent=4,ensure_ascii=False)
	else:
		return None


if __name__ == "__main__":
	main()