import json
import os
from time import time
from colorama import Fore
from main_search import search
from module.logger import init_logger
"""
#TODO Был изменен поиск в parserhtml.py, есть ошибки, надо  исправить
- [?] parser.html: Начал брать цену в зависимости от наличия перечеркнутой (старой) цены
- [ ] добавить нормальный логгер как в music_bot
"""

"""
File "g:\\Web-Develop\\projects\\my\\python_project\\btrx\\module\\parsersearchsite.py", line 46, in getProgramUrl
    raise TypeError(f"price type == int, now: {type(price)}")
TypeError: price type == int, now: <class 'NoneType'>
"""

datalist = []
clear = lambda: os.system('cls')
init_logger('btrx',"main")
def main():
	with open("docForparse\\sudeksp.json","r",encoding="utf-8") as file:
		lis_pro = json.loads(file.read())
		# print(lis_pro)
	prog_array = list()
	for elem in lis_pro[1:]:
		prog = elem["program"]
		prog_array.append(prog.replace("\n"," "))
	# print(prog_array)
	return search("эластограф",type_programm="НМО",search_price=0,mail_service="mindbox")

if __name__ == "__main__":
	clear()
	start = time()
	data: list[dict[str,str|int|None]] = main()

	if data != None:
		with open("data.json","w", encoding="utf-8") as file:
			json.dump(data,file,indent=4,ensure_ascii=False)

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
		print(Fore.MAGENTA+f'Main time: {round(hour)} hour'+ Fore.RESET)