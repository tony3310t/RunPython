import csv
from yahoo_finance import Share
import datetime
import ast
import time
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from urllib.request import urlopen

class Stock:
	def __init__(self):
		pass
	def getData(self, strTmp):
		try:
			indexStart = strTmp.find('<td')
			indexEnd = strTmp.find('</td>')
			rowData = strTmp[0:indexEnd]

			rowDataLen = len(rowData)
			tmp = ''
			while rowDataLen > 0:
				if rowData[rowDataLen-1] == '>':
					rowDataTmp = rowData[rowDataLen:]
					indexLeftBrackets = rowDataTmp.find('<')

					if rowDataTmp.strip() != '':
						tmp = rowDataTmp.strip().replace(',', '')
						break
				rowDataLen = rowDataLen-1

			return tmp
		except:
			return 'E'

	def getStockList(self, strTmp):
		try:
			indexStart = strTmp.find('<td')
			indexEnd = strTmp.find('</td>')
			rowData = strTmp[0:indexEnd]

			return tmp
		except:
			return 'E'

	def getData2(self, strTmp):
		try:
			rowDataLen = len(strTmp)
			tmp = ''
			while rowDataLen > 0:
				if strTmp[rowDataLen-1] == '>':
					rowDataTmp = strTmp[rowDataLen:]
					indexLeftBrackets = rowDataTmp.find('<')

					if rowDataTmp.strip() != '':
						tmp = rowDataTmp.strip().replace(',', '')
						break
				rowDataLen = rowDataLen-1

			return tmp
		except:
			return 'E'

	def getMAVolumeSD(self, startIndex, days, data):
		MA = '-1'
		Volume = '-1'
		SD = '-1'
		if startIndex < len(data) - days:
			count = startIndex
			MACount=0
			volumeCount=0
			while count < startIndex+days:
				MACount = MACount + float(data[count].get("Close"))
				volumeCount = volumeCount + int(data[count].get("Volume"))

				if count == startIndex+days-1:
					MA = round(float(MACount/days),3)
					Volume = float(volumeCount/days)
				count = count+1

			if MA != '-1':
				count = startIndex			
				SDCount=0
				while count < startIndex+days:
					Sub = MA - float(data[count].get("Close"))
					SDCount = SDCount + (Sub*Sub)
								
					if count == startIndex+days-1:
						SD = float(round((((SDCount/days)**0.5)), 3))
					count = count+1
		
		return {'MA':MA, 'Volume':Volume,'SD':SD}

	def get_historical_data(self, name, endDate):
		data = []
		url = "https://finance.yahoo.com/quote/" + name + "/history/"
		rows = BeautifulSoup(urlopen(url).read()).findAll('table')[0].tbody.findAll('tr')

		for each_row in rows:
			divs = each_row.findAll('td')
			if divs[1].span.text  != 'Dividend': #Ignore this row in the table
				#I'm only interested in 'Open' price; For other values, play with divs[1 - 5]
				data.append({'Date': divs[0].span.text
							,'Open': float(divs[1].span.text.replace(',',''))
							,'High': float(divs[2].span.text.replace(',',''))
							,'Low': float(divs[3].span.text.replace(',',''))
							,'Close': float(divs[4].span.text.replace(',',''))
							,'Volume': float(divs[6].span.text.replace(',',''))
							})

		i=0
		while i < len(data):
			UpDown = '-100'
			if i < len(data) -1:
				UpDown = str((round(((float(data[i].get("Close")) - float(data[i+1].get("Close")))/float(data[i].get("Close"))), 3)) * 100)

			tmpData = getMAVolumeSD(i, 5, data)
			tmpData = getMAVolumeSD(i, 20, data)
			tmpData = getMAVolumeSD(i, 30, data)
			tmpData = getMAVolumeSD(i, 40, data)
			tmpData = getMAVolumeSD(i, 50, data)
			tmpData = getMAVolumeSD(i, 60, data)
			
		return data


