import requests
import json

from module.html.parserhtml import parseSiteUrl

link = 'https://apkipp.ru'


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
		f'Всего на сайте({link}) найдено: {count} программ. Фактически по точному содержанию слова в программе: {count_word_programm}'
	)


def getProgramUrl(search_key='Онкология',price='2600'):
	find_url_list = []
	with open('data/json/site_search.json', 'r', encoding='utf-8') as f:
		local_data = json.load(f)

	for k, v in enumerate(local_data):
		if search_key.lower() in local_data[k]['name'].lower():
			# print('\n' + f"{local_data[k]['name']}\n{k+1} {link}{local_data[k]['url']}")
			program_url = local_data[k]['url']
			find_url_list.append(f'{k+1} ' + link + program_url)
			main_url = link + program_url
			parseSiteUrl(main_url,price)