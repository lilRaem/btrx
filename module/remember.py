import os, json,sys
sys.path.insert(0,os.getcwd())
from req.params import *
from module.parsersearchsite import getProgramUrl
from module.config import FinalData
class Remember():
	def __init__(self) -> None:
		super().__init__()

	def remember(self,obj,name):
		# print(obj)
		# print(type(obj))
		new: list = obj
		if os.path.exists(f"data/cached_items/{name}"):
			obj = self.load(name)
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

	def save(self,obj,name:str):
		with open(f"data/cached_items/{name}.json","w", encoding="utf-8") as file:
			if type(obj) == list:
				json.dump(obj,file,ensure_ascii=False,indent=4)
			else:
				file.write(obj)
			file.close()
		print(f"save {name}")
		return obj

	def load_(self,name):
		obj = None
		with open(f"data/cached_items/{name}.json","r", encoding="utf-8") as file:
			try:
				obj: list = json.loads(file.read())
			except:
				obj = file.read()
			file.close()
		# print(f"upd load {name}")
		return obj

	def load(self,name:str) -> list:
		obj = None
		#if os.path.exists(f"data/cached_items/{name}.json"):
		with open(f"data/cached_items/{name}.json","r", encoding="utf-8") as file:
			try:
				obj: list = json.loads(file.read())
				#print("obj: ",obj)
			except Exception as e:
				print('load error: ',e)
				obj = json.loads(file.read())
			file.close()
		#else:
		#	os.makedirs("data/cached_items",exist_ok=True)
		#	with open(f"data/cached_items/{name}.json","w", encoding="utf-8") as file:
		#		file.write([])
		#		file.close()
		#	with open(f"data/cached_items/{name}.json","r", encoding="utf-8") as file:
		#		try:
		#			if type(obj) == list:
		#				obj: list = json.loads(file.read())
		#				print(obj)
		#		except Exception as e:
		#			obj = []
		#			print(e)
		#		file.close()
		print(f"load {name}")
		return obj

	def update(self,obj,name):
		print("update and")
		obj = self.save(obj,name)
		return obj

def load_json() -> list[dict]:
	with open("data/json/btrx_data/_23.02.2024_file.json","r",encoding="utf-8") as f:
		data = json.load(f)
	return data

if __name__ == "__main__":

	new = list()
	rem = Remember()
	for prog in load_json():
		fresh_prog = FinalData()
		fresh_prog.id = prog.get("ID")
		fresh_prog.name = prog.get('NAME').lower()
		fresh_prog.fullname = f"Курс {prog.get('NAME').lower()}"
		fresh_prog.price = int(prog.get("PRICE").replace('.00',''))
		#print("fresh: ",fresh_prog)
		if prog:
			prog_url: list[dict] = list()
			if prog.get("PROPERTY_213"):
				try:
					fresh_prog.hour = int(prog['PROPERTY_213']['value'])
				except:
					fresh_prog.hour = prog['PROPERTY_213']['value']
					#print(f"{fresh_prog.id}\n{fresh_prog.name}\nhas string ({fresh_prog.hour}) hour or error")
			else:
				fresh_prog.hour = None

			#if os.path.exists("data/cached_items"):
			#	with open("data/cached_items/listtest.json","w",encoding="utf-8") as f:
			#		json.dump(new, f,ensure_ascii=False,indent=4)
			#else:
			#	os.makedirs('data/cached_items/errors')
			#	with open("data/cached_items/listtest.json","w",encoding="utf-8") as f:
			#		json.dump(new, f,ensure_ascii=False,indent=4)

			for l_prog in rem.load("test"):
				cached_prog = FinalData()
				cached_prog.id = l_prog.get("id")
				cached_prog.katalog = l_prog.get("katalog")
				cached_prog.name = l_prog.get("name")
				cached_prog.fullname = l_prog.get("fullname")
				cached_prog.price = l_prog.get("price")
				cached_prog.hour = l_prog.get("hour")
				cached_prog.nmoSpec = l_prog.get("nmoSpec")
				cached_prog.linkNmo = l_prog.get("linkNmo")
				cached_prog.url = l_prog.get("url")
				cached_prog.final_url = l_prog.get("final_url")

				if fresh_prog.fullname == l_prog.get("name"):
					if int(fresh_prog.price) == int(cached_prog.price):
						if not fresh_prog.hour: fresh_prog.hour = int(cached_prog.hour)
						if fresh_prog.hour == cached_prog.hour:
							prog_url.append(cached_prog.model_dump())
					#else:
					#	print("cached: ",cached_prog,"fresh: ",fresh_prog)
			if not prog_url:
				prog_url = getProgramUrl(fresh_prog.name,fresh_prog.price)
			#print("prog_url: ",prog_url)
			if prog_url:
				for p_url in prog_url:
					print(p_url)
					if fresh_prog.fullname == p_url.get("name"):
						if int(fresh_prog.price) == int(p_url.get("price")):
							if not fresh_prog.hour: fresh_prog.hour = int(p_url.get("hour"))
							if fresh_prog.hour == p_url.get("hour"):
								p_url['id'] = int(fresh_prog.id)
								new.append(p_url)
								rem.remember(new,'test')