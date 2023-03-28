from time import time
from typing import Optional
from pydantic import BaseModel,StrictStr
from colorama import Fore,Back,Style
try:
	from config import FinalData, ParseSiteConfig
except:
	from module.config import FinalData, ParseSiteConfig
import requests
import json

try:
	import html_pars.parserhtml as phtml
except:
	import module.html_pars.parserhtml as phtml

parse_site_config = ParseSiteConfig()

def searchInSite(search_key: str = 'Онкология') -> tuple[int,list[dict]]:
	'''Поиск на сайте по слову и сохраяет результат в data/json/site_search.json'''
	url = parse_site_config.get_ApiUrl(search_key)
	# 'https://apkipp.ru/poisk/?search={data}'
	data = requests.get(url, headers=parse_site_config.get_headers())
	jdata: list[dict] = data.json()

	# with open('data/json/site_search.json', 'w', encoding='utf-8') as f:
	# 	json.dump(jdata['course_list'],f, ensure_ascii=False, indent=4)

	count = 0
	count_word_programm = 0
	item_list: list[dict] = list()
	for k in jdata['course_list']:
		if search_key.lower() in k['name'].lower():
			item_list.append(dict(k))
			count_word_programm = count_word_programm + 1
		count = count + 1
	print(
		f'Всего на сайте ({parse_site_config.link}) найдено: {count} программ. Фактически по точному содержанию слова "{search_key}" в программе: {count_word_programm}\n'
	)
	return count_word_programm, item_list

def getProgramUrl(search_key:str='Онкология',price: int = 9800) -> list[dict[str,str|int|None]]|None:
	find_url_list: list[dict[str,str|int|None]] = list()
	start = time()
	if type(price) != int:
		raise TypeError(f"price type == int, now: {type(price)}")
	for data in searchInSite(search_key)[1]:
		final_data = FinalData()

		if data.get("name"): final_data.name = data.get("name")
		final_data.price = price
		if search_key.lower() in final_data.name.lower():
			final_data.url = data.get("url")
			main_url = parse_site_config.link + final_data.url
			pSiteUrl = phtml.parseSiteUrl(main_url,final_data.price)
			for data_psiteurl in pSiteUrl:
				if data_psiteurl.get('spec'): final_data.spec = data.get('spec')
				find_url_list.append(data_psiteurl)
				if data_psiteurl.get('price') == price: print(Fore.GREEN+f'{data}'+Style.RESET_ALL)
	if find_url_list:
		if find_url_list.__len__() == 1:
			print(Fore.MAGENTA+f'(parsersearchsite.py|getProgramUrl(): count_find_url = 1) Search time: {round(time()-start,2)} sec' + Fore.RESET)
		else:
			print(f'1. Найдено {find_url_list.__len__()} страниц с названием: {search_key}')
			for data in find_url_list:
				if search_key.lower() in data.get("name").lower():
					if data.get("price"):
						if price == int(data.get("price")):
							print("\n"+Style.BRIGHT+Fore.LIGHTCYAN_EX+f'{data}'+Style.RESET_ALL)
						else:
							print("\n"+Fore.CYAN+f'{data}'+Fore.RESET)
	else:
		print('Url not found')
	try:
		if find_url_list:
			if find_url_list.__len__() == 1:
				for data in find_url_list:
						if search_key.lower() in data.get("name").lower():
							if data.get("price"):
								if price == int(data.get("price")):
									print(f'3. Найдена {find_url_list.__len__()} страница:\n{data.get("name")}|{data.get("hour")}|{data.get("price")}')
									return find_url_list
			else:
				for data in find_url_list:
						if search_key.lower() in data.get("name").lower():
							if data.get("price"):
								if price == int(data.get("price")):
									if find_url_list.__len__() < 5:
										print(f'4. Найдено {find_url_list.__len__()} страниц:\n{find_url_list}')
									return find_url_list
	except Exception as e:
		print(Fore.RED+e+Fore.RESET)
	print("\nReturn without parsed data")
	return find_url_list

if __name__ == "__main__":
	getProgramUrl(search_key="Онкология",price=19600)