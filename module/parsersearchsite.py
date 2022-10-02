import requests
import json
from colorama import Fore,Back,Style

link = 'https://apkipp.ru'

import html_pars.parserhtml as phtml

def searchInSite(search_key='Онкология'):
	'''Поиск на сайте по слову и сохраяет результат в data/json/site_search.json'''
	url = f'{link}/api/v1/search/?search={search_key}'
	# 'https://apkipp.ru/poisk/?search={data}'
	headers = {
		'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
	}

	param = {"course_list": ''}
	a = 0
	data = requests.get(url, headers=headers)
	jdata = data.json()
	dict = []

	with open('data/json/site_search.json', 'w', encoding='utf-8') as f:
		d = json.dumps(jdata['course_list'], ensure_ascii=False, indent=4)
		f.write(d)
	count = 0
	count_word_programm = 0
	for k in jdata['course_list']:
		if search_key.lower() in k['name'].lower():
			count_word_programm = count_word_programm + 1
		count = count + 1
	print(
		f'Всего на сайте ({link}) найдено: {count} программ. Фактически по точному содержанию слова в программе: {count_word_programm}\n'
	)
	return count_word_programm

def getProgramUrl(search_key='Онкология',price='6400'):
	data_url = {}
	find_url_list = []
	with open('data/json/site_search.json', 'r', encoding='utf-8') as f:
		local_data = json.load(f)
	for k, v in enumerate(local_data):
		search_key = search_key.lower()
		if search_key in v['name'].lower():
			program_url = v['url']
			main_url = link + program_url
			pSiteUrl = phtml.parseSiteUrl(main_url,price)
			if pSiteUrl != None:
				find_url_list.append(pSiteUrl)
				# print(Fore.GREEN+f'{pSiteUrl}'+Style.RESET_ALL)
			else:
				# find_url_list.append(pSiteUrl)
				print(f"{Fore.LIGHTWHITE_EX+v['name']+' '+Fore.RESET+Fore.LIGHTBLACK_EX}\n[{str(k+1)}] {link}{v['url']}"+Fore.RESET)
	if find_url_list != []:
		count_find_url = 0
		for data in find_url_list:
			count_find_url = count_find_url + 1
		if count_find_url == 1:
			return find_url_list[0]
		else:
			print(f'Найденно {count_find_url} страниц:\n{find_url_list}')
	else:
		print('Url not found')
if __name__ == "__main__":
	getProgramUrl()