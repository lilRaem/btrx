import os
from time import time
from colorama import Fore
from main_search import search
"""
#TODO Был изменен поиск в parserhtml.py, есть ошибки, надо  исправить
[ ] parser.html: Начал брать цену в зависимости от наличия перечеркнутой (старой) цены
"""

datalist = []
clear = lambda: os.system('cls')

def main():
	search("Фармацевтическая химия и фармакогнозия","")

if __name__ == "__main__":
	clear()
	start = time()
	main()
	print(Fore.MAGENTA+f'Main time: {round(time()-start,2)} sec'+ Fore.RESET)
