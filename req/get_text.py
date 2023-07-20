import json,sys,os
from pydantic import BaseModel,StrictStr,StrictInt
from typing import Optional
from params import list_course,check_600,check_300,forCheck600,forCheck300,already_600_300,types_prog,types_check
sys.path.insert(0,os.getcwd())
from module.parsersearchsite import getProgramUrl

class Course(BaseModel):
	id: Optional[int] = None
	hour: Optional[StrictInt] = None
	name: Optional[StrictStr] = None
	price: Optional[StrictInt] = None
	fullname: Optional[StrictStr] = None
	text: Optional[StrictStr] = None
	text_600: Optional[StrictStr] = None
	text_300: Optional[StrictStr] = None
	type: Optional[StrictStr] = None
	type_text: Optional[list[StrictStr]] = None
	spec: Optional[list[StrictStr]] = None
	spec_600: Optional[list[StrictStr]] = None
	spec_300: Optional[list[StrictStr]] = None
	all_600_300: Optional[list[StrictStr]] = None
	url: Optional[list[StrictStr]] = None

def load_json() -> list[dict]:
	with open("data/json/btrx_data/19.07.2023_file.json","r",encoding="utf-8") as f:
		data = json.load(f)
	return data

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

	def save(self,obj,name):
		with open(f"data/cached_items/{name}","w", encoding="utf-8") as file:
			if type(obj) == list:
				json.dump(obj,file,ensure_ascii=False,indent=4)
			else:
				file.write(obj)
			file.close()
		print(f"save {name}")
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

def main():
	print("start main")
	remem = Remember()
	list_treb_prog:list[Course] = list()
	programm_url = list()
	for prog in load_json():

		course = Course()
		course.id = int(prog.get("ID"))


		prog_fullname = "Курс "+prog.get("NAME").lower()
		course.fullname = prog_fullname
		course.name = course.fullname.replace("Курс ", "").capitalize()
		if prog.get("PROPERTY_213"):
			course.hour = int(prog.get("PROPERTY_213").get("value"))
		# print(course.name)
		if prog.get("PRICE"):
			course.price = int(prog.get("PRICE").replace(".00",""))


		try:
			programm_url_ = None
			load_prog = remem.load("listurl")
			for mem_prog in load_prog:
				if course.fullname == mem_prog.get('name'):
					print(course.fullname,"==",mem_prog.get('name'))
					if int(course.price) == int(mem_prog.get('price')):
						mem_prog['price'] = course.price
						if mem_prog.get("url"):
							programm_url_.append(mem_prog)
							print(programm_url_)

			# if programm_url == None:
			if not programm_url_:
				programm_url = getProgramUrl(course.name,course.price)
			print("try")
			for i,d in enumerate(programm_url):
				if course.fullname == programm_url[i].get('name'):
					print(course.fullname,"==",programm_url[i].get('name'))


					if int(course.price) == int(programm_url[i].get('price')):
						d['price'] = int(course.price)
						if d.get("url"):
							remem.remember(programm_url,"listurl")
		except Exception as e:
			print(e)
			try:
				programm_url = getProgramUrl(course.name,course.price)
			except:
				pass
			print("except")
			remem.remember(programm_url,"listurl")


		if course.fullname.lower() in list_course or course.fullname in list_course:
			for course_ in list_course:
				if course.fullname.lower() == course_.lower():
					course.name = course_.replace("Курс ", "").capitalize()
					if prog.get("PROPERTY_213"):
						if str(prog.get("NAME")).lower() in forCheck600 and int(prog.get("PROPERTY_213").get("value")) == 600:
							# course.hour = int(prog.get("PROPERTY_213").get("value"))
							# course.text = "в соответствии с приказом Минздрава России №707н от 08.10.2015 «Об утверждении Квалификационных требований к медицинским и фармацевтическим работникам с высшим образованием по направлению подготовки «Здравоохранение и медицинские науки» необходимо\nналичие подготовки в ординатуре или интернатуре по одной из специальностей:"
							course.text_600 = "в соответствии с приказом Минздрава России №707н от 08.10.2015 «Об утверждении Квалификационных требований к медицинским и фармацевтическим работникам с высшим образованием по направлению подготовки «Здравоохранение и медицинские науки» необходимо\nналичие подготовки в ординатуре или интернатуре по одной из специальностей:"
							# course.spec = check_600(course.fullname)
							course.spec_600 = check_600(course.fullname)
						elif str(prog.get("NAME")).lower() in forCheck300 and int(prog.get("PROPERTY_213").get("value")) == 300:
							# course.hour = int(prog.get("PROPERTY_213").get("value"))
							# course.text = "в соответствии с приказом Минздрава России №83н от 10.02.2016 «Об утверждении Квалификационных требований к медицинским и фармацевтическим работникам со средним медицинским и фармацевтическим образованием» необходимо наличие среднего профессионального образования по одной из специальностей:"
							course.text_300 = "в соответствии с приказом Минздрава России №83н от 10.02.2016 «Об утверждении Квалификационных требований к медицинским и фармацевтическим работникам со средним медицинским и фармацевтическим образованием» необходимо наличие среднего профессионального образования по одной из специальностей:"
							# course.spec = check_300(course.fullname)
							course.spec_300 = check_300(course.fullname)
					course.text = "в соответствии с приказом Минздрава России № 66н от 03.08.2012 «Об утверждении Порядка и сроков совершенствования медицинскими работниками и фармацевтическими работниками профессиональных знаний и навыков путем обучения по дополнительным профессиональным образовательным программам в образовательных и научных организациях» наличие опыта работы более 5 лет по одной из должностей:"
					course.all_600_300 = already_600_300(course.hour,course.fullname)
		else:
			try:
				if programm_url:
					for d_url in programm_url:
						course.url = str(d_url['url'])
						if course.fullname == d_url.get('name'):
							if course.price == d_url.get('price'):
								if not course.hour: course.hour = d_url['hour']
								if int(course.hour) == int(d_url['hour']):
									course.type = d_url['spec']
									if "Профессиональная переподготовка" == course.type:
										course_type = 1
									elif "Повышение квалификации" == course.type:
										course_type = 2
									elif "Повышение квалификации (НМО)" == course.type:
										course_type = 4
									elif "Категория медработника" == course.type:
										course_type = 6
									else:
										course_type = None
						course.type_text = types_check(course_type)
			except:
				continue
		# print(course.dict())

		list_treb_prog.append(course)
	print("end main")
	return list_treb_prog

