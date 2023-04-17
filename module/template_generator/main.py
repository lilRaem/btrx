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


	dict_data: dict = dict()
	fail_list_nmo_prog: list[dict] = list()
	for source_jdata in source_json:

		source_data = SourceData()
		source_data.spec = source_jdata.get('spec')
		source_data.job = source_jdata.get('job')
		source_data.pp = source_jdata.get('pp')

		list_data: list[dict[str,str|int]] = list()

		count = 0
		print(f"\n\n\n{source_data.spec}")
		list_prog_data: list[dict[str,str|int]] = list()
		nmo_data = findNMO(source_data.spec,source_nmojson)
		if nmo_data:
			print(nmo_data.__len__(),nmo_data[0]['nmo_spec'])
			for nmo in nmo_data:
				if nmo:
					print(nmo['nmo_prog'], nmo["price"])
					prog_search = search(nmo["nmo_prog"],int(nmo["price"]),"НМО")
					try:
						list_prog_data.append(prog_search[0])
					except:
						da={
							"searched_spec": source_data.spec,
							"spec": nmo['nmo_spec'],
							"name": nmo['nmo_prog'],
							"hour": nmo['hour'],
							"price": nmo["price"],
							"linkNmo": nmo['linkNmo']
						}
						fail_list_nmo_prog.append(da)
		else:
			TypeError("nmo data erro")
		sleep(0.3)

		# try:
		# 	prog = search(source__nmo_data.nmo_prog,9792,"НМО")
		# except:
		# 	fail_list_nmo_prog.append(data)
		# 	save_json(list_data,"module\\template_generator\\source\\expertnayaCep_Medsestry_nmo",f"fail.json")
		# list_nmo_prog.append(prog)
		dict_data = {
			"specname": source_data.spec,
			"programs": list_prog_data
		}

		save_json(fail_list_nmo_prog,"module\\template_generator\\source\\expertnayaCep_Medsestry_nmo",f"fail.json")

		print(dict_data)
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
	main_json = load_json(f"data\\json\\docx_converted","docxtojson.json")

	template = load_template("expertnayaCep_Medsestry_nmo","html")
	context = None
	for data in main_json:
		if data.get("spec") != "Медицинская оптика" and data.get("spec") != "Фармация":
			# print(data.get('pp'))
			try:
				source_json = load_json(f"module\\template_generator\\source\\expertnayaCep_Medsestry_nmo",f"{data.get('spec')}.json")
				li = list()
				for i,s_data in enumerate(source_json):
					if data.get("spec") == s_data.get('specname'):
						# print(s_data.get("name"))
						# if s_data.get('programs')[i].get("hour") == 0:
						# 	log.warning(f"hour = {s_data.get('program_data').get('hour')}| main_spec: {data.get('spec')} and in prog specname: {s_data.get('program_data').get('name')} id: {s_data.get('program_data').get('id')} {s_data.get('program_data').get('final_url')}")

						# li.append(s_data.get("programs"))
						context = {
							"specname": data.get("spec"),
							"progs": s_data.get("programs")
						}
				print(context)
				save_html_with_template("module\\template_generator\\ready\\expertnayaCep_Medsestry\\nmo",f"[НМО] [Медсестры] {data.get('spec')}.html",template, context)
			except Exception as e:
				print(data.get("spec"), e)
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
	build_jina_template()
	# build_json()
if __name__ == "__main__":
	main()
