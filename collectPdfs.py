from mimetools import Message
from StringIO import StringIO
from unidecode import unidecode
import requests
import json
import wget

f = open("header.txt","r")
request_text = f.read()

request_line, headers_alone = request_text.split('\n', 1)
headers = Message(StringIO(headers_alone))
data = {
"Page":1,
"Count":25,
"GroupByCase":False,
"Courts":["VAS"],
"DateFrom":"2014-05-29T00:00:00",
"DateTo":"2014-06-11T23:59:59",
"Sides":[],
"Judges":[],
"Cases":[],
"Text":""
}

url = "http://ras.arbitr.ru/Ras/Search"
out=requests.post(url,json.dumps(data), headers=dict(headers))

output = out.json()
for i in output['Result']['Items']:
	print i['Id']+"/"+unidecode(i['FileName'])
	wget.download("http://ras.arbitr.ru/PdfDocument/"+i['Id']+"/"+unidecode(i['FileName']))

