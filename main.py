import json
import os
from time import time
from colorama import Fore
from main_search import search
from module.logger import init_logger
"""
#TODO Был изменен поиск в parserhtml.py, есть ошибки, надо  исправить
- [?] parser.html: Начал брать цену в зависимости от наличия перечеркнутой (старой) цены
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
	"""
	search time for "Онко" with price = 0:
	before: ~ 1 min
	after: ???
	"""
	#TODO не работает
	# return search("Инструктор-проводник по альпинизму и горному туризму",15000,"ПП",mail_service="sendsay")
	return search("Эндокринология",type_programm="ПП",search_price=49800,mail_service="mindbox")
	# return search("актуальные вопросы диагностики и лечения травм",5900,"ПК",mail_service="mindbox")

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
		print(Fore.MAGENTA+f'Main time: {round(minute)} min'+ Fore.RESET)