import requests
import json
from colorama import Fore,Back,Style

link = 'https://apkipp.ru'
import sys
sys.path.append('/')
try:
	import html_pars.parserhtml as phtml
except:
	import module.html_pars.parserhtml as phtml

product_id = 'empty'
product_spec = 'empty'
product_name = 'empty'
product_price = 'empty'
product_hour = 'empty'
product_linkNmo = 'empty'
product_url = 'empty'

def searchInSite(search_key='Онкология'):
	'''Поиск на сайте по слову и сохраяет результат в data/json/site_search.json'''
	global product_id,product_spec,\
	product_name,product_price,product_hour,\
	product_linkNmo,product_url

	url = f'{link}/api/v1/search/?search={search_key}'
	# 'https://apkipp.ru/poisk/?search={data}'
	headers = {
		'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
	}

	data = requests.get(url, headers=headers)
	jdata = data.json()
	dict = {}

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
		f'Всего на сайте ({link}) найдено: {count} программ. Фактически по точному содержанию слова {search_key} в программе: {count_word_programm}\n'
	)
	return count_word_programm

def getProgramUrl(search_key='Онкология',price='6400'):
	data_url = {}
	find_url_list = []
	with open('data/json/site_search.json', 'r', encoding='utf-8') as f:
		local_data = json.load(f)
	for k, v in enumerate(local_data):
		if search_key.lower() in v['name'].lower():
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
			print(f'Найдено {count_find_url} страниц с названием: {search_key}')
			el_c = 0
			for i,data in enumerate(find_url_list):
				if search_key.lower() in data['name'].lower():
					if price == data['price']:
						el_c = el_c + 1
						if el_c == 1:
							print(f'Найдено {el_c} страниц:\n{find_url_list[i]["name"]}|{find_url_list[i]["hour"]}|{find_url_list[i]["price"]}')
							return find_url_list[i]
						else:
							print(f'Найдено {el_c} страниц:\n{find_url_list}')
				else:
					print(f'Найденно {el_c} страниц:\n{find_url_list}')
	else:
		print('Url not found')
if __name__ == "__main__":

	searchInSite('Нейрохирургия')
	print(getProgramUrl('Нейрохирургия','2900'))