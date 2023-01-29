from time import time
from typing import Optional
from colorama import Fore,Back,Style
from pydantic import BaseModel, StrictStr
from bs4 import BeautifulSoup
import requests
import os, json
# try:
# 	from module.config import FinalData
# except:
# 	from config import FinalData
from typing import Optional
from pydantic import BaseModel, StrictStr

class FinalData(BaseModel):
	id: Optional[StrictStr] = None
	spec: Optional[StrictStr] = None
	name: Optional[StrictStr] = None
	price: Optional[StrictStr] = None
	hour: Optional[StrictStr] = None
	nmoSpec: Optional[StrictStr] = None
	linkNmo: Optional[StrictStr] = None
	url: Optional[StrictStr] = None

def bs4pars():
	with open(f"{os.getcwd()}\\module\\html\\templates\\source\\pp_spo.html",'r',encoding='utf-8') as f:
		html = f.read()

	soup = BeautifulSoup(html,'lxml')
	pars_list = []
	pars_dict = {}
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

def parseSiteUrl(parseurl: str="https://apkipp.ru/katalog/zdravoohranenie-nemeditsinskie-spetsialnosti/kurs-sudebnyij-ekspert-ekspert-biohimik-ekspert-genetik-ekspert-himik/",price: str='49800'):
	start = time()
	headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/51.0'
    }
	final_data = FinalData()
	site_data_list = []
	req = requests.get(parseurl, headers,timeout=None)
	soup = BeautifulSoup(req.content,'lxml')

	final_data.name = soup.find('h1','main-title').text
	final_data.hour = soup.find('div','items-box-block__element-type-item').findChildren('span')[0].text.replace('часов', '').replace('часа', '').strip()
	final_data.price = soup.find('div','course-info-block__action-buy-price').findChildren('span')[0].text.strip()
	final_data.url = parseurl

	count = 0
	if final_data.price == price:
		site_data_list.append(json.loads(final_data.json(ensure_ascii=False)))
		print(site_data_list[0]['price'])
	else:
		final_data.hour = None
		final_data.price = None
		final_data.url = None
		site_data_list.append(json.loads(final_data.json(ensure_ascii=False)))
	for data in site_data_list:
		count = count + 1
	if count == 1:
		print(Fore.MAGENTA+f'(parserhtml.py|parseSiteUrl(): count = 1) Search time: {round(time()-start,2)} sec' + Fore.RESET)
		return site_data_list
	else:
		print('fail parse too many programs')
		print(Fore.MAGENTA+f'(parserhtml.py|parseSiteUrl(): count > 1) Search time: {round(time()-start,2)} sec' + Fore.RESET)
		print(site_data_list[0])
		return site_data_list

def main():
	bs4pars()


if __name__ == "__main__":
	# main()
	print(parseSiteUrl())