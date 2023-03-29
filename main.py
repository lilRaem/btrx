import json
import os
from time import time
from colorama import Fore
from main_search import search
"""
#TODO Был изменен поиск в parserhtml.py, есть ошибки, надо  исправить
- [?] parser.html: Начал брать цену в зависимости от наличия перечеркнутой (старой) цены
"""

"""
File "g:\Web-Develop\projects\my\python_project\btrx\module\parsersearchsite.py", line 46, in getProgramUrl
    raise TypeError(f"price type == int, now: {type(price)}")
TypeError: price type == int, now: <class 'NoneType'>
"""

datalist = []
clear = lambda: os.system('cls')

def main():
	"""
	search time for "Онко" with price = 0:
	before: ~ 1 min
	after: ???
	"""
	return search("онкология",9800,"НМО",mail_service="mindbox")

if __name__ == "__main__":
	clear()
	start = time()
	data: list[dict[str,str|int|None]] = main()

	# Берем ссылки НМО
	list_data = list()
	for link_data in data:

		with open(f"{os.getcwd()}\\data\\json\\docx_converted\\nmofile\\program_{link_data.get('type_zdrav')}.json",'r',encoding="utf-8") as nmo_file:
			nmo_data: list[dict[str,str|int|None]] = json.loads(nmo_file.read())
		if link_data.get("spec") == "Повышение квалификации (НМО)":
			for i,nmo_d in enumerate(nmo_data):
				# final_data =a
				# print(i,f"price {nmo_d.get('price')}")
				nmo_price = int(nmo_d.get('price').strip())
				nmo_hour = int(nmo_d.get('hour'.strip()))

				if nmo_d.get('title_program').lower() == link_data.get('name').lower():
					if int(link_data.get('price')) == nmo_price and link_data.get('price') and int(link_data.get('hour')) == nmo_hour:
						if not link_data.get('linkNmo'): link_data['linkNmo'] = nmo_d.get('linkNmo')
						if not link_data.get('nmoSpec'): link_data['nmoSpec'] = nmo_d.get('title_spec').strip()
			list_data.append(link_data)

			print(f"\n{link_data}")



	if data != None:
		with open("data.json","w", encoding="utf-8") as file:
			x = json.dump(data,file,indent=4,ensure_ascii=False)

	# print(Fore.MAGENTA+f'Main time: {end} sec'+ Fore.RESET)


	end: float = round(time()-start,2)
	minute: float = None
	if end < 60.0:
		print(Fore.MAGENTA+f'Main time: {end} sec'+ Fore.RESET)
	elif end >= 60.0:
		minute = round(end/60.0,2)
		print(Fore.MAGENTA+f'Main time: {minute} min'+ Fore.RESET)
	else:
		hour = minute
		print(Fore.MAGENTA+f'Main time: {round(minute)} min'+ Fore.RESET)