import sys
from time import sleep
from random import uniform
from jinja2 import Environment, select_autoescape, FileSystemLoader
import os
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

def save_json(data:list[dict],path: str,file_name: str):
	with open(os.path.join(f"{os.getcwd()}\\{path}",file_name),'w',encoding='utf-8') as f:
		json.dump(data,f,ensure_ascii=False,indent=4)

def load_json(path: str,file: str) -> list[dict[str,str|int|list[str]]]:
	with open(os.path.join(f"{os.getcwd()}\\{path}",file),'r',encoding='utf-8') as f:
		data: list[dict[str,str|int|list[str]]] = json.loads(f.read())
	return data

def load_template(template_name:str,ext:str):
	env = Environment(loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__)),
	autoescape=select_autoescape([f'{ext}']))
	return env.get_template(f"{template_name}.{ext}")

def build():
	source_json = load_json(f"data\\json\\docx_converted","docxtojson.json")
	# ###
	class SourceData(BaseModel):
		spec: Optional[StrictStr] = None
		job: Optional[list[str]] = None
		pp: Optional[list[str]] = None
	# ###

	for source_jdata in source_json:
		list_data = list()
		source_data = SourceData()
		source_data.spec = source_jdata.get('spec')
		source_data.job = source_jdata.get('job')
		source_data.pp = source_jdata.get('pp')
		for jobs in source_data.job:
			print(jobs)

		for pps in source_data.pp:
			dict_data = dict()
			finder=search(pps,20000,"ПП")
			print(f"title: {pps} finder_items: {finder.__len__()}")

			if finder:
				dict_data ={
				"specname": source_data.spec,
				"program_data": finder[0]
				}
				list_data.append(dict_data)
		save_json(list_data,"module\\template_generator\\source\\expertnayaCep_Mdesestry_pp",f"{source_data.spec}.json")

def build_jina_template():
	source_json = load_json(f"data\\json\\docx_converted","docxtojson.json")

def main():
	# load_json(f"data\\json\\docx_converted","docxtojson.json")
	# print(load_template("expertnayaCep_Mdesestry_pp","html"))
	# print(sys.path)
	# search()
	build()

if __name__ == "__main__":
	main()
