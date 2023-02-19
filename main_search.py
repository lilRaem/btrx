import os
from time import time
from module.config import FinalData, makefileWdateName, ParseSiteConfig
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

def search(search_name:str, search_price:int) -> list|None:
	if type(search_price) != int:
		TypeError(f"Type of search_price == int\n now: {type(search_price)}")
	fdata: list[dict[str,str|int|None]] = list()
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
		if json_check_data:
			count_check_data = json_check_data.__len__()
		else:
			print('item not exist')

		if count_check_data == 1:


			# for d in progUrl_data:
			# 	count_getProgramUrl += 1

			for _final_data in json_check_data:
				final_data = FinalData()
				final_data.id = int(_final_data.get('id'))
				final_data.name = _final_data.get('name')
				if _final_data.get('price'):
					final_data.price = int(_final_data.get('price'))
				else:
					final_data.price = None
				if _final_data.get('hour'):
					final_data.hour = int(_final_data.get('hour'))
				else:
					final_data.hour = None
				final_data.linkNmo = _final_data.get('linkNmo')
				try:
					progUrl_data = getProgramUrl(final_data.name, final_data.price)
					count_getProgramUrl = progUrl_data.__len__()
					if progUrl_data: print(f"Length of url_list: {count_getProgramUrl}")
					if count_getProgramUrl == 1:
						final_data.url = progUrl_data[0].get('url')
						if not _final_data.get('hour'):
							final_data.hour = int(progUrl_data[0].get('hour'))
					else:
						if progUrl_data:
							for d in progUrl_data:
								if final_data.name.lower() == d.get("name").replace("Курс ","").lower():
									if d.get('price'):
										if final_data.price == int(d.get('price')):
											final_data.url = d.get('url')
									if not final_data.hour:
										final_data.hour = int(d.get('hour'))
				except Exception as e:
					progUrl_data = None
					print(Fore.RED+f"get progUrl_data() error:\n{e}"+Fore.RESET)

			print("\n" + Fore.GREEN + f'{final_data.json(encoder="utf-8",ensure_ascii=False)}')
			fdata.append(final_data.dict())
		else:
			if json_check_data != None:
				for val_data in json_check_data:
					final_data = FinalData()
					final_data.id = int(val_data.get('id'))
					final_data.name = val_data.get('name')
					if val_data.get('price'):
						final_data.price = int(val_data.get('price'))
					else:
						final_data.price = None
					final_data.linkNmo = val_data.get('linkNmo')
					try:
						progUrl_data = getProgramUrl(final_data.name, final_data.price)
					except Exception as e:
						progUrl_data = None
						print(Fore.RED+f"get progUrl_data() error:\n{e}"+Fore.RESET)
					try:
						final_data.hour = val_data.get('hour')
					except Exception as e:
						if progUrl_data:
							final_data.hour = progUrl_data[0].get('hour')
						print(Fore.RED+f"val_data.get('hour') error:\n{e}"+Fore.RESET)
					if progUrl_data:
						for v in progUrl_data:
							if v.get('price'):
								final_data.url = v.get('url')
							if int(v.get('hour')) == final_data.hour:
								pass
							else:
								if final_data.hour == None and final_data.price == v.get('price'):
									final_data.hour = int(v.get('hour'))
					print("\n" + Fore.GREEN + f'{final_data.json(encoder="utf-8",ensure_ascii=False)}' + Fore.RESET)
					fdata.append(final_data.dict())
		if fdata:
			for vv in fdata:
				if vv.get('price') == search_price:
					print(Fore.WHITE+f"\n{Back.GREEN}*****\n{Style.DIM}id: {vv.get('id')}\nname: {vv.get('name')}\nprice: {vv.get('price')}\nhour: {vv.get('hour')}\n{vv.get('url')}"+Fore.RESET+Back.RESET)
					print(Fore.CYAN+f"\n{vv.get('url')}?program={vv.get('name')}&header=Курс {vv.get('name')}&cost={vv.get('price')}&tovar={vv.get('id')}&sendsay_email="+"${ Recipient.Email }"+Fore.RESET)
				else:
					print(Fore.WHITE+f"\n{Back.LIGHTGREEN_EX}*****\n{Style.DIM}id: {vv.get('id')}\nname: {vv.get('name')}\nprice: {vv.get('price')}\nhour: {vv.get('hour')}\n{vv.get('url')}"+Fore.RESET+Back.RESET)
					print(Fore.CYAN+f"\n{vv.get('url')}?program={vv.get('name')}&header=Курс {vv.get('name')}&cost={vv.get('price')}&tovar={vv.get('id')}&sendsay_email="+"${ Recipient.Email }"+Fore.RESET)
			return fdata
	else:
		btrx.save_to_json(btrx.get_product_list(), makefileWdateName(path)[1], path)
		data = btrx.load_from_jsonFile(makefileWdateName(path)[1],path)
		btrx.check_product(search_name, search_price, btrx.get_all_data(data))
	print('\n'+Fore.MAGENTA+f"(main.py) Search time: {round(time()-start,2)} sec"+ Fore.RESET)

if __name__ == "__main__":
	start = time()
	# data = search("Онкология",0)
	# with open("data.json","w", encoding="utf-8") as file:
	# 	file.write(json.dump(data,file,indent=4,ensure_ascii=False,sort_keys=True,default=list[dict]))
	# p = Btrx()
	# path = "data\\json\\btrx_data"
	# data = p.load_from_jsonFile(makefileWdateName(path)[1],path)
	try:
		prgog = searchInSite(search_key="Онкология",price=None)
	except:
		prgog = 0
	print("\nmain_search: "+f"{prgog.__len__()}")
	print(Fore.MAGENTA+f'Main time: {round(time()-start,2)} sec'+ Fore.RESET)
	# buildjsondata()
	# print(datalist)d:\Program\Microsoft VS Code\resources\app\out\vs\code\electron-sandbox\workbench\workbench.html
	# class DataData(BaseModel):
	# 	id: Optional[StrictStr] = None
	# data_data = DataData()
	# id = data_data.id
	# id = 'ss'
	# print(data_data)
