from datetime import date
from typing import Optional
from pydantic import BaseModel, StrictStr, StrictInt, StrictBool
from random import choice
import time
import os
# Main types of search data Program:
class FinalData(BaseModel):
	id: Optional[StrictInt] = None
	type_zdrav: Optional[StrictStr] = None
	spec: Optional[StrictStr] = None
	name: str|Optional[StrictStr] = None
	price: Optional[StrictInt] = None
	hour: Optional[StrictInt] = None
	nmoSpec: Optional[StrictStr] = None
	linkNmo: Optional[StrictStr] = None
	url: Optional[StrictStr] = None
	final_url: Optional[StrictStr] = None


# Main types of search data UserData:
class UserInnerPhoneData(BaseModel):
	inner_phone: Optional[StrictInt] = None
	zdr_phone: Optional[StrictStr] = None
	password: Optional[StrictStr] = None

class UserEmailData(BaseModel):
	email: Optional[StrictStr] = None
	password: Optional[StrictStr] = None

class LastCheckDatetimeData(BaseModel):
	date: Optional[StrictStr] = None
	time: Optional[StrictStr] = None

class UserData(BaseModel):
	id: Optional[StrictInt] = None
	name: Optional[StrictStr] = None
	email: UserEmailData() = None
	department: Optional[StrictStr] = None
	position: Optional[StrictStr] = None
	inner_phone: UserInnerPhoneData() = None
	is_active: Optional[StrictBool] = None
	last_check_datetime: LastCheckDatetimeData() = None

# Main Bitrix config:
class BtrxConfig():
	id = "di28gta836z3xn50"

# Parse soup config:
class ParseSiteConfig():

	link = "https://apkipp.ru"

	soupMainBlock = "courses-block"
	soupName = ("h1", "main-title")
	soupHour = ("div", "items-box-block__element-type-item")
	soupPrice = ("div", "course-info-block__action-buy-price")

	headers = [
	{"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"},
	{"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"},
	{"User-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15'},
	{"User-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'},
	{"User-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'},
	{"User-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'},
	{"User-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'},
	]

	def get_headers(self) -> dict[str,str]: return choice(self.headers)

	def get_ApiUrl(self,search_key:str):
		"""get url with set link and search_key

		Args:
			search_key (str): word of search programm

		Returns:
			str: url with set link and word arg
		"""
		return f'{self.link}/api/v1/search/?search={search_key}&as_phrase=true'

def makefileWdateName(path:str) -> tuple[str,str]:
	"""
	[0] = str(fileNameDateWithPath)
	[1] = str(filename)

	Returns:
		tuple(fileNameWithPath,filename)
	"""
	today = date.today()
	cur_date = today.strftime("%d.%m.%Y")
	filename = f'{cur_date}_file.json'
	filenameWcurDate = f"{filename}"
	return str(path+"\\"+filenameWcurDate), str(filename)

def timing_decorator(func):
	def wrapper(*args, **kwargs):
		start_time = time.time()
		result = func(*args, **kwargs)
		end_time = time.time()
		print(f"Function {func.__name__}() took {round(end_time - start_time,2)} seconds to run.")
		return result
	return wrapper

def memoize(func):
	cache = {}
	def wrapper(*args):
		print(**map(args))
		if args in cache:
			print(cache)
			return cache[args]
		else:
			result = func(*args)
			# cache[args] = result
			return cache[args]
	return wrapper