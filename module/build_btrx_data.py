from datetime import date
import os
import sys
sys.path.append('/')
from btrx import get_all_data,check_product,get_product_list,save_to_json,load_from_jsonFile
from parsersearchsite import searchInSite, getProgramUrl
from html_pars import parserhtml
from colorama import Fore,Back,Style
product_id = 'empty'
product_spec = 'empty'
product_name = 'empty'
product_price = 'empty'
product_hour = 'empty'
product_linkNmo = 'empty'
product_url = 'empty'

def makefileWdateName() -> str:
	"""
	[0] = str(fileNameWithPath)
	[1] = str(filename)

	Returns:
		tuple: [fileNameWithPath,filename]
	"""
	today = date.today()
	cur_date = today.strftime("%d.%m.%Y")
	filename = f'{cur_date}_file.json'
	path = os.getcwd() + "\\data\\json\\btrx_data"
	filenameWcurDate = f"{path}\{filename}"
	return str(filenameWcurDate), str(filename)

def getBtrxData():
	global product_id,product_spec,\
	product_name,product_price,product_hour,\
	product_linkNmo,product_url
	btrx_list = []
	path = os.getcwd() + "\\data\\json\\btrx_data"
	if os.path.exists(makefileWdateName()[0]):
		loaded_data = load_from_jsonFile(makefileWdateName()[0],path)
		loaded_hour = None
		for data in loaded_data[2:5]:
			if data['ID'] != '' or data['ID'] != None:
				product_id = data['ID']
			else:
				product_id = None
			if data['NAME'] != '' or data['NAME'] != None:
				product_name = data['NAME']
			else:
				product_name = None
			if data['PRICE'] != '' or data['PRICE'] != None:
				product_price = data['PRICE']
				try:
					if '.00' in product_price:
						product_price = product_price.replace('.00','')
					elif '.000' in product_price:
						product_price = product_price.replace('.000','')
					else:
						product_price = data['PRICE']
				except Exception as e:
					product_price = data['PRICE']
					print(e)
			else:
				product_price = None

			if data['PROPERTY_213'] != None:
				loaded_hour = data['PROPERTY_213']
				product_hour = loaded_hour['value']
				if product_hour != '' or product_hour != None:
					product_hour=loaded_hour['value']
				else:
					product_hour = None
			else:
				product_hour = None
			dictData = {
						'id': product_id,
						'spec': product_spec,
						'name': product_name,
						'price': product_price,
						'hour': product_hour,
						'linkNmo': product_linkNmo,
						'url': product_url
				}
			btrx_list.append(dictData)
	else:
		saved_data = save_to_json(get_product_list(),makefileWdateName()[1],path)
		loaded_hour = None
		for data in saved_data[2:5]:
			if data['ID'] != '' or data['ID'] != None:
				product_id = data['ID']
			else:
				product_id = None
			if data['NAME'] != '' or data['NAME'] != None:
				product_name = data['NAME']
			else:
				product_name = None
			if data['PRICE'] != '' or data['PRICE'] != None:
				product_price = data['PRICE']

				if '.00' in product_price:
					product_price = product_price.replace('.00','')
				elif '.000' in product_price:
					product_price = product_price.replace('.000','')
				else:
					product_price = data['PRICE']
			else:
				product_price = None

			if data['PROPERTY_213'] != None:
				loaded_hour = data['PROPERTY_213']
				product_hour = loaded_hour['value']
				if product_hour != '' or product_hour != None:
					product_hour=loaded_hour['value']
				else:
					product_hour = None
			else:
				product_hour = None
			dictData = {
						'id': product_id,
						'spec': product_spec,
						'name': product_name,
						'price': product_price,
						'hour': product_hour,
						'linkNmo': product_linkNmo,
						'url': product_url
				}
			btrx_list.append(dictData)
	return btrx_list

def buildjsondata():
	global product_id,product_spec,\
	product_name,product_price,product_hour,\
	product_linkNmo,product_url
	btrx_data = getBtrxData()
	site_list = []
	print(Back.WHITE+Fore.BLUE+f'{btrx_data}'+Fore.RESET+Back.RESET)
	for data_btrx in btrx_data[2:5]:
		product_id = data_btrx['id']
		if product_id == '' or product_id == None:
			product_id == None
		else:
			product_id = data_btrx['id']
		product_name = data_btrx['name']
		product_name = product_name.lower()
		if product_name == '' or product_name == None:
			product_name == None
		else:
			product_name = data_btrx['name']
			product_name = product_name.lower()
		product_spec = data_btrx['spec']
		if product_spec == '' or product_spec == None:
			product_spec == None
		else:
			product_spec = data_btrx['spec']
		product_price = data_btrx['price']
		if product_price == '' or product_price == None:
			product_price == None
		else:
			product_price = data_btrx['price']
		product_hour = data_btrx['hour']
		if product_hour == '' or product_hour == None:
			product_hour == None
		else:
			product_hour = data_btrx['hour']
		product_linkNmo = data_btrx['linkNmo']
		if product_linkNmo == '' or product_linkNmo == None:
			product_linkNmo == None
		else:
			product_linkNmo = data_btrx['linkNmo']
		site_dictData = {
						'id': product_id,
						'spec': product_spec,
						'name': product_name,
						'price': product_price,
						'hour': product_hour,
						'linkNmo': product_linkNmo,
						'url': product_url
				}
		searchInSite(product_name)
		program_url_data = getProgramUrl(product_name,product_price)
		program_url_name = program_url_data['name']
		program_url_name = program_url_name.lower()
		program_url_price = program_url_data["price"]
		program_url_url = program_url_data['url']

		if product_name in program_url_name:
			if product_price in program_url_price or program_url_price in product_price:
				if product_price == program_url_price:
					print(program_url_data['name'], product_name)
					if program_url_url != '' or program_url_url != None:
						if program_url_data['hour'] == product_hour:
							print(program_url_data['hour'], product_hour)
							product_url = program_url_url
						else:
							print(f'hour not match: site:{program_url_data["hour"]} btrx:{product_hour}')
							print(site_dictData)
				else:
					print('Error with price')
		site_dictData = {
						'id': product_id,
						'spec': product_spec,
						'name': product_name,
						'price': product_price,
						'hour': product_hour,
						'linkNmo': product_linkNmo,
						'url': product_url
				}
if __name__ == "__main__":
	buildjsondata()