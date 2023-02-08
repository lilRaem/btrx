from time import time
from typing import Optional
from pydantic import BaseModel,StrictStr
from colorama import Fore,Back,Style
try:
	from config import FinalData
except:
	from module import config
import requests
import json

try:
	import html_pars.parserhtml as phtml
except:
	import module.html_pars.parserhtml as phtml

link = 'https://apkipp.ru'

def searchInSite(search_key: str ='Онкология') -> int|list:
	'''Поиск на сайте по слову и сохраяет результат в data/json/site_search.json'''

	url = f'{link}/api/v1/search/?search={search_key}&as_phrase=true'
	# 'https://apkipp.ru/poisk/?search={data}'
	headers = {
		'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
	}

	data = requests.get(url, headers=headers)
	jdata = data.json()

	with open('data/json/site_search.json', 'w', encoding='utf-8') as f:
		json.dump(jdata['course_list'],f, ensure_ascii=False, indent=4)
	count = 0
	count_word_programm = 0
	item_list = []
	for k in jdata['course_list']:
		if search_key.lower() in k['name'].lower():
			item_list.append(k)
			count_word_programm = count_word_programm + 1
		count = count + 1
	print(
		f'Всего на сайте ({link}) найдено: {count} программ. Фактически по точному содержанию слова "{search_key}" в программе: {count_word_programm}\n'
	)
	return int(count_word_programm), list(item_list)

def getProgramUrl(search_key:str='Онкология',price: str ='6400') -> list:
	find_url_list = []
	start = time()
	if type(price) != str:
		raise TypeError(f"price type == str, now: {type(price)}")
	with open('data/json/site_search.json', 'r', encoding='utf-8') as f:
		local_data = json.load(f)
	for k, v in enumerate(local_data):
		try:
			final_data = config.FinalData()
		except:
			final_data = FinalData()
		final_data.name = v['name']
		final_data.price = price
		if search_key.lower() in final_data.name.lower():
			final_data.url = v['url']
			main_url = link + final_data.url
			pSiteUrl = phtml.parseSiteUrl(main_url,final_data.price)
			for data in pSiteUrl:
				find_url_list.append(data)
				# print(Fore.GREEN+f'{pSiteUrl}'+Style.RESET_ALL)
	if find_url_list != []:
		count_find_url = 0
		count_find_by_word = 0
		if count_find_url == 1:
			print(Fore.MAGENTA+f'(parsersearchsite.py|getProgramUrl(): count_find_url = 1) Search time: {round(time()-start,2)} sec' + Fore.RESET)
		else:
			for d in find_url_list:
				count_find_by_word = count_find_by_word + 1
			print(f'1. Найдено {count_find_by_word} страниц с названием: {search_key}')
			for i,data in enumerate(find_url_list):
				if search_key.lower() in data['name'].lower():
					count_find_url = count_find_url + 1
					if final_data.price == data['price']:
						print("\n"+Fore.CYAN+f'{find_url_list[i]}'+Fore.RESET)
						# count_find_url = count_find_url + 1
	else:
		print('Url not found')
	if count_find_url == 1 and count_find_url != None:
		for i,data in enumerate(find_url_list):
				if search_key.lower() in data['name'].lower():
					if price == data['price']:
						print(f'3. Найдена {count_find_url} страница:\n{data["name"]}|{data["hour"]}|{data["price"]}')
						return find_url_list
	else:
		print(f'4. Найдено {count_find_url} страниц:\n{find_url_list}')
		return find_url_list

if __name__ == "__main__":
	# for v in searchInSite('Онкология')[1]:
	# 	print(dict(v)['name'])
	getProgramUrl(search_key="Онкология",price="19600")