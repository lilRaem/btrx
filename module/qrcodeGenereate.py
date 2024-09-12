import json, requests, os
import requests
url = "https://api.qrcode-monkey.com//qr/custom"
data = "https://shrinkingurl/link"

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
	"logo": 'logo.png',
	"logoMode": "default"
	},
	"data":data,

	"file": "svg",
	"size": 100,
}
headers = {
	"content-type": "application/json"
}

response_Fin = requests.request("POST", url, json=payload, headers=headers,timeout=2000)
if response_Fin.status_code == 200:
	print('QR-code generated!')
else:
	print("QR-code generation fail...")

if os.path.exists("data/qrcode"):

	list_dir = os.listdir("data/qrcode")

	with open(f'data/qrcode/file_{list_dir.__len__()+1}.svg', 'w',encoding="utf-8") as f:
		f.write(response_Fin.text)
		print(f"file_{list_dir.__len__()+1}.svg saved in data/qrcode!")
else:
	os.mkdir("data/qrcode")
	with open('data/qrcode/file_1.svg', 'w') as f:
		f.write(response_Fin.text)