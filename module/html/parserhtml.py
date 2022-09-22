from re import L
from time import sleep
from bs4 import BeautifulSoup
import os, json


def bs4pars():
	with open(f"{os.getcwd()}/module/html/templates/source/nmo_vo.html",'r',encoding='utf-8') as f:
		html = f.read()

	soup = BeautifulSoup(html,'lxml')
	pars_list = []
	pars_dict = {}
	for el in soup.find_all(class_='text-block'):
		# print("==={el.find('i','prog_altspecial').text}===")

		if el.find('b','prog_special').text != '':
			prog_special = el.find('b','prog_special').text.strip()
		else:
			prog_special = None
		if el.find('i','prog_altspecial').text != '':
			prog_altspecial = el.find('i','prog_altspecial').text.strip()
			prog_altspecial = prog_altspecial.replace('\n','')
			prog_altspecial = prog_altspecial.replace('\t','')
		else:
			prog_altspecial = None
		if el.find('a','prog_title').text != '':
			prog_title = el.find('a','prog_title').text.replace('\t','').replace('\n','')
		else:
			prog_title = None
		if el.find('span').next_element != '':
			prog_hour = el.find('span').next_element
		else:
			prog_hour = None
		if el.find('span').next_element.next_element.next_element.next_element.text != '':
			prog_price = el.find('span').next_element.next_element.next_element.next_element.text.replace('руб','').replace('\n','').replace('\t','').strip()
		else:
			prog_price = None

		pars_dict = {
			'prog_special': prog_special,
			'prog_altspecial': prog_altspecial,
			'prog_title': prog_title,
			'prog_hour': prog_hour,
			'prog_price': prog_price,
			'url': el.find('a','prog_title').get('href')
		}

		pars_list.append(pars_dict)
	print(pars_list)
	with open(f'{os.getcwd()}/module/html/templates/data.json','w',encoding='utf-8') as fp:
		json.dump(pars_list,fp,ensure_ascii=False,indent=4)
def main():
	bs4pars()


if __name__ == "__main__":
	main()