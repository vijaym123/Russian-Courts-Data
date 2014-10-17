from mimetools import Message
from StringIO import StringIO
from unidecode import unidecode
import requests
import json
import wget
import codecs
from BeautifulSoup import BeautifulSoup
import re

def BuildCSV(params, data):
	string = ";".join(params) + "\n"
	string = "\n".join([ ";".join(i) for i in data])
	return string

def writeCSV(params, data, filename="outputCourtCases.txt"):
	string = BuildCSV(params,data)
	f = codecs.open(filename, encoding='utf-8', mode='w+')
	f.write(string)
	f.close()
	return True

def getCardDetails(urlInfo, caseId):
	url = urlInfo["card"] + caseId
	outKad = requests.get(url, headers=dict(urlInfo["card-headers"]))
	soupPage = BeautifulSoup(outKad.text)
	infoDict = {}
	try :
		snippet = soupPage.findAll('td', {"class" : "plaintiffs first"})[0]
		items = snippet.findAll('a')
		address = snippet.findAll('span', {"class" : "js-rolloverHtml"})
		infoDict["plaintiffs"] = {}
		infoDict["plaintiffs"]["names"] = [unidecode(i.text) for i in items]
		infoDict["plaintiffs"]["address"] = [unidecode(i.text) for i in address] 
	except :
		infoDict["plaintiffs"] = {}
	try :
		snippet = soupPage.findAll('td', {"class" : "defendants"})[1]
		items = snippet.findAll('a')
		address = snippet.findAll('span', {"class" : "js-rolloverHtml"})
		infoDict["defendants"] = {}
		infoDict["defendants"]["names"] = [unidecode(i.text) for i in items]
		infoDict["defendants"]["address"] = [unidecode(i.text) for i in address] 

	except :
		infoDict["defendants"] = {}
	try :
		snippet = soupPage.findAll('td', {"class" : "third"})[1]
		items = snippet.findAll('a')
		address = snippet.findAll('span', {"class" : "js-rolloverHtml"})
		infoDict["third"] = {}
		infoDict["third"]["names"] = [unidecode(i.text) for i in items]
		infoDict["third"]["address"] = [unidecode(i.text) for i in address] 

	except :
		infoDict["third"] = {}
	
	print infoDict
	return True

if __name__ == "__main__":
	urlInfo = {
	"kad" : {
		"url-main" : "http://kad.arbitr.ru/Kad/Search",
		"card" : "http://kad.arbitr.ru/Card/",
		"headers" : "",
		"card-headers" : ""
		},
	"ras" : {
		"url-main" : "http://ras.arbitr.ru/Ras/Search",
		"html" : "http://ras.arbitr.ru/Ras/HtmlDocument/",
		"headers" : ""
		}

	}

	f = open("headerKad.txt","r")
	request_text = f.read()
	request_line, headers_alone = request_text.split('\n', 1)
	urlInfo["kad"]["headers"] = Message(StringIO(headers_alone))
	
	f = open("headerRas.txt","r")
	request_text = f.read()
	request_line, headers_alone = request_text.split('\n', 1)
	urlInfo["ras"]["headers"] = Message(StringIO(headers_alone))

	f = open("headerKadCard.txt","r")
	request_text = f.read()
	request_line, headers_alone = request_text.split('\n', 1)
	urlInfo["kad"]["card-headers"] = Message(StringIO(headers_alone))

	numberOfPages = 1;

	resultDataset = []
	params = []

	for page in range(numberOfPages):
		payload = {
		"kad" : {
				"Page": page + 1, "Count":25, "Courts":["VS"], "DateFrom":None, "DateTo":None,
				"JudgesEx":[], "Sides":[], "Judges":[], "Cases":[], "WithVKSInstances":False
				},
		"ras" : {
				"Page":1, "Count":25, "GroupByCase":False, "DateFrom":"2000-01-01T00:00:00",
				"DateTo":"2030-01-01T23:59:59", "Sides":[], "Judges":[], "Cases":[], "Text":""
				}
			}

		outKad = requests.post(urlInfo["kad"]["url-main"],json.dumps(payload["kad"]), headers=dict(urlInfo["kad"]["headers"]))
		outputKad = outKad.json()
		
		for i in outputKad['Result']['Items']:
			cardDict = getCardDetails(urlInfo["kad"],i['CaseId'])
			payload["ras"]["Cases"] = [unidecode(i['CaseNumber'])]
			outRas = requests.post(urlInfo["ras"]["url-main"],json.dumps(payload["ras"]), headers=dict(urlInfo["ras"]["headers"]))
			outputRas = outRas.json()
			print payload["ras"]["Cases"]
			print outputRas
			exit()