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
sys.path.insert(0,os.getcwd())
from main_search import search
from module.logger import init_logger , logging


def save_html_with_template(path:str,file_name:str,template:Template,context):
	with open(os.path.join(f"{os.getcwd()}\\{path}",file_name),'w',encoding='utf-8') as result:
		result.write(template.render(context).replace('amp;',''))

def save_json(data:list[dict],path: str,file_name: str):
	with open(os.path.join(f"{os.getcwd()}\\{path}",file_name),'w',encoding='utf-8') as f:
		json.dump(data,f,ensure_ascii=False,indent=4)

def load_json(path: str,file_name: str) -> list[dict[str,str|int|list[str]]]:
	with open(os.path.join(f"{os.getcwd()}\\{path}",file_name),'r',encoding='utf-8') as f:
		data: list[dict[str,str|int|list[str]|dict[str,str|int|None]]] = json.loads(f.read())
	return data

def load_template(template_name:str,ext:str):
	env = Environment(loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__)),
	autoescape=select_autoescape([f'{ext}']))
	return env.get_template(f"{template_name}.{ext}")

def build_json():
	source_json = load_json(f"data\\json\\docx_converted","docxtojson.json")
	source_nmojson = load_json(f"data\\json\\docx_converted\\nmofile","program_СПО.json")
	# ###
	class SourceData(BaseModel):
		spec: Optional[StrictStr] = None
		job: Optional[list[str]] = None
		pp: Optional[list[str]] = None
	# ###

	class SourceNmoData(BaseModel):
		nmo_spec: Optional[StrictStr] = None
		nmo_prog: Optional[StrictStr] = None
		price: Optional[StrictInt] = None
		hour: Optional[StrictInt] = None
		date: Optional[StrictStr] = None
		linkNmo: Optional[StrictStr] = None
	dict_data: dict = dict()


	fail_list_nmo_prog_: list[dict] = list()
	for source_jdata in source_json:
		list_data: list[dict[str,str|int]] = list()
		source_data = SourceData()
		source__nmo_data = SourceNmoData()
		source_data.spec = source_jdata.get('spec')
		source_data.job = source_jdata.get('job')
		source_data.pp = source_jdata.get('pp')
		count = 0
		list_nmo_prog: list[dict] = list()
		fail_list_nmo_prog: list[dict] = list()

		for data in source_nmojson:

			source__nmo_data = SourceNmoData()
			source__nmo_data.nmo_spec = data.get('title_spec')
			source__nmo_data.nmo_prog = data.get('title_program')
			source__nmo_data.price = data.get('price')
			source__nmo_data.hour = data.get('hour')
			source__nmo_data.date = data.get('date')
			source__nmo_data.linkNmo = data.get('linkNmo')
			source__nmo_data.linkNmo = source__nmo_data.linkNmo.strip()
			dict_data_: dict = dict()

			if source__nmo_data.linkNmo == "https://clck.ru/337Pz8" or source__nmo_data.linkNmo == "https://clck.ru/337QMR" or source__nmo_data.linkNmo == "https://clck.ru/337Qe6" or source__nmo_data.linkNmo == "https://clck.ru/337Qvm" or source__nmo_data.linkNmo == "https://clck.ru/337RFE":
				count += 1
				print(count,source__nmo_data.dict())
				fail_list_nmo_prog.append(source__nmo_data.dict())
				dict_data_ = {
					"specname": source__nmo_data.nmo_spec,
					"programs": fail_list_nmo_prog
				}
				fail_list_nmo_prog_.append(dict_data_)
				save_json(fail_list_nmo_prog_,"module\\template_generator\\source\\expertnayaCep_Medsestry_nmo",f"fail.json")
			if str(source__nmo_data.nmo_spec) == str(source_data.spec):
				list_nmo_prog.append(source__nmo_data.dict())
			dict_data = {
				"specname": source_data.spec,
				"programs": list_nmo_prog
			}

		list_data.append(dict_data)
		save_json(list_data,"module\\template_generator\\source\\expertnayaCep_Medsestry_nmo",f"{source_data.spec}.json")
	# print(list_data)
		# for jobs in source_data.job:
		# 	print(jobs)

		# finder=search(source_data.spec,9792,"НМО")
		# if finder:
		# 	print(f"title: {source_data.spec} finder_items: {finder.__len__()}")
		# else:
		# 	print("Finder is none")
		# dict_data = dict()
		# if finder:
		# 	dict_data ={
		# 	"specname": source_data.spec,
		# 	"program_data": finder[0]
		# 	}
		# 	list_data.append(dict_data)

def build_jina_template():
	init_logger("template_generator","template_generator")
	log = logging.getLogger("template_generator.main.build_jina_template")
	main_json = load_json(f"data\\json\\docx_converted","docxtojson.json")

	template = load_template("expertnayaCep_Medsestry_nmo_144","html")
	context = None
	for data in main_json:

		if data.get("spec") != "Медицинская оптика" and data.get("spec") != "Фармация":
			# print(data.get('pp'))
			try:
				source_json = load_json(f"module\\template_generator\\source\\expertnayaCep_Medsestry_nmo_144",f"{data.get('spec')}.json")
				li = list()
				for s_data in source_json:
					if data.get("spec") == s_data.get('specname'):
						# print(s_data.get("name"))
						if s_data.get('program_data').get("hour") == 0:
							log.propagate=False
							log.warning(f"hour = {s_data.get('program_data').get('hour')}| main_spec: {data.get('spec')} and in prog specname: {s_data.get('program_data').get('name')} id: {s_data.get('program_data').get('id')} {s_data.get('program_data').get('final_url')}")
						li.append(s_data)
						context = {
							"specname": data.get("spec"),
							"progs": li
						}
						save_html_with_template("module\\template_generator\\ready\\expertnayaCep_Medsestry\\nmo_144",f"[НМО 144] [Медсестры] {data.get('spec')}.html",template,context)
			except:
				print(data.get("spec"))
	if context:
		log.debug("Build templates successfully")
	else:
		log.error("Error build templates")

def main():
	# load_json(f"data\\json\\docx_converted","docxtojson.json")
	# print(load_template("expertnayaCep_Mdesestry_pp","html"))
	# print(sys.path)
	# search()
	# build()
	# build_jina_template()
	build_json()
if __name__ == "__main__":
	main()
