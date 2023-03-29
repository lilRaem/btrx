import os
from time import time
from module.config import FinalData, makefileWdateName, ParseSiteConfig
from colorama import Fore, Back, Style
from module.btrx import Btrx
# from module.build_btrx_data import buildjsondata
from module.parsersearchsite import searchInSite, getProgramUrl
from module.html_pars.parserhtml import parseSiteUrl
"""
# TODO Был изменен поиск в parserhtml.py, есть ошибки, надо  исправить
- [ ] parser.html: Начал брать цену в зависимости от наличия перечеркнутой (старой) цены
"""

datalist = []

def search(search_name:str, search_price:int, type_programm:str,mail_service:str="mindbox") -> list|None:
	if type(search_price) != int:
		TypeError(f"Type of search_price == int\n now: {type(search_price)}")
	fdata: list[dict[str,str|int|None]] = list()
	start = time()
	btrx = Btrx()
	search_name = search_name.strip()
	search_name = search_name.replace('\n', ' ')
	search_name = search_name.replace('  ', ' ')
	# name = input('Введите название программы: ')
	path = "data\\json\\btrx_data"
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
			for _final_data in json_check_data:

				final_data = FinalData()

				if _final_data.get('id'): final_data.id = int(_final_data.get('id'))
				if _final_data.get('name'): final_data.name = _final_data.get('name').strip()

				if _final_data.get('price'): final_data.price = int(_final_data.get('price'))
				if _final_data.get('hour'): final_data.hour = int(_final_data.get('hour'))

				if final_data.name and final_data.price:
					progUrl_data = getProgramUrl(final_data.name, final_data.price)

					if progUrl_data: print(f"Length of progUrl_data: {progUrl_data.__len__()}")
					else: print(f"Length of progUrl_data: {None}")

					if progUrl_data.__len__() == 1:
						for data in progUrl_data:
							final_data.url = data.get('url')
							if not final_data.spec: final_data.spec = data.get('spec')
							if not final_data.type_zdrav: final_data.type_zdrav = data.get('type_zdrav')
							if not final_data.hour: final_data.hour = int(data.get('hour'))
					else:
						if progUrl_data:
							for data in progUrl_data:
								if final_data.name.lower().strip() == data.get("name").replace("Курс ","").lower().strip():
									if data.get('price'):
										if int(data.get('price')) == final_data.price:
											final_data.url = data.get('url')
										if data.get('type_zdrav'):
											if int(data.get('price')) == final_data.price:
												final_data.type_zdrav = data.get('type_zdrav')
											# final_data.spec = data.get('spec') # без цены подставляет spec из последнего элемента списка progUrl_data
										if data.get('spec'):
											if int(data.get('price')) == final_data.price:
												final_data.spec = data.get('spec')
										if not final_data.hour:
											if int(data.get('price')) == final_data.price:
												final_data.hour = int(data.get('hour'))
			print("\n" + Fore.GREEN + f'{final_data.json(encoder="utf-8",ensure_ascii=False)}')
			fdata.append(final_data.dict())
		else:
			if json_check_data != None:
				for val_data in json_check_data:
					final_data = FinalData()
					final_data.id = int(val_data.get('id'))
					final_data.name = val_data.get('name').strip()
					final_data.spec = val_data.get('spec')
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
							# if v.get('type_zdrav'): final_data.type_zdrav = v.get('type_zdrav')
							if v.get('spec'): final_data.spec = v.get('spec')
							# if v.get('price'): final_data.url = v.get('url')
							# if v.get('url'): final_data.url = v.get('url')

							if int(v.get('hour')) == final_data.hour:
								final_data.hour = int(v.get('hour'))
							else:
								if final_data.hour == None and int(final_data.price) == int(v.get('price')):
									final_data.hour = int(v.get('hour'))
							if final_data.name.lower() in v.get('name').lower():
								if int(final_data.price) == int(v.get('price')):
									final_data.url = v.get('url')
									if v.get('type_zdrav'): final_data.type_zdrav = v.get('type_zdrav')
					print("\n" + Fore.GREEN + f'{final_data.dict()}' + Fore.RESET)
					fdata.append(final_data.dict())
		if fdata:
			for vv in fdata:

				if mail_service == "mindbox":
					user_email = "${ Recipient.Email }"
				elif mail_service == "sendsay":
					user_email = "[% anketa.member.email %]"
				else:
					user_email = None
				if vv.get('price') == search_price:

					if vv.get("spec") == "Профессиональная переподготовка":
						type_programm = "ПП"
					elif vv.get("spec") == "Повышение квалификации":
						type_programm = "ПК"
					elif vv.get("spec") == "Повышение квалификации (НМО)":
						type_programm = "НМО"
					else:
						type_programm = None

					print(Fore.WHITE+f"\n{Back.GREEN}*****\n{Style.DIM}id: {vv.get('id')}\ntype_zdrav: {vv.get('type_zdrav')}\nname: {vv.get('name')}\nspec: {vv.get('spec')}\nprice: {vv.get('price')}\nhour: {vv.get('hour')}\n{vv.get('url')}"+Fore.RESET+Back.RESET)
					print(Fore.CYAN+f"\n{vv.get('url')}?program={vv.get('name')}&header=Курс {type_programm} {vv.get('name')}&cost={vv.get('price')}&tovar={vv.get('id')}&sendsay_email="+f"{user_email}"+Fore.RESET)
				else:
					if vv.get("spec") == "Профессиональная переподготовка":
						type_programm = "ПП"
					elif vv.get("spec") == "Повышение квалификации":
						type_programm = "ПК"
					elif vv.get("spec") == "Повышение квалификации (НМО)":
						type_programm = "НМО"
					else:
						type_programm = None
					print(Fore.WHITE+f"\n{Back.LIGHTGREEN_EX}*****\n{Style.DIM}id: {vv.get('id')}\ntype_zdrav: {vv.get('type_zdrav')}\nname: {vv.get('name')}\nspec: {vv.get('spec')}\nprice: {vv.get('price')}\nhour: {vv.get('hour')}\n{vv.get('url')}"+Fore.RESET+Back.RESET)
					print(Fore.CYAN+f"\n{vv.get('url')}?program={vv.get('name')}&header=Курс {type_programm} {vv.get('name')}&cost={vv.get('price')}&tovar={vv.get('id')}&sendsay_email="+f"{user_email}"+Fore.RESET)
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
	a = 1
	parseSiteUrl(parseurl="https://apkipp.ru/katalog/zdravoohranenie-srednij-medpersonal/kurs-sovremennyie-aspektyi-akusherskoj-pomoschi-v-rodovspomogatelnyih-uchrezhdeniyah/")

	print(Fore.MAGENTA+f'Main time: {round(time()-start,2)} sec'+ Fore.RESET)
	# buildjsondata()
	# print(datalist)d:\Program\Microsoft VS Code\resources\app\out\vs\code\electron-sandbox\workbench\workbench.html
	# class DataData(BaseModel):
	# 	id: Optional[StrictStr] = None
	# data_data = DataData()
	# id = data_data.id
	# id = 'ss'
	# print(data_data)
