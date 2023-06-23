import sys
import os
from time import sleep
from random import uniform
from jinja2 import Environment, select_autoescape, FileSystemLoader
from config_generator.webdriver_config import selenium_start, webdriver
from jinja2.environment import Template
from random import randint
from bs4 import BeautifulSoup
import json
from colorama import Fore,Back,Style
from pydantic import BaseModel,StrictInt,StrictStr
from typing import Optional
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
	# webdrv.get(url)
	with open("module/template_generator/source/expertnayaCep_VO/listFromMindbox.html","r",encoding='utf-8') as f:
		html = f.read()

	soup = BeautifulSoup(html,'lxml')
	opt = soup.find_all("span",{"data-testid":"HighlighterRoot.tableTitle"})
	li = list()
	for o in opt:
		li.append(o.text.strip().replace("\n","").strip())

	# print(opt)
	# sport_list = list()
	# for d in opt:
	# 	print(d['title'])
	# 	sport_list.append(d['title'])
	with open("parse_data.json","w",encoding="utf-8") as f:
		if li:
			json.dump(li,f,ensure_ascii=False,indent=4)

def save_html_with_template(path:str,file_name:str,template:Template,context):
	with open(os.path.join(f"{os.getcwd()}/{path}",file_name),'w',encoding='utf-8') as result:
		result.write(template.render(context).replace('amp;',''))
	return path,file_name

def save_json(data:list[dict],path: str,file_name: str):
	with open(os.path.join(f"{os.getcwd()}/{path}",file_name),'w',encoding='utf-8') as f:
		json.dump(data,f,ensure_ascii=False,indent=4)

def load_json(path: str,file_name: str) -> list[dict[str,str|int|list[dict]|dict[str,str|int|None]]|list[str]]:
	with open(os.path.join(f"{os.getcwd()}/{path}",file_name),'r',encoding='utf-8') as f:
		data: list[dict[str,str|int|list[dict]|dict[str,str|int|None]]|list[str]] = json.loads(f.read())
	return data

def load_template(template_name:str,ext:str):
	env = Environment(loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__)),
	autoescape=select_autoescape([f'{ext}']))
	return env.get_template(f"{template_name}.{ext}")

