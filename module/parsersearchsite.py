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
from module.logger import logging
parse_site_config = ParseSiteConfig()

log = logging.getLogger("btrx.module.parsersearchsite")

def searchInSite(search_key: str = 'Онкология') -> tuple[int,list[dict]]:
	'''Поиск на сайте по слову и сохраяет результат в data/json/site_search.json'''
	url = parse_site_config.get_ApiUrl(search_key)
	# 'https://company.ru/poisk/?search={data}'
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
	log.info(
		f'Всего на сайте ({parse_site_config.link}) найдено: {count} программ. Фактически по точному содержанию слова "{search_key}" в программе: {count_word_programm}'
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
				if data_psiteurl.get('price') == price:
					log.info(Fore.GREEN+f' {data["name"]} {data_psiteurl["hour"]} {data_psiteurl["price"]}\n{data_psiteurl["url"]} '+Fore.RESET)
	if find_url_list:
		if find_url_list.__len__() == 1:
			log.info(f"Find one LINK: {find_url_list[0]}")
		else:
			log.info(f'1. Найдено {find_url_list.__len__()} страниц с названием: {search_key}')
			for data in find_url_list:
				if search_key.lower() in data.get("name").lower():
					if data.get("price"):
						if price == int(data.get("price")):
							log.debug(f"By search price: {price} and in find price: {int(data.get('price'))}\n{data}")

	else:
		log.warning('Url not found')
	try:
		if find_url_list:
			if find_url_list.__len__() == 1:
				for data in find_url_list:
						if search_key.lower() in data.get("name").lower():
							if data.get("price"):
								if price == int(data.get("price")):
									log.info(f'3. Найдена {find_url_list.__len__()} страница:\n{data.get("name")}|{data.get("hour")}|{data.get("price")}')
									log.debug(f"parsersearchsite find list: {find_url_list}")
									return find_url_list
			else:
				for data in find_url_list:
						if search_key.lower() in data.get("name").lower():
							if data.get("price"):
								if price == int(data.get("price")):
									if find_url_list.__len__() < 7:
										log.info(f'4. Найдено {find_url_list.__len__()} страниц:\n{find_url_list}')
									return find_url_list
	except Exception as e:
		log.exception(e)
	log.debug("\nReturn without parsed data")
	return find_url_list

if __name__ == "__main__":
	getProgramUrl(search_key="Современные аспекты акушерской помощи в родовспомогательных учреждениях",price=9792)