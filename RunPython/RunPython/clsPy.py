import csv
from yahoo_finance import Share
import datetime
import ast
import time

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
