import os
import time
import json
from module.config import FinalData
from colorama import Fore, Back, Style
from datetime import date
from pydantic import BaseModel, validator , StrictStr ,Field
from typing import Optional
from module.btrx import (get_all_data, check_product, get_product_list,load_from_jsonFile, save_to_json)
from module.build_btrx_data import buildjsondata
from module.parsersearchsite import searchInSite, getProgramUrl
'''
TODO что необходимо во время работы
[+] подставлять id товара автоматически
[-] Поиск товара автоматически
[-] Добавить колличество программ в название файла
[+] Во временно tmpfile.json ищет по словам которых по факту в программе нет (теперь все работает)
[+] поиск по словам и цене работает не корректно
[+] сделать списки более универсальными (чтобы была ссылка нмо и id)
[-] скопировать таблицы из pdf (https://medium.com/@winston.smith.spb/python-an-easy-way-to-extract-data-from-pdf-tables-c8de22308341,
https://github.com/jsvine/pdfplumber)
[+] Создание многоуровнего json: https://stackoverflow.com/a/49957442

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

TODO Интересные ссылки
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
	filenameWcurDate = f"{path}\\{filename}"
	return str(filenameWcurDate), str(filename)


datalist = []

def main(search_name='Ультразвуковая диагностика', search_price='99000'):
	start = time.time()
	search_name = search_name.strip()
	search_name = search_name.replace('\n', '')
	search_name = search_name.replace('  ', ' ')
	# name = input('Введите название программы: ')
	path = os.getcwd() + "\\data\\json\\btrx_data"
	final_data = FinalData()
	print(Fore.YELLOW + 'Path exists?: ', os.path.exists(makefileWdateName()[0]),
		makefileWdateName()[0] + Back.RESET)
	if (os.path.exists(makefileWdateName()[0])):
		data = load_from_jsonFile(makefileWdateName()[0], path)
		check_data = check_product(search_name, search_price, get_all_data(data))
		json_check_data=json.loads(check_data)
		searchInSite(search_name)
		count_check_data = 0
		if check_data != None:
			for chck_data in json_check_data:
				count_check_data = count_check_data + 1
		else:
			print('item not exist')
		if check_data != None and count_check_data == 1:
			progUrl_data = getProgramUrl(search_name, search_price)
			final_data.id = json_check_data['id']
			final_data.name = json_check_data['name']
			final_data.price = json_check_data['price']
			final_data.hour = json_check_data['hour']
			final_data.linkNmo = json_check_data['linkNmo']
			final_data.url = progUrl_data['url']
			print("\n" + Fore.GREEN + f'{final_data.json(encoder="utf-8",ensure_ascii=False)}')

		else:
			if check_data != None:
				final_data.id = json_check_data['id']
				final_data.name = json_check_data['name']
				final_data.price = json_check_data['price']
				final_data.linkNmo = json_check_data['linkNmo']
				progUrl_data = getProgramUrl(json_check_data['name'], json_check_data['price'])
				json_progUrl_data = json.loads(progUrl_data)
				final_data.url = json_progUrl_data['url']
				try:
					final_data.hour = json_check_data['hour']
				except:
					final_data.hour = json_progUrl_data['hour']
				print("\n" + Fore.GREEN + f'{final_data.json(encoder="utf-8",ensure_ascii=False)}' + Fore.RESET)
	else:
		save_to_json(get_product_list(), makefileWdateName()[1], path)
		data = load_from_jsonFile(makefileWdateName()[0], path)
		check_product(search_name, final_data.price, get_all_data(data))
	print('\n'+Fore.MAGENTA+f"(main.py) Search time: {time.time()-start} sec"+ Fore.RESET)

if __name__ == "__main__":
	start = time.time()
	main()
	print(Fore.MAGENTA+f'Main time: {time.time()-start} sec'+ Fore.RESET)
	# buildjsondata()
	# print(datalist)d:\Program\Microsoft VS Code\resources\app\out\vs\code\electron-sandbox\workbench\workbench.html

	# class DataData(BaseModel):
	# 	id: Optional[StrictStr] = None
	# data_data = DataData()
	# id = data_data.id
	# id = 'ss'
	# print(data_data)
