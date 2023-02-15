from time import time
from colorama import Fore,Back,Style
from bs4 import BeautifulSoup
import requests
import os, json
try:
	from module.config import FinalData, ParseSiteConfig
except:
	from config import FinalData, ParseSiteConfig

def bs4pars():
	with open(f"{os.getcwd()}\\module\\html\\templates\\source\\pp_spo.html",'r',encoding='utf-8') as f:
		html = f.read()
	bs4conf = ParseSiteConfig()
	soup = BeautifulSoup(html,'lxml')
	pars_list = []
	pars_dict = {}
	for el in soup.find_all(class_=f'{bs4conf.soupMainBlock}'):
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
	# print(pars_list)
	with open(f'{os.getcwd()}/module/html/templates/data.json','w',encoding='utf-8') as fp:
		json.dump(pars_list,fp,ensure_ascii=False,indent=4)

def parseSiteUrl(parseurl: str="https://apkipp.ru/katalog/zdravoohranenie/kurs-ultrazvukovaya-diagnostika-3/",price: str='99000'):
	start = time()
	psUrlconf = ParseSiteConfig()
	headers = psUrlconf.headers
	final_data = FinalData()
	site_data_list = []
	req = requests.get(parseurl, headers,timeout=None)
	soup = BeautifulSoup(req.content,'lxml')

	final_data.name = soup.find(f'{psUrlconf.soupName[0]}',f'{psUrlconf.soupName[1]}').text
	final_data.hour = soup.find(f'{psUrlconf.soupHour[0]}', f'{psUrlconf.soupHour[1]}').findChildren('span')[0].text.replace('часов', '').replace('часа', '').strip()
	_price = soup.find(f'{psUrlconf.soupPrice[0]}',f'{psUrlconf.soupPrice[1]}').findChildren('span')
	if _price != []:
		for i,d in enumerate(_price):
			if d.get("class") != None and d.get("class")[i] == "old-price":
				print(f"Price with oldprice in site: {d.get('class')[i]}")
			else:
				if price == d.text:
					final_data.price = d.text
					print(f"Price with oldprice: {final_data.price}")
	else:
		try:
			final_data,price = soup.find(f'{psUrlconf.soupPrice[0]}',f'{psUrlconf.soupPrice[1]}').findChildren('span')[0].text.strip()
			print(f"(try) Price without oldprice: {final_data.price}")
		except:
			final_data.price = price
			print(f"(except) Price without oldprice: {final_data.price}")
	final_data.url = parseurl
	# print(final_data.price)
	count = 0
	if final_data.price == price:
		site_data_list.append(json.loads(final_data.json(ensure_ascii=False)))
		print(site_data_list[0]['price'])
	else:
		# final_data.hour = None
		# final_data.price = None
		# final_data.url = None
		if final_data.price:
			if "₽" in final_data.price:
				final_data.price = final_data.price.replace("₽","").strip()
		site_data_list.append(json.loads(final_data.json(ensure_ascii=False)))
	for data in site_data_list:
		count = count + 1
	if count == 1:
		print(Fore.MAGENTA+f'(parserhtml.py|parseSiteUrl(): count = 1) Search time: {round(time()-start,2)} sec' + Fore.RESET)
		return site_data_list
	else:
		print('fail parse too many programs')
		print(Fore.MAGENTA+f'(parserhtml.py|parseSiteUrl(): count > 1) Search time: {round(time()-start,2)} sec' + Fore.RESET)
		# print(site_data_list[0])
		return site_data_list

def main():
	bs4pars()


if __name__ == "__main__":
	# main()
	print(parseSiteUrl(price='0'))