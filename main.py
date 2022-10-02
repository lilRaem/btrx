import os
from unicodedata import name
from colorama import Fore,Back,Style
from datetime import date

from module.btrx import (get_all_data, check_product, get_product_list, load_from_jsonFile, save_to_json)
from module.build_btrx_data import buildjsondata
from module.parsersearchsite import searchInSite, getProgramUrl
'''
TODO что необходимо во время работы
[+] подставлять id товара автоматически
[-] Поиск товара автоматически
[-] Добавить колличество программ в название файла
[+] Во временно tmpfile.json ищет по словам которых по факту в программе нет (теперь все работает)
[-] Добавить порядковые цифры к выводу по словам и слову
[+] поиск по словам и цене работает не корректно
[+] сделать списки более универсальными (чтобы была ссылка нмо и id)
[-] скопировать таблицы из pdf (https://medium.com/@winston.smith.spb/python-an-easy-way-to-extract-data-from-pdf-tables-c8de22308341,
https://github.com/jsvine/pdfplumber)
[-] Создание многоуровнего json: https://stackoverflow.com/a/49957442

TODO Что нужно сделать:

Разбросать важные функции по отдельным модулям python (отдельно выгрузка с битрикс, отдельно генератор шаблона, отдельно поиск и сравнение элементов)
Отдельным файлом:

[+] выгрузка с битрикс
[-] генератор шаблона
[-] поиск и сравнение c таблицами
[-] поиск по файлу tmpfile.json (на дынный момент разбивает на отдельные слова и ищет по ним,
	сохраняет в tmpfile.json) btrx.py check_product(*,*,*) line 145
[+] производить поиск по сайту через python

TODO Сделать тесты:
[-] main.py
[-] parserdocx.py
[+] btrx.py (можно доработать очень маленькое покрытие)
[-] parserdocx2table.py
[-]	parserhtml.py

TODO Что минимально нужно чтобы получить id товара?
[+] Имя программы, цена
'''


def makefileWdateName() -> str:
	"""
	[0] = str(fileNameWithPath)
	[1] = str(filename)

	Returns:
		tuple: [fileNameWithPath,filename]
	"""
	today = date.today()
	cur_date = today.strftime("%d.%m.%Y")
	filename = f'{cur_date}_file.json'
	path = os.getcwd() + "\\data\\json\\btrx_data"
	filenameWcurDate = f"{path}\{filename}"
	return str(filenameWcurDate), str(filename)


datalist = []

def main(search_name = 'Тренер-преподаватель по корэшу',
		search_price = '15000'):

	search_name = search_name.strip()
	search_name = search_name.replace('\n','')
	search_name = search_name.replace('  ',' ')
	# name = input('Введите название программы: ')
	path = os.getcwd() + "\\data\\json\\btrx_data"

	print(Fore.YELLOW+'Path exists?: ', os.path.exists(makefileWdateName()[0]), makefileWdateName()[0]+Back.RESET)
	if (os.path.exists(makefileWdateName()[0])):
		data = load_from_jsonFile(makefileWdateName()[0], path)
		check_data = check_product(search_name, search_price, get_all_data(data,datalist))
		searchInSite(search_name)
		if check_data != None:
			progUrl_data = getProgramUrl(search_name,search_price)
			id = check_data['id']
			if id == None or id == '':
				id = None
			name = check_data['name']
			if name == None or name == '':
				name = None
			price = check_data['price']
			if price == None or price == '':
				price = None
			hour = check_data['hour']
			if hour == None or hour == '':
				hour = None
			linkNmo = check_data['linkNmo']
			if linkNmo == None or linkNmo == '':
				linkNmo = None
			url = progUrl_data['url']
			if url == None or url == '':
				url = None
			d_dict = {
				'id': id,
				'name': name,
				'price': price,
				'hour': hour,
				'linkNmo': linkNmo,
				'url': url
			}
			print("\n"+Fore.GREEN+f'{d_dict}')
	else:
		save_to_json(get_product_list(),makefileWdateName()[1],path)
		data = load_from_jsonFile(makefileWdateName()[0], path)
		check_product(name, price,
			get_all_data(data, datalist))


if __name__ == "__main__":
	# main()

	buildjsondata()
	# print(datalist)d:\Program\Microsoft VS Code\resources\app\out\vs\code\electron-sandbox\workbench\workbench.html