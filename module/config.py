from datetime import date
from typing import Optional
from pydantic import BaseModel, StrictStr

class FinalData(BaseModel):
	id: Optional[StrictStr] = None
	spec: Optional[StrictStr] = None
	name: Optional[StrictStr] = None
	price: Optional[StrictStr] = None
	hour: Optional[StrictStr] = None
	nmoSpec: Optional[StrictStr] = None
	linkNmo: Optional[StrictStr] = None
	url: Optional[StrictStr] = None


def makefileWdateName(path:str) -> str:
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