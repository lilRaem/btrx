import os, json,sys
sys.path.insert(0,os.getcwd())
from req.params import *
from module.parsersearchsite import getProgramUrl

class Remember():
	def __init__(self) -> None:
		super().__init__()

	def remember(self,obj,name):
		# print(obj)
		# print(type(obj))
		new: list = obj
		if os.path.exists(f"data/cached_items/{name}"):
			obj = self.load_(name)
			old = obj

			temp3 = []
			for element in new:
				if element not in old:
					temp3.append(element)
					# print(element)
					old.append(element)
			if temp3 != []:
				print("not equal")
				obj = old
				obj = self.save(obj,name)
		else:
			obj = self.save(obj,name)
		return obj

	def save(self,obj,name):
		with open(f"data/cached_items/{name}","w", encoding="utf-8") as file:
			if type(obj) == list:
				json.dump(obj,file,ensure_ascii=False,indent=4)
			else:
				file.write(obj)
			file.close()
		print(f"save {name}")
		return obj

	def load_(self,name):
		obj = None
		with open(f"data/cached_items/{name}","r", encoding="utf-8") as file:
			try:
				obj: list = json.loads(file.read())
			except:
				obj = file.read()
		# print(f"upd load {name}")
		return obj

	def load(self,name):
		obj = None
		with open(f"data/cached_items/{name}","r", encoding="utf-8") as file:
			try:
				obj: list = json.loads(file.read())
			except:
				obj = file.read()
		print(f"load {name}")
		return obj

	def update(self,obj,name):
		print("update and")
		obj = self.save(obj,name)
		return obj

def load_json() -> list[dict]:
    with open("data/json/btrx_data/19.07.2023_file.json","r",encoding="utf-8") as f:
        data = json.load(f)
    return data

if __name__ == "__main__":

    new = list()


    for prog in load_json()[505:510]:
        rem = Remember()
        fullname = f"Курс {prog.get('NAME').lower()}"
        price = int(prog.get("PRICE").replace('.00',''))
        if prog:
            prog_url: list[dict] = list()
            if prog.get("PROPERTY_213"):
                hour = int(prog['PROPERTY_213']['value'])
            else:
                hour = None
            for l_prog in rem.load("listtest"):
                if fullname == l_prog.get("name"):
                    if int(price) == int(l_prog.get("price")):
                        if not hour: hour = int(l_prog.get("hour"))
                        if hour == l_prog.get("hour"):
                            prog_url.append(l_prog)
            if not prog_url:
                prog_url = getProgramUrl(fullname,price)
            if prog_url:
                for p_url in prog_url:
                    if fullname == p_url.get("name"):

                        if int(price) == int(p_url.get("price")):
                            if not hour: hour = int(p_url.get("hour"))
                            if hour == p_url.get("hour"):
                                p_url['id'] = int(prog.get('ID'))
                                new.append(p_url)
                                rem.remember(new,'listtest')