def build(data: list[Course]):
	main_title = "У этой программы есть требования к поступающим:"
	for d in data:
		if d.name and d.price:
			print(d.id)
			print(d.name, d.hour, f"price: {d.price}")
			print(d.fullname)
			if d.type:
				print(d.type)
			print(main_title)
			if d.hour == 600:
				d.text_600 = "в соответствии с приказом Минздрава России №206н от 02.05.2023 «Об утверждении Квалификационных требований к медицинским и фармацевтическим работникам с высшим образованием» необходимо наличие подготовки в ординатуре или интернатуре по одной из специальностей:"
				if d.text_600:
					print("\n"+d.text_600)
				if d.spec_600:
					for x in d.spec_600:
						print(x+";")
					print("ИЛИ")
			if d.hour == 300:
				if d.text_300:
					print("\n"+d.text_300)

				if d.spec_300:
					for x in d.spec_300:
						print(x+";")
					print("ИЛИ")
			if d.text:
				print("\n"+d.text)
			if d.all_600_300:
				for x in d.all_600_300:
					print(x+";")
			if d.type_text:
				print("\n"+d.type_text)
			print("***")
			print(d.url)
			print("\n---\n")

if __name__ == "__main__":
	# try:
	main()
	# rem = Remember()
	# remember_obj: list[dict[str,str]] = [{"title": "test1"},{"title": "test2"},{"title": "test3"},{"id":3,"title": "test6"}]
	# print(rem.update(remember_obj,"test"))
	# remember_obj_: list[dict[str,str]] = [{"title": "test1"},{"title": "test2"},{"title": "test4"},]
	# rem.update(remember_obj_,"test")
	# list_s = ["1","2"]
	# list_r = ["3","4"]
	# print(list_s+list_r)
	# build(main())
	# except Exception as e:
	# 	print(e)
	# print(main())