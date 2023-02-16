from datetime import date
from typing import Optional
from pydantic import BaseModel, StrictStr, StrictInt, StrictBool

# Main types of search data Program:
class FinalData(BaseModel):
	id: Optional[StrictStr] = None
	spec: Optional[StrictStr] = None
	name: Optional[StrictStr] = None
	price: Optional[StrictStr] = None
	hour: Optional[StrictStr] = None
	nmoSpec: Optional[StrictStr] = None
	linkNmo: Optional[StrictStr] = None
	url: Optional[StrictStr] = None

# Main types of search data UserData:
class UserData(BaseModel):
	id: Optional[StrictInt] = None
	name: Optional[StrictStr] = None
	email: dict
	department: Optional[StrictStr] = None
	position: Optional[StrictStr] = None
	inner_phone: dict
	is_active: Optional[StrictBool] = None
	last_check_datetime: dict

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

# Main Bitrix config:
class BtrxConfig():
	id = "di28gta836z3xn50"

# Parse soup config:
class ParseSiteConfig():

	soupMainBlock = "courses-block"
	soupName = ("h1", "main-title")
	soupHour = ("div", "items-box-block__element-type-item")
	soupPrice = ("div", "course-info-block__action-buy-price")

	headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/51.0'
    }

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