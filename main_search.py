import os
from time import time
import json
from module.config import FinalData, makefileWdateName
from colorama import Fore, Back, Style
from module.btrx import Btrx
# from module.build_btrx_data import buildjsondata
from module.parsersearchsite import searchInSite, getProgramUrl
"""
#TODO Был изменен поиск в parserhtml.py, есть ошибки, надо  исправить
[ ] parser.html: Начал брать цену в зависимости от наличия перечеркнутой (старой) цены
[ ] ошибка При поиске несуществующей программы final_data.id = json_check_data['id'] TypeError: list indices must be integers or slices, not str line 80
"""

datalist = []


def search(search_name:str, search_price:str) -> list|None:
	fdata = []
	start = time()
	btrx = Btrx()
	search_name = search_name.strip()
	search_name = search_name.replace('\n', '')
	search_name = search_name.replace('  ', ' ')
	# name = input('Введите название программы: ')
	path = "data\\json\\btrx_data"
	final_data = FinalData()
	print(Fore.YELLOW + 'Path exists?: ', os.path.exists(makefileWdateName(path)[0]),
		makefileWdateName(path)[0] + Back.RESET)
	if (os.path.exists(makefileWdateName(path)[0])):
		data = btrx.load_from_jsonFile(makefileWdateName(path)[1], path)
		json_check_data = btrx.check_product(search_name, search_price, btrx.get_all_data(data))
		searchInSite(search_name)
		count_check_data = 0
		if json_check_data != None:
			for chck_data in json_check_data:
				count_check_data = count_check_data + 1
		else:
			print('item not exist')
		if json_check_data != None and count_check_data == 1:
			progUrl_data = getProgramUrl(search_name, search_price)
			count_getProgramUrl = 0
			# for d in progUrl_data:
			# 	count_getProgramUrl += 1

			print(f"Length of url_list: {progUrl_data.__len__()}")
			for i,_final_data in enumerate(json_check_data):
				final_data = FinalData()
				final_data.id = _final_data['id']
				final_data.name = _final_data['name']
				final_data.price = _final_data['price']
				final_data.hour = _final_data['hour']
				final_data.linkNmo = _final_data['linkNmo']
				if count_getProgramUrl == 1:
					final_data.url = progUrl_data[0]['url']
					if _final_data['hour'] == None:
						final_data.hour = progUrl_data[0]['hour']
				else:
					for d in progUrl_data:
						if final_data.name.lower() == d['name'].replace("Курс ","").lower():
							if final_data.price == d['price']:
								final_data.url = d['url']
							if final_data.hour == None:
								final_data.hour = d['hour']
			print("\n" + Fore.GREEN + f'{final_data.json(encoder="utf-8",ensure_ascii=False)}')
			fdata.append(final_data.json(encoder="utf-8",ensure_ascii=False))
		else:
			if json_check_data != None:
				for iter_data, val_data in enumerate(json_check_data):
					final_data = FinalData()
					final_data.id = json_check_data[iter_data]['id']
					final_data.name = json_check_data[iter_data]['name']
					final_data.price = json_check_data[iter_data]['price']
					final_data.linkNmo = json_check_data[iter_data]['linkNmo']
					progUrl_data = getProgramUrl(final_data.name, final_data.price)
					try:
						final_data.hour = json_check_data[iter_data]['hour']
					except:
						final_data.hour = progUrl_data['hour']
					for i,v  in enumerate(progUrl_data):
						if v['price']:
							final_data.url = v['url']
						if v['hour'] == final_data.hour:
							pass
						else:
							if final_data.hour == None and final_data.price == v['price']:
								final_data.hour = v['hour']
					print("\n" + Fore.GREEN + f'{final_data.json(encoder="utf-8",ensure_ascii=False)}' + Fore.RESET)
					fdata.append(final_data.json(encoder="utf-8",ensure_ascii=False))
		if fdata:
			for v in fdata:
				vv = json.loads(v)
				if vv['price'] == search_price:
					print(Fore.WHITE+f"\n{Back.GREEN}*****\n{Style.DIM}id: {vv['id']}\nname: {vv['name']}\nprice: {vv['price']}\nhour: {vv['hour']}\n{vv['url']}"+Fore.RESET+Back.RESET)
					print(Fore.CYAN+f"\n{vv['url']}?program={vv['name']}&header=Курс {vv['name']}&cost={vv['price']}&tovar={vv['id']}&sendsay_email="+"${ Recipient.Email }"+Fore.RESET)
				else:
					print(Fore.WHITE+f"\n{Back.LIGHTGREEN_EX}*****\n{Style.DIM}id: {vv['id']}\nname: {vv['name']}\nprice: {vv['price']}\nhour: {vv['hour']}\n{vv['url']}"+Fore.RESET+Back.RESET)
					print(Fore.CYAN+f"\n{vv['url']}?program={vv['name']}&header=Курс {vv['name']}&cost={vv['price']}&tovar={vv['id']}&sendsay_email="+"${ Recipient.Email }"+Fore.RESET)
			return fdata
	else:
		btrx.save_to_json(btrx.get_product_list(), makefileWdateName(path)[1], path)
		data = btrx.load_from_jsonFile(makefileWdateName(path)[1],path)
		btrx.check_product(search_name, search_price, btrx.get_all_data(data))
	print('\n'+Fore.MAGENTA+f"(main.py) Search time: {round(time()-start,2)} sec"+ Fore.RESET)

if __name__ == "__main__":
	start = time()
	search()
	print(Fore.MAGENTA+f'Main time: {round(time()-start,2)} sec'+ Fore.RESET)
	# buildjsondata()
	# print(datalist)d:\Program\Microsoft VS Code\resources\app\out\vs\code\electron-sandbox\workbench\workbench.html
	# class DataData(BaseModel):
	# 	id: Optional[StrictStr] = None
	# data_data = DataData()
	# id = data_data.id
	# id = 'ss'
	# print(data_data)
