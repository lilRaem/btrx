from time import time
from colorama import Fore,Back,Style
from random import choice
from bs4 import BeautifulSoup
import requests
import os, json
import sys
sys.path.insert(0,os.getcwd())
try:
	from module.config import FinalData, ParseSiteConfig
except:
	from config import FinalData, ParseSiteConfig
from module.logger import logging

log = logging.getLogger("btrx.module.html_pars.parserhtml")
def bs4pars():
	with open(f"{os.getcwd()}\\module\\html\\templates\\source\\pp_spo.html",'r',encoding='utf-8') as f:
		html = f.read()
	bs4conf = ParseSiteConfig()
	soup = BeautifulSoup(html,'lxml')
	pars_list = []
	pars_dict = {}
	for el in soup.find_all(class_=f'{bs4conf.soupMainBlock}'):
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
			'prog_special': prog_special,
			'prog_altspecial': prog_altspecial,
			'prog_hour': prog_hour,
			'prog_price': prog_price,
			'url': el.find('a','button').get('href')
		}
		log.debug(f"Find:\ntitle: {pars_dict['prog_title']}\nhour: {pars_dict['prog_hour']}\nprice: {pars_dict['prog_price']}\nurl: {pars_dict['url']}")
		pars_list.append(pars_dict)
	with open(f'{os.getcwd()}/module/html/templates/data.json','w',encoding='utf-8') as fp:
		json.dump(pars_list,fp,ensure_ascii=False,indent=4)

