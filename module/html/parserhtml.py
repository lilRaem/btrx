from re import L
from time import sleep
import requests
from bs4 import BeautifulSoup
import os, json
from colorama import Fore,Back,Style

def bs4pars():
	with open(f"{os.getcwd()}/module/html/templates/source/pp_spo.html",'r',encoding='utf-8') as f:
		html = f.read()

	soup = BeautifulSoup(html,'lxml')
	pars_list = []
	pars_dict = {}
	# НМО старый шаблон
	# for el in soup.find_all(class_='text-block'):
	# 	# print("==={el.find('i','prog_altspecial').text}===")

	# 	if el.find('b','prog_special').text != '':
	# 		prog_special = el.find('b','prog_special').text.strip()
	# 	else:
	# 		prog_special = None
	# 	if el.find('i','prog_altspecial').text != '':
	# 		prog_altspecial = el.find('i','prog_altspecial').text.strip()
	# 		prog_altspecial = prog_altspecial.replace('\n','')
	# 		prog_altspecial = prog_altspecial.replace('\t','')
	# 	else:
	# 		prog_altspecial = None
	# 	if el.find('a','prog_title').text != '':
	# 		prog_title = el.find('a','prog_title').text.replace('\t','').replace('\n','')
	# 	else:
	# 		prog_title = None
	# 	if el.find('span').next_element != '':
	# 		prog_hour = el.find('span').next_element
	# 	else:
	# 		prog_hour = None
	# 	if el.find('span').next_element.next_element.next_element.next_element.text != '':
	# 		prog_price = el.find('span').next_element.next_element.next_element.next_element.text.replace('руб','').replace('\n','').replace('\t','').strip()
	# 	else:
	# 		prog_price = None

	# 	pars_dict = {
	# 		'prog_special': prog_special,
	# 		'prog_altspecial': prog_altspecial,
	# 		'prog_title': prog_title,
	# 		'prog_hour': prog_hour,
	# 		'prog_price': prog_price,
	# 		'url': el.find('a','prog_title').get('href')
	# 	}

	# 	pars_list.append(pars_dict)
	for el in soup.find_all(class_='courses-block'):
		print(el.find('p','headtext').text)
		if el.find('p','headtext').text != '':
			prog_special = el.find('p','headtext').text.strip()
		else:
			prog_special = None
		if el.find('p','subtext').text != '':
			prog_altspecial = el.find('p','subtext').text.strip()
			prog_altspecial = prog_altspecial.replace('\n','')
			prog_altspecial = prog_altspecial.replace('\t','')
		else:
			prog_altspecial = None
		if el.find('p','headtext').text != '':
			prog_title = el.find('p','headtext').text.replace('\t','').replace('\n','')
		else:
			prog_title = None
		if el.find('p','prog_hour').text != '':
			prog_hour = el.find('p','prog_hour').text.replace('часов','').replace('часа','').strip()
		else:
			prog_hour = None
		if el.find('p','prog_price').text != '':
			prog_price = el.find('p','prog_price').text.replace('руб.','').replace(' ','').strip()
		else:
			prog_price = None
		pars_dict = {
			'prog_title': prog_title,
			'prog_altspecial': prog_altspecial,
			'prog_hour': prog_hour,
			'prog_price': prog_price,
			'url': el.find('a','button').get('href')
		}
		pars_list.append(pars_dict)
	print(pars_list)
	with open(f'{os.getcwd()}/module/html/templates/data.json','w',encoding='utf-8') as fp:
		json.dump(pars_list,fp,ensure_ascii=False,indent=4)


def parseSiteUrl(url="https://apkipp.ru/katalog/zdravoohranenie-nemeditsinskie-spetsialnosti/kurs-sudebnyij-ekspert-ekspert-biohimik-ekspert-genetik-ekspert-himik/?program=%D0%A1%D1%83%D0%B4%D0%B5%D0%B1%D0%BD%D1%8B%D0%B9%20%D1%8D%D0%BA%D1%81%D0%BF%D0%B5%D1%80%D1%82&header=%D0%9A%D1%83%D1%80%D1%81%20%D0%9F%D0%9F%20%D0%A1%D1%83%D0%B4%D0%B5%D0%B1%D0%BD%D1%8B%D0%B9%20%D1%8D%D0%BA%D1%81%D0%BF%D0%B5%D1%80%D1%82&cost=49800&tovar=19197&sendsay_email=[%%20anketa.member.email%20%]&utm_source=sendsay&utm_medium=basket&utm_campaign=lostbasket&utm_content=lostbasket&utm_term=lostbasket",price='49800'):
	headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/51.0'
    }
	print('parseSiteUrl()')
	req = requests.get(url, headers)
	soup = BeautifulSoup(req.content,'lxml')
	site_hour = soup.find('div','items-box-block__element-type-item').findChildren('span')[0].text.replace('часов', '').replace('часа', '').strip()
	site_price = soup.find('div','course-info-block__action-buy-price').findChildren('span')[0].text.strip()
	site_data_list = {
			"title": soup.find('h1','main-title').text,
			"price":site_price,
			"hour":site_hour,
			"url": url
		}
	if site_price == price:
		print(Fore.GREEN+f'{site_data_list}'+Style.RESET_ALL)
		return site_data_list
	else:
		print(Fore.LIGHTBLACK_EX+f'no match price {site_data_list}'+Style.RESET_ALL)

def main():
	bs4pars()


if __name__ == "__main__":
	# main()
	parseSiteUrl()