def build_json():
	source_json = load_json(f"module/template_generator/source/expertnayaCep_VO","Квалификационные возможности врачей и провизоров и пути их изменения 2023.json")
	source_json_ = load_json(f"module/template_generator/source/expertnayaCep_VO","Аккред ОТ 2021 ОБЩЕЕedit.json")
	source_ppjson = load_json(f"data/json/docx_converted/nmofile","program_СПО.json")

	# ###
	class SourceData(BaseModel):
		spec: Optional[StrictStr] = None
		job: Optional[list[StrictStr]] = None
		pp: Optional[dict[StrictStr,StrictStr]] = None 
	# ###
	class SourcePPdata(BaseModel):
		new: Optional[list] = None
		delete: Optional[list] = None
		progs: Optional[list] = None
		orig: Optional[list] = None
	dict_data: dict = dict()
	fail_list_nmo_prog: list[dict] = list()
	list_data: dict[str,str|int] = list()
	
	tag_HIT_prog_list = [
		"ультразвуковая диагностика",
		"физическая и реабилитационная медицина",
		"эндокринология",
		"психотерапия",
		"психиатрия",
		"неврология",
		"урология",
		"остеопатия",
		"мануальная терапия",
		"организация здравоохранения и общественное здоровье"
	]

	"""
		специальность: Психиатрия ==>
		✓ будет добавлено: ['Сексология (до 1 сентября 2023)'];

		доавить в карточку дату
	"""
	"""
		специальность: Детская онкология ==>
		✓ будет добавлено: ['Радиология', 'Медико-социальная экспертиза', 'Гематология (аккредитация по Детской онкологии-гематологии)'];

		Гематология - остается в Детской онкологии
	"""
	
	# Очень важная Информация снизу
	countKVAL = 0
	countACC = 0
	for i,data in enumerate(source_json):
		
		countKVAL += 1
		
		item = SourceData()
		item_pp = SourcePPdata()
		item.spec = data['spec'][0]
		item.job = data['job']
		if data['pp']:
			item_pp.progs = data['pp']
		item.pp = item_pp.dict()
		for data_ in source_json_:
			if data['spec'][0].lower() == data_['spec'].lower():

					different_in_dataKVAL = list(set(data['pp']) - set(data_['pp']))
					different_in_dataACC = list(set(data_['pp']) - set(data['pp']))
					
					# if d.get("specname") == "":
					if data['spec'][0].lower() == data_["spec"].lower():
						
						item.spec = data['spec'][0]
						item.job = data['job']
						if different_in_dataKVAL != []:
							item_pp.new = different_in_dataKVAL
						if different_in_dataACC != []:
							item_pp.delete = different_in_dataACC
						item_pp.progs = list(set(data_['pp']) - set(different_in_dataACC)) + different_in_dataKVAL
						item_pp.orig = data_['pp']
						item.pp = item_pp.dict()
		# if item.pp:
		# 	print(item.spec,item.pp.get('progs'))
		list_data.append(item.dict())
	
	
	for fin_data in list_data[8:]:
		data_list_search = list()
		# print(fin_data.get("pp").get("new"))
		# print("=>")
		# print(fin_data.get("pp").get("progs"))

		print(f"\n| {fin_data.get('spec')} | ==>")
		
		if fin_data.get("pp").get("progs"):
			list_of_new_progs = list()
			for kpd,fin_progs_data in enumerate(fin_data.get("pp").get("progs")):
				countACC += 1
				new_name_prog = str()
				tags = None
				if fin_data.get("pp").get("new"):
					if fin_progs_data in fin_data.get("pp").get("new") and fin_progs_data.lower() in tag_HIT_prog_list:
						tags={"tag": "#HIT# #NEW#"}
					elif fin_progs_data in fin_data.get("pp").get("new"):
						tags={"tag": "#NEW#"}
					elif fin_progs_data.lower() in tag_HIT_prog_list:
						tags={"tag": "#HIT#"}
					else:
						print(f"{kpd+1} {fin_progs_data}")
						list_of_new_progs.append(fin_progs_data)
				elif fin_progs_data.lower() in tag_HIT_prog_list:
						print(f"{kpd+1} {fin_progs_data} #HIT#")
						list_of_new_progs.append(new_name_prog)
				else:
					print(f"{kpd+1} {fin_progs_data}")
					list_of_new_progs.append(fin_progs_data)
				fin_data['pp']['progs'] = list_of_new_progs

				# if fin_progs_data == 'Рентгенология': hour = 990
				# if fin_progs_data == 'Остеопатия':
				# 	hour = 3504
				# 	price = 124500
				# if fin_progs_data == 'Физическая и реабилитационная медицина': hour = 1008

				if fin_progs_data == 'Остеопатия':
					finded_data = search(fin_progs_data,124500,"ВО")
				elif fin_progs_data == 'Анестезиология-реаниматология':
					finded_data = search(fin_progs_data,99000,"ВО")
				else:
					finded_data = search(fin_progs_data,49800,"ВО")

				try:
					if len(finded_data) >= 2:
						print(Fore.RED+f"\
						Че за х????\n\
						spec: {fin_data.get('spec')}\n\
						prog: {fin_progs_data}"+Fore.RESET)
						pass

					dict_data = {
						"specname": fin_data.get('spec'),
						"tags": tags,
						"programs": finded_data[0]
					}
				except:
					dict_data = {
						"specname": fin_data.get('spec'),
						"tags": tags,
						"programs": finded_data
					}
				print(f"\nin {fin_data.get('spec')} search i found this:\n{finded_data}")
				data_list_search.append(dict_data)
		save_json(data_list_search,"module/template_generator/source/expertnayaCep_VO/expertnayaCep_VO_pp",f"[ПП] {fin_data.get('spec')}.json")

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
	# main_json: list[dict] = load_json(f"module/template_generator/source/expertnayaCep_VO","sport_all_pp_pk.json")
	template = load_template("expertnayaCep_VO/expertnayaCep_VO","html")


	theme_list: list = list()

	class Programs(BaseModel):
		tag: Optional[StrictStr] = None
		id: Optional[StrictInt] = None
		spec: Optional[StrictStr] = None
		name: Optional[StrictStr] = None
		price: Optional[StrictInt] = None
		hour: Optional[StrictInt] = None
		url: Optional[StrictStr] = None



	for file_name in os.listdir("module/template_generator/source/expertnayaCep_VO/expertnayaCep_VO_pp"):

		main_json: list[dict] = load_json(f"module/template_generator/source/expertnayaCep_VO/expertnayaCep_VO_pp",file_name)
		context = dict()
		li:list[dict] = list()
		for i,data in enumerate(main_json):
			item = Programs()

			if file_name.replace("[ПП] ","").replace(".json","").strip() == data.get("specname"):
				if data.get("programs"):
					progs: list[dict] = data.get("programs")

					# for prog in progs:

					item.id = progs.get("id")
					item.spec = progs.get("spec")
					item.name = progs.get("name")
					item.price = progs.get("price")
					item.hour = progs.get("hour")
					item.url = progs.get("final_url")
					if data['tags']:
						item.tag = data['tags']['tag']
					# print("\n"+f"{item.name}"+"\n")
					li.append(item.dict())

					context = {
						"specname": file_name.replace("[ПП] ","").replace(".json","").strip(),
						"programs": li
					}
					print(context)
					print("========")
						# prog["final_url"] = f"{url}?program={name}&header=Курс {type_prog} {name}&cost={price}&tovar={id}{'&sendsay_email=${ Recipient.Email }'}"
							# print(prog.get("final_url"),f"\n{type_prog}")
							# source_json = load_json(f"module/template_generator/source/expertnayaCep_Medsestry",f"[Письмо 3] Переподготовка с аккредитацией или 6 причин, почему не стоит бояться аккредитации.json")
							# if data.get("spec") == "Профессиональная переподготовка":
							# 	data['final_url'] = f"{data.get()}"

					html_path,html_name = save_html_with_template("module/template_generator/ready/expertnayaCep_VO/expertnayaCep_VO_pp",f"[ПП] {data.get('specname')}.html",template, context)
		
def checkTemplatesTags(html_path:str,html_name:str):
	with open(os.path.join(f"{os.getcwd()}/{html_path}",html_name),'w',encoding='utf-8') as f:
		html_data = f.read()
	print(html_data)

def main():
	# load_json(f"data/json/docx_converted","docxtojson.json")
	# print(load_template("expertnayaCep_Mdesestry_pp","html"))
	# print(sys.path)
	# search()
	# build()
	build_jina_template()
	# build_json()
	# bs4parser("https://apkipp.ru/katalog/fizicheskaya-kultura-i-sport/")

if __name__ == "__main__":
	main()
