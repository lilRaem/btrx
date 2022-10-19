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