def parseSiteUrl(parseurl: str="https://apkipp.ru/katalog/zdravoohranenie/kurs-ultrazvukovaya-diagnostika-3/",price: int = 99000) -> list[dict[str,str|int|None]]:
	start = time()
	psUrlconf = ParseSiteConfig()
	final_data = FinalData()
	site_data_list: list[dict[str,str|int|None]] = list()
	header = choice(psUrlconf.headers)

	req = requests.get(parseurl, headers=header,timeout=None)
	# print(f"\n{Fore.LIGHTYELLOW_EX}request time: {round(time()-start,2)} sec{Fore.RESET}")
	soup = BeautifulSoup(req.content,'lxml')
	if parseurl == "https://apkipp.ru/katalog/zdravoohranenie/kurs-ultrazvukovaya-diagnostika-3/":
		final_data.name = soup.find(f'h2',f'color-pink sets_banner-title').text.strip()

		final_data.hour = 600

		_price = 99000
		_spec = soup.find("div","sets_banner-suptitle").text.strip()
	elif parseurl:
		final_data.name = soup.find(f'{psUrlconf.soupName[0]}',f'{psUrlconf.soupName[1]}')

		if not final_data.name: final_data.name = soup.find('h1').text
		else: final_data.name: final_data.name = soup.find(f'{psUrlconf.soupName[0]}',f'{psUrlconf.soupName[1]}').text

		try:
			final_data.hour = int(soup.find(f'{psUrlconf.soupHour[0]}', f'{psUrlconf.soupHour[1]}').findChildren('span')[0].text.replace('часов', '').replace('часа', '').strip())
		except:
			final_data.hour = int(soup.find('div', 'intro__include-item').findChildren('span')[0].text.replace('часов', '').replace('часа', '').replace('дней', '').strip())
		try:
			_price = soup.find(f'{psUrlconf.soupPrice[0]}',f'{psUrlconf.soupPrice[1]}').findChildren('span')
		except:
			try:
				_price = soup.find('div','pay__wrapper-prices').findChildren('div','pay__price-new')[1].text.replace("₽","").replace(" ","").strip()
			except:
				_price = soup.find('div','pay__wrapper-prices').findChildren('div','pay__price-new')[0].text.replace("₽","").replace(" ","").strip()
		try:
			_spec = soup.find("div","course-info-block__text-requirements-title").text.strip()
		except:
			_spec = soup.find("div","intro__suptitle").text.strip()
	else:
		final_data.name = soup.find('h1').text
		final_data.hour = int(soup.find('div', 'intro__include-item').findChildren('span')[0].text.replace('часов', '').replace('часа', '').strip())
		_price = soup.find('div','pay__wrapper-prices').findChildren('div','pay__price-new')[1].text.replace("₽","").replace(" ","").strip()
		_spec = soup.find("div","intro__suptitle").text.strip()
		print(final_data)

	log.info(f"Parsed url: {parseurl}\nname: {final_data.name} hour: {final_data.hour} price: {_price}",stacklevel=200)

	if "профессиональной переподготовки" in _spec or "профессиональной переподготовке" in _spec or "Первичная переподготовка" in _spec or "Он-лайн переподготовка" in _spec:
		_spec = "Профессиональная переподготовка"
	elif "повышения квалификации" in _spec or "повышении квалификации" in _spec and "НМО" not in _spec:
		_spec = "Повышение квалификации"
	elif "НМО" in _spec and "повышении квалификации" in _spec or "цикл НМО" in _spec:
		_spec = "Повышение квалификации (НМО)"
	elif "ПОЛУЧЕНИЕ КАТЕГОРИИ" in _spec or "получение категории" in _spec or "Получение категории" in _spec:
		_spec = "Категория медработника"
	else:
		_spec = None

	type_url = parseurl.replace("https://apkipp.ru/katalog/","").split("/")[0]

	if type_url == "zdravoohranenie":
		final_data.katalog = f"Здравоохранение/{type_url}"
		final_data.type_zdrav = "ВО"
	elif type_url == "zdravoohranenie-srednij-medpersonal":
		final_data.katalog = f"Здравоохранение - Средний медперсонал/{type_url}"
		final_data.type_zdrav = "СПО"
	elif type_url == "zdravoohranenie-mladshij-medpersonal":
		final_data.katalog = f"Здравоохранение - Младший медперсонал/{type_url}"
		final_data.type_zdrav = "МП"
	elif type_url == "zdravoohranenie-nemeditsinskie-spetsialnosti":
		final_data.katalog = f"Здравоохранение - Немедицинские специальности/{type_url}"
		final_data.type_zdrav = "НМП"
	elif type_url == "menedzhment":
		final_data.katalog = f"Менеджмент/{type_url}"
	elif type_url == "doshkolnoe-obrazovanie":
		final_data.katalog = f"Дошкольное образование/{type_url}"
	elif type_url == "sudebnyie-pristavyi":
		final_data.katalog = f"Судебные приставы/{type_url}"
	elif type_url == "servis-i-turizm":
		final_data.katalog = f"Сервис и туризм/{type_url}"
	elif type_url == "fizicheskaya-kultura-i-sport":
		final_data.katalog = f"Физическая культура и спорт/{type_url}"
	elif type_url == "pedagogicheskoe-obrazovanie":
		final_data.katalog = f"Педагогическое образование/{type_url}"
	elif type_url == "tsentryi-zanyatosti-naseleniya":
		final_data.katalog = f"Центры занятости населения/{type_url}"
	elif type_url == "avtoshkolam":
		final_data.katalog = f"Автошколам/{type_url}"
	elif type_url == "nalogovoe-delo":
		final_data.katalog = f"Налоговое дело/{type_url}"
	elif type_url == "kultura-i-iskusstvo":
		final_data.katalog = f"Культура и искусство/{type_url}"
	elif type_url == "sotsialnaya-zaschita-naseleniya":
		final_data.katalog = f"Социальная защита населения/{type_url}"
	elif type_url == "dopolnitelnoe-obrazovanie":
		final_data.katalog = f"Дополнительное образование/{type_url}"
	elif type_url == "notariat":
		final_data.katalog = f"Нотариат/{type_url}"
	elif type_url == "otsenka-i-sudebnaya-ekspertiza":
		final_data.katalog = f"Оценка и судебная экспертиза/{type_url}"
	elif type_url == "stroitelstvo":
		final_data.katalog = f"Строительство/{type_url}"
	elif type_url == "ritualnyie-uslugi":
		final_data.katalog = f"Ритуальные услуги/{type_url}"
	elif type_url == "psihologiya":
		final_data.katalog = f"Психология/{type_url}"
	elif type_url == "defektologiya":
		final_data.katalog = f"Дефектология/{type_url}"
	elif type_url == "servis-i-turizm":
		final_data.katalog = f"Сервис и туризм/{type_url}"
	elif type_url == "pensionnyie-fondyi":
		final_data.katalog = f"Пенсионные фонды/{type_url}"
	elif type_url == "ekonomika":
		final_data.katalog = f"Экономика/{type_url}"
	elif type_url == "promyishlennaya-bezopasnost":
		final_data.katalog = f"Промышленная безопасность/{type_url}"
	elif type_url == "avtotransportnyie-predpriyatiya":
		final_data.katalog = f"Автотранспортные предприятия/{type_url}"
	elif type_url == "zags":
		final_data.katalog = f"ЗАГС/{type_url}"
	elif type_url == "yurisprudentsiya":
		final_data.katalog = f"Юриспруденция/{type_url}"
	elif type_url == "obschepit":
		final_data.katalog = f"Общепит/{type_url}"
	else:
		final_data.type_zdrav = None
	# print(soup.find("div","banner-box__info-title"))
	if _spec: final_data.spec = _spec
	if parseurl != "https://apkipp.ru/katalog/zdravoohranenie/kurs-ultrazvukovaya-diagnostika-3/":
		if _price:
			for i,d in enumerate(_price):
				try:
					if d.get("class") != None and "old-price" in d.get("class")[i]: log.debug(f"Price with oldprice in site: {d.get('class')[i]}")
					else:
						if d.text != "₽":
							final_data.price = int(d.text.replace(" ₽",""))
							if price == int(d.text.replace(" ₽","")): log.debug(f"Price without oldprice: {final_data.price}")
				except:
					final_data.price = int(_price)
		else:
			try:
				final_data.price = int(soup.find(f'{psUrlconf.soupPrice[0]}',f'{psUrlconf.soupPrice[1]}').findChildren('span')[0].text.strip())
				log.debug(f"(try) Price without oldprice: {final_data.price}")
			except:
				final_data.price = price
				log.debug(f"(except) Price without oldprice: {final_data.price}")

		if final_data.price == price:
			final_data.url = parseurl
			site_data_list.append(final_data.dict())
			log.debug(Fore.GREEN+f"Found price: {site_data_list[0].get('price')}"+Fore.RESET)
		else: site_data_list.append(final_data.dict())

	if site_data_list.__len__() == 1:
		# print(Fore.MAGENTA+f'(parserhtml.py|parseSiteUrl(): count = 1) Search time: {round(time()-start,2)} sec' + Fore.RESET)
		return site_data_list
	else:
		log.error(Fore.RED+' fail parse too many programs '+Fore.RESET)
		# print(Fore.RED+f'(parserhtml.py|parseSiteUrl(): count > 1) Search time: {round(time()-start,2)} sec' + Fore.RESET)
		return site_data_list

def main():
	bs4pars()

if __name__ == "__main__":
	# main()
	print(parseSiteUrl(parseurl="https://apkipp.ru/katalog/zdravoohranenie-srednij-medpersonal/kurs-ultrazvukovaya-diagnostika/",price=9792))