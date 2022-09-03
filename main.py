import os
from unicodedata import name
from colorama import Fore,Back,Style
from datetime import date
from jinja2 import Environment, FileSystemLoader, Template

from module.btrx import (get_all_data, check_product, get_product_list, load_from_jsonFile, save_to_json)
from module.parsersearchsite import searchInSite, getProgramUrl
'''
TODO что необходимо во время работы
[-] подставлять id товара автоматически
[-] Поиск товара автоматически
[-] Добавить колличество программ в название файла
[+] Во временно tmpfile.json ищет по словам которых по факту в программе нет (теперь все работает)
[-] Добавить порядковые цифры к выводу по словам и слову
[+] поиск по словам и цене работает не корректно
[-] сделать списки более универсальными (чтобы была ссылка нмо и id)
[-] скопировать таблицы из pdf (https://medium.com/@winston.smith.spb/python-an-easy-way-to-extract-data-from-pdf-tables-c8de22308341,
https://github.com/jsvine/pdfplumber)

TODO Что нужно сделать:

Разбросать важные функции по отдельным модулям python (отдельно выгрузка с битрикс, отдельно генератор шаблона, отдельно поиск и сравнение элементов)
Отдельным файлом:

[+] выгрузка с битрикс
[-] генератор шаблона
[-] поиск и сравнение c таблицами
[-] поиск по файлу tmpfile.json (на дынный момент разбивает на отдельные слова и ищет по ним,
	сохраняет в tmpfile.json) btrx.py check_product(*,*,*) line 145
[-] производить поиск по сайту через python

TODO Сделать тесты:
[-] main.py
[-] parserdocx.py
[+] btrx.py (можно доработать очень маленькое покрытие)
[-] parserdocx2table.py
[-]	parserhtml.py

TODO Что минимально нужно чтобы получить id товара?

[+] Имя программы, цена
'''
today = date.today()
cur_date = today.strftime("%d.%m.%Y")
filename = f'{cur_date}_file.json'
path = os.getcwd() + "\\data\\json\\btrx_data"
datalist = []

def main():

	# name = input('Введите название программы: ')
	name = 'Биопсийная диагностика нейрохирургической патологии'
	price = '5800'
	print(Fore.YELLOW+'Path exists?: ', os.path.exists(f"{path}\{filename}"), f"{path}\{filename}"+Back.RESET)
	if (os.path.exists(f"{path}\{filename}")):
		data = load_from_jsonFile(f"{path}\{filename}", path)
		check_product(name, price, get_all_data(data,datalist))
		searchInSite(name)
		getProgramUrl(name)
	else:
		save_to_json(get_product_list(),filename,path)
		data = load_from_jsonFile(f"{path}\{filename}", path)
		check_product(name, price,
			get_all_data(data, datalist))


if __name__ == "__main__":
	main()
