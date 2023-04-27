import sys
import os
from time import sleep
from random import uniform
from jinja2 import Environment, select_autoescape, FileSystemLoader
from jinja2.environment import Template

from bs4 import BeautifulSoup
import json
from colorama import Fore,Back,Style
import requests
from pydantic import BaseModel,StrictInt,StrictStr
from typing import Optional
from config.webdriver_config import selenium_start
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
sys.path.insert(0,os.getcwd())
from main_search import search
from module.logger import init_logger , logging
from module.config import ParseSiteConfig
# склонение слов по падежам
import pymorphy3

def bs4parser(url:str):
	parsConf = ParseSiteConfig()

	webdrv = selenium_start()
	# if "custom-select__option" in req.text:
	# 	print(req.text)
	webdrv.get(url)
	html = webdrv.page_source

	soup = BeautifulSoup(html,'lxml')

	opt = soup.find(class_="custom-select__dropdown").children
	sport_list = list()
	for d in opt:
		print(d['title'])
		sport_list.append(d['title'])
	with open("parse_data.json","w",encoding="utf-8") as f:
		json.dump(sport_list,f,ensure_ascii=False,indent=4)

def save_html_with_template(path:str,file_name:str,template:Template,context):
	with open(os.path.join(f"{os.getcwd()}\\{path}",file_name),'w',encoding='utf-8') as result:
		result.write(template.render(context).replace('amp;',''))

def save_json(data:list[dict],path: str,file_name: str):
	with open(os.path.join(f"{os.getcwd()}\\{path}",file_name),'w',encoding='utf-8') as f:
		json.dump(data,f,ensure_ascii=False,indent=4)

def load_json(path: str,file_name: str) -> list[dict[str,str|int|list[dict]|dict[str,str|int|None]]|list[str]]:
	with open(os.path.join(f"{os.getcwd()}\\{path}",file_name),'r',encoding='utf-8') as f:
		data: list[dict[str,str|int|list[dict]|dict[str,str|int|None]]|list[str]] = json.loads(f.read())
	return data

def load_template(template_name:str,ext:str):
	env = Environment(loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__)),
	autoescape=select_autoescape([f'{ext}']))
	return env.get_template(f"{template_name}.{ext}")

def build_json():
	source_json = load_json(f"module\\template_generator\\source\\Sport","sport_all.json")
	source_json_ = load_json(f"module\\template_generator\\source\\Sport","fizProg_list_from_docx.json")
	source_ppjson = load_json(f"data\\json\\docx_converted\\nmofile","program_СПО.json")

	# ###
	class SourceData(BaseModel):
		spec: Optional[StrictStr] = None
		job: Optional[list[str]] = None
		pp: Optional[list[str]] = None
	# ###

	dict_data: dict = dict()
	fail_list_nmo_prog: list[dict] = list()
	list_data: list[dict[str,str|int]] = list()
	for d in source_json:
		if d.get("specname") == "":
			print(d)
	# list_data.append(dict_data)
	# save_json(list_data,"module\\template_generator\\source\\Sport",f"sport_all.json")

def findNMO(prog:str,nmolist:list[dict]):
	class SourceNmoData(BaseModel):
		nmo_spec: Optional[StrictStr] = None
		nmo_prog: Optional[StrictStr] = None
		price: Optional[StrictInt] = None
		hour: Optional[StrictInt] = None
		date: Optional[StrictStr] = None
		linkNmo: Optional[StrictStr] = None
	list_nmo_prog: list[dict] = list()
	for data in nmolist:
		source__nmo_data = SourceNmoData()
		source__nmo_data.nmo_spec = data.get('title_spec')
		source__nmo_data.nmo_prog = data.get('title_program')
		source__nmo_data.price = data.get('price')
		source__nmo_data.hour = data.get('hour')
		source__nmo_data.date = data.get('date')
		source__nmo_data.linkNmo = data.get('linkNmo')
		source__nmo_data.linkNmo = source__nmo_data.linkNmo.strip()
		if prog == "Наркология":
			prog = "Наркология\n(Лечебное дело)"
		if prog == "Лабораторное дело":
			prog = "Лабораторное дело (Медико-профилактическое дело)"
		if str(source__nmo_data.nmo_spec) == str(prog):
			# print(f"\nKvalspec: {prog}\nnmo data: {source__nmo_data.dict()}\n")
			list_nmo_prog.append(source__nmo_data.dict())
	return list_nmo_prog

def build_jina_template():
	init_logger("template_generator","template_generator")
	log = logging.getLogger("template_generator.main.build_jina_template")
	main_json: list[dict] = load_json(f"module\\template_generator\\source\\Sport","sport_all_pp_pk.json")
	template = load_template("sport/sport_pk_pp_one_sport","html")

	li:list[dict] = list()
	for data in main_json:
		progs: list[dict] = data.get("programs")
		for prog in progs:
			id = prog.get("id")
			spec = prog.get("spec")
			name = prog.get("name")
			price = prog.get("price")
			hour = prog.get("hour")
			url = prog.get("url")

			if spec == "Профессиональная переподготовка":
				type_prog = "ПП"
			elif spec == "Повышение квалификации":
				type_prog = "ПК"
			elif spec == "Повышение квалификации (НМО)":
				type_prog = "НМО"
			else:
				type_prog = None

			prog["final_url"] = f"{url}?program={name}&header=Курс {type_prog} {name}&cost={price}&tovar={id}{'&sendsay_email=${ Recipient.Email }'}"
			# print(prog.get("final_url"),f"\n{type_prog}")
			# source_json = load_json(f"module\\template_generator\\source\\expertnayaCep_Medsestry",f"[Письмо 3] Переподготовка с аккредитацией или 6 причин, почему не стоит бояться аккредитации.json")
			# if data.get("spec") == "Профессиональная переподготовка":
			# 	data['final_url'] = f"{data.get()}"


		context = {
			"specname": data.get("specname"),
			"progs": data.get("programs")
		}
		morph = pymorphy3.MorphAnalyzer()


		with open("file.txt",'a',encoding='utf-8') as f:
			try:
				print(context.get("specname").split())
				result = ' '.join(morph.parse(word)[0].inflect({'datv'}).word for word in context.get("specname").split())
				to_write = f"\n\n---\n{context.get('specname')}\n\n\"Тренер по {result}? Получите диплом или удостоверение по {result}. Дистанционно. Диплом с правом ведения деятельности\""
				f.write(to_write)
			except:
				to_write = f"\n\n!!!\n{context.get('specname').lower()}\n\n\"Тренер по {context.get('specname').lower()}? Получите диплом или удостоверение по {context.get('specname')}. Дистанционно. Диплом с правом ведения деятельности\""
				print(Fore.RED+f'{context.get("specname").split()}'+Fore.RESET)
				f.write(to_write)
		save_html_with_template("module\\template_generator\\ready\\sport\\Sport_all",f"[ПП+ПК] {data.get('specname')}.html",template, context)

def main():
	# load_json(f"data\\json\\docx_converted","docxtojson.json")
	# print(load_template("expertnayaCep_Mdesestry_pp","html"))
	# print(sys.path)
	# search()
	# build()
	build_jina_template()
	# build_json()
	# bs4parser("https://apkipp.ru/katalog/fizicheskaya-kultura-i-sport/")

if __name__ == "__main__":
	main()
