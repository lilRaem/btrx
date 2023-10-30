import os, csv, json

file = "судэксперты.csv"
print(os.getcwd()+(f"\\docForparse\\{file}"))
path = os.getcwd()+(f"\\docForparse\\{file}")


jslist = list()
with open(f"{path}","r",encoding="utf-8") as f:
	# print(f.read())
	csvReaader = csv.DictReader(f,delimiter=";",fieldnames=["program","desc","exist"])
	for row in csvReaader:
		print(row)
		jslist.append(row)
	f.close()
	with open("asd.json","w",encoding="utf-8") as fj:
		jsonString = json.dumps(jslist,ensure_ascii=False, indent=4)
		fj.write(jsonString)

