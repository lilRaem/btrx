import requests

url = "https://api.qrcode-monkey.com//qr/custom"

with open('logo.png','r') as file:
	print(file.flush)

payload = {
	"config":{
	"body": "circular",
	"eye": "frame13",
	"eyeBall": "ball14",
	"erf1": [],
	"erf2": [],
	"erf3": [],
	"brf1": [],
	"brf2": [],
	"brf3": [],
	"bodyColor": "#000000",
	"bgColor": "#FFFFFF",
	"eye1Color": "FD3C76",
	"eye2Color": "FD3C76",
	"eye3Color": "FD3C76",
	"eyeBall1Color": "005DFF",
	"eyeBall2Color": "005DFF",
	"eyeBall3Color": "005DFF",
	"gradientColor1": "",
	"gradientColor2": "",
	"gradientType": "linear",
	"gradientOnEyes": False,
	"logo": "",
	"logoMode": "default"
	},
	"data": "https://web-apkipp.ru/newform/assets/docs/NMO/%D0%90%D0%9F%D0%9A%20%D0%B8%20%D0%9F%D0%9F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D1%8B%20%D0%9F%D0%9A%20%D0%9D%D0%9C%D0%9E%20%2021.10.2022.pdf",
	"file": "svg",
	"size": 400,
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "1b39f61d32msh113bae3507a8747p13948ejsn82e29bf847a1",
	"X-RapidAPI-Host": "qrcode-monkey.p.rapidapi.com"
}

# response = requests.request("POST", url, json=payload, headers=headers)

# print(response.text)

# with open('file.svg', 'w') as f:
# 	f.write(response.text)