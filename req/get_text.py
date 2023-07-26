import json,sys,os
from time import sleep
from pydantic import BaseModel,StrictStr,StrictInt
from colorama import Fore,Back
from typing import Optional
from params import list_course,check_600,check_300,forCheck600,forCheck300,already_600_300,types_prog,types_check
sys.path.insert(0,os.getcwd())
from module.parsersearchsite import getProgramUrl
from module.remember import Remember
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
	with open("data/json/btrx_data/21.07.2023_file.json","r",encoding="utf-8") as f:
		data = json.load(f)
	return data


def main():
	print("start main")
	rem = Remember()
	list_treb_prog:list[Course] = list()
	list_fail_urlprog: list[Course] = list()
	for i_p,prog in enumerate(load_json()[2400:2410]):

		course = Course()
		course.id = int(prog.get("ID"))

		programm_url = list()
		prog_fullname = "Курс "+prog.get("NAME").lower()
		course.fullname = prog_fullname
		course.name = course.fullname.replace("Курс ", "").capitalize()
		if prog.get("PROPERTY_213"):
			course.hour = int(prog.get("PROPERTY_213").get("value"))
		# print(course.name)
		if prog.get("PRICE"):
			course.price = int(prog.get("PRICE").replace(".00",""))
		if prog:
			prog_url: list[dict] = list()
			if prog.get("PROPERTY_213"):
				course.hour = int(prog['PROPERTY_213']['value'])
			rem.remember(programm_url,'listurl')
			print("\n***")
			for l_prog in rem.load("listurl"):
				if course.fullname == l_prog.get("name") or course.name == l_prog.get("name"):
					if int(course.price) == int(l_prog.get("price")):
						if not course.hour: course.hour = int(l_prog.get("hour"))
						if course.hour == l_prog.get("hour"):
							print(course.name,f"price: {course.price}","\n-*-\n")
							course.url = l_prog.get("url")
							prog_url.append(l_prog)
						else:
							print(course.name,f"price: {course.price}","\n-*-\n")

			# if not prog_url:
			# 	print(f"index of prog: {i_p}")
			# 	course.name = course.name.strip()
			# 	course.fullname = course.fullname.strip()
			# 	# print(Back.LIGHTYELLOW_EX+f"[search]: {course.name} price: {course.price} {course.id} {course.hour}"+Back.RESET)
			# 	if course.price:
			# 		prog_url_1 = getProgramUrl(search_key=str(course.fullname).lower(),price=int(course.price))
			# 		if not prog_url_1:
			# 			prog_url = getProgramUrl(search_key=str(course.name).lower(),price=int(prog.get("PRICE").replace(".00","")))
			# 		else:
			# 			prog_url = prog_url_1
			# 		prog_url_2 = getProgramUrl(search_key=str(course.name).lower(),price=int(course.price))
			# 		if not prog_url_2:
			# 			prog_url = getProgramUrl(search_key=str(course.fullname).lower(),price=int(prog.get("PRICE").replace(".00","")))
			# 		else:
			# 			prog_url = prog_url_2
			# 		if not prog_url:
			# 			if not os.path.exists("data/cached_items/errors/didntfind_Prog.json"):
			# 				os.mkdir('data/cached_items/errors')
			# 			with open("data/cached_items/errors/didntfind_Prog.json", "w",encoding="utf8") as f:
			# 				list_fail_urlprog.append(course.model_dump(include=['id','name',"price","hour","url"]))
			# 				json.dump(list_fail_urlprog, f, ensure_ascii=False,indent=4)
			# 				f.close()

			# if prog_url:
			# 	for p_url in prog_url:
			# 		if course.fullname.lower() == p_url.get("name").lower() or course.name.lower() == p_url.get("name").lower():
			# 			if int(course.price) == int(p_url.get("price")):
			# 				if not course.hour: course.hour = int(p_url.get("hour"))
			# 				if course.hour == p_url.get("hour"):
			# 					print(Fore.GREEN+f"{course.name} {course.price}"+Fore.RESET)
			# 					p_url['id'] = int(prog.get('ID'))
			# 					# print(p_url)
			# 					programm_url.append(p_url)
			# 					rem.remember(programm_url,'listurl')


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
						if course.fullname.lower() == d_url.get('name').lower():
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
		# print(course.model_dump_json())

		list_treb_prog.append(course)
	print("end main")
	return list_treb_prog

def build(data: list[Course]):
	main_title = "У этой программы есть требования к поступающим:"
	privileges_box__item_title = "для зачисления необходимо наличие одного из документов:"
	for d in data:
		if d.name and d.price:
			print(d.id,d.hour)


if __name__ == "__main__":
	# try:
	build(main())

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