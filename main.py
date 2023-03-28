import json
import os
from time import time
from colorama import Fore
from main_search import search
"""
#TODO Был изменен поиск в parserhtml.py, есть ошибки, надо  исправить
- [ ] parser.html: Начал брать цену в зависимости от наличия перечеркнутой (старой) цены
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
	return search("Лечебная физкультура",20000,"ПП",mail_service="mindbox")

if __name__ == "__main__":
	clear()
	start = time()
	data: list[dict[str,str|int|None]] = main()
	minute: float = None
	if data != None:
		with open("data.json","w", encoding="utf-8") as file:
			x = json.dump(data,file,indent=4,ensure_ascii=False)
	end: float = round(time()-start,2)
	# print(Fore.MAGENTA+f'Main time: {end} sec'+ Fore.RESET)
	if end < 60.0:
		print(Fore.MAGENTA+f'Main time: {end} sec'+ Fore.RESET)
	elif end >= 60.0:
		minute = round(end/60.0,2)
		print(Fore.MAGENTA+f'Main time: {minute} min'+ Fore.RESET)
	else:
		hour = minute
		print(Fore.MAGENTA+f'Main time: {round(minute)} min'+ Fore.RESET)