import base64
from codecs import ascii_decode
import json
import requests
url = "https://apkipp.ru/katalog/ajax/filter/"
data = "https://web-apkipp.ru/newform/assets/docs/NMO/%D0%90%D0%9F%D0%9A%20%D0%B8%20%D0%9F%D0%9F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D1%8B%20%D0%9F%D0%9A%20%D0%9D%D0%9C%D0%9E%20%2021.10.2022.pdf"

payload = {

	"limit": 5,

}
headers = {
	"content-type": "application/json",
	"content-encoding": "gzip"
}

response_Fin = requests.request("GET", url)
if response_Fin.status_code == 200:
	print(f'QR-code generated!\n{response_Fin.text}')
with open('file.json','w', encoding='utf-8') as f:

	f.write(json.dumps(response_Fin.json(),ensure_ascii=False, indent=4))