import json
import sys
from remember import Remember
from config import FinalData
from main_search import search
sys.path.insert(0,'/')
def main(name: str = "Биолог", price: int = 49800):
	# print("Start")
	rem = Remember()
	final_data = FinalData()
	lis: list[FinalData] = list()
	for data in rem.load("listurl"):
		final_data.id = data['id']
		final_data.fullname = data['name']
		final_data.katalog = data['katalog']
		final_data.spec = data['spec']
		final_data.type_zdrav = data['type_zdrav']
		final_data.name = data['name'].replace("Курс ", "").capitalize()
		final_data.price = data['price']
		final_data.hour = data['hour']
		final_data.url = data['url']
		final_data.final_url = data['final_url']
		if final_data.fullname.lower() == name.lower() or final_data.name.lower() == name.lower():
			if final_data.price:
				if int(final_data.price) == int(price):
					if not final_data.hour: final_data.hour = data['hour']
					if final_data.hour == data['hour']:
						print(final_data.name)
						return final_data
	return None


if __name__ == "__main__":
	prog = None
	li = [
		"Биолог", "Зоолог", "Инструктор-методист по лечебной физкультуре",
		"Медицинская логопедия", "Медицинская психология", "Медицинский физик",
		"Физическая реабилитация (физическая терапия)",
		"эргореабилитация (эрготерапия)", "Судебный эксперт (эксперт-биохимик, эксперт-генетик, эксперт-химик)",
		"Химик-эксперт в клинико-диагностической лаборатории",
		"Эксперт-физик по контролю за источниками ионизирующих и неионизирующих излучений---", "Эмбриолог"
	]
	for i,name in enumerate(li):
		# print()
		# print(name,"\n")
		res = main(name=name,price=49800)

		if not res:
			print(res)
			prog=search(name,49800)
		print(prog)
		with open("d.json",'a',encoding='utf-8') as f:
			if res:
				json.dump(res.model_dump(),f,ensure_ascii=False,indent=4)
			else:
				if prog:
					json.dump(prog,f,ensure_ascii=False,indent=4)