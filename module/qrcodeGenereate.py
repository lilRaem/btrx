import base64
import json
import requests
import PIL.Image
url = "https://api.qrcode-monkey.com//qr/custom"
data = "https://web-apkipp.ru/newform/assets/docs/NMO/%D0%90%D0%9F%D0%9A%20%D0%B8%20%D0%9F%D0%9F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D1%8B%20%D0%9F%D0%9A%20%D0%9D%D0%9C%D0%9E%20%2021.10.2022.pdf"

s = None

image = PIL.Image.open("logo.png")
bytes = image.tobytes()
mystr = base64.b64encode(bytes).decode('utf-8')
payload_img = {
	"download": mystr,
	"data": "hELL",
}
headers = {
	"content-type": "application/json"
}
response = requests.request("POST", url, json=payload_img, headers=headers)
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
	"logo": 'a8077b772dea1044706a2646bf7056b07cfad66a.png',
	"logoMode": "default"
	},
	"data":response.text,

	"file": "svg",
	"size": 400,
}
headers = {
	"content-type": "application/json"
}

response_Fin = requests.request("POST", url, json=payload_img, headers=headers)
if response_Fin.status_code == 200:
	print(f'QR-code generated!\n{response_Fin.text}')

with open('file.svg', 'w') as f:
	f.write(response_Fin.text)