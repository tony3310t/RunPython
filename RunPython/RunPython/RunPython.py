import sys
import json
import os
import requests
import csv
import operator
from yahoo_finance import Share
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import clsPy

if __name__ == '__main__':
	#funcName = sys.argv[1]
	#stockSymbol = sys.argv[2]
	#startDate = sys.argv[3]
	#endDate = sys.argv[4]

	#funcName = 'Create_StockInfo'
	#funcName = 'Create_RonChe'
	#funcName = 'Parser_iTrust'
	#funcName = 'Parser_Foreign'
	funcName = 'Parser_Dealer'
	#funcName = 'Parser_RonChe'
	#funcName = 'Parser_StockList'
	#funcName = 'Get_RonChe_Info'
	#funcName = 'find_Surf'
	#stockSymbol = '3576.TW'
	#startDate = '2013-01-01'
	#endDate = '2017-01-21'

	if funcName == 'Create_StockInfo':
		stockSymbol = ''
		with open('E:\stockList.csv', newline='') as f:		
			reader = csv.reader(f)
			
			count=0
			for row in reader:
				if row == []:
					continue				
				
				number = str(str(row[0]) + '.TW')
				
				try:
					if count != 0:
						stockSymbol = stockSymbol + ','
					stockSymbol = stockSymbol + number
					count = count + 1
				except:
					print(number)

		with open('E:\OTC.csv', newline='') as f:		
			reader = csv.reader(f)
			
			count=0
			for row in reader:
				if row == []:
					continue				
				
				number = str(str(row[0]) + '.TW')
				try:
					if count != 0:
						stockSymbol = stockSymbol + ','
					stockSymbol = stockSymbol + number
					count = count + 1
				except:
					print(number)

		stockList = stockSymbol.split(',')

		
		i = 0
		while i < len(stockList):
			try:
				print(stockList[i])
				result = ''
				stock = Share(stockList[i])
				data = stock.get_historical(startDate, endDate)
				str = '{"' + stockList[i] + '"' + ':'
				str = str + json.dumps(data)
				str = str + '}'
				result = result + str

				pathName = 'E:\stockInfo' + '\\' + stockList[i] + '_' +  startDate + '_' + endDate + '.txt'
				if os.path.exists(pathName):
					os.remove(pathName)
				f = open(pathName, 'w', encoding = 'UTF-8')    # 也可使用指定路徑等方式，如： C:\A.txt
				f.write(result)
				f.close()

				#if i < len(stockList)-1 :
					#result = result + ','						
			except:
				print('Error:' + stockList[i])
			i=i+1

		#result = result + ']'

		
	#print(str)
	#print(data[0])

	if funcName == 'Create_RonChe':

		#list = []
		dayAdd = {}
		with open('E:\stockList.csv', newline='') as f:		
			reader = csv.reader(f)
			i = 0
			for row in reader:
				if row == []:
					continue
				i = i + 1
				number = str(row[0])
				#print(number)

				try:
					response = requests.get("http://jsjustweb.jihsun.com.tw/z/zc/zcn/zcn.djhtm?a="+number+"&c=2017-02-01&d=2017-03-08")
					index = response.text.find('nowrap>相抵</TD>')
					strTmp = response.text[index:]
		
					code = 1
					count = 0
					num = 0
					tmpNum = 0
					percent = 0
					maxPercent = 0
					maxPercentDate = ''
					
					while code == 1:		
						index = strTmp.find('class="t3n0">')

						if index == -1:
							if num > tmpNum and percent > 30 and percent < 85 :
								print(str(number) + ':' +str(num - tmpNum) + '  percent:' + str(dayPercent) + ' Max%:' + str(maxPercent) + ' MaxDate:' + str(maxPercentDate))
							break

						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</TD>')
						date = strTmp[0:9]
						#print(str[0:indexTD])
						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						#print(str[0:indexTD])
						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						#print(str[0:indexTD])
						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						#print(str[0:indexTD])
						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')

						tmpNum = int(strTmp[0:indexTD].replace(',', ''))
						if count ==0:
							num = tmpNum

						#print(str[0:indexTD])
						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')

						dayAddMax = int(strTmp[0:indexTD].replace(',', ''))	

						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')

						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						dayPercent = float(strTmp[0:indexTD].replace('%', ''))

						if dayPercent > maxPercent:
							maxPercent = dayPercent
							maxPercentDate = date

						if count ==0:
							percent = dayPercent
							if dayAddMax > 0 and percent>30 and percent<85:
								dayAdd[number] = dayAddMax
										
						count = count + 1
				except:
					print('E:' + str(number))	
		
		sorted_x = sorted(dayAdd.items(), key=operator.itemgetter(1))						
		print(sorted_x)	


	if funcName == 'find_Surf':

		with open('E:\stockList.csv', newline='') as f:		
			reader = csv.reader(f)
			
			for row in reader:
				if row == []:
					continue				
				
				number = str(str(row[0]) + '.TW')
				try:
					start = time.time()
					stock = Share(number)
					data = stock.get_historical('2015-01-01', '2017-01-20')
					end = time.time()
					elapsed = end - start
					#print(elapsed)
					i=0
					while i < (len(data) - 121):
						if float(data[i].get("Close")) / float(data[i].get("Open")) > 1.04:
							k=2
							count=0
							NG=0
							if ((i+1) < (len(data))) and (data[i].get("Close") > data[i+1].get("Close")):
								up = float(data[i+1].get("Close")) * 1.0
								down = float(data[i+1].get("Close")) * 0.9
								while i+k < len(data):
									if float(data[i+k].get("Close")) < up and float(data[i+k].get("Close")) > down:
										if float(data[i+k].get("Close")) > down:
											count = count+1
										else:
											NG = NG +1
											if NG > 5:
												break
									else:
										NG = NG+1
										if NG > 5:
											break
									k=k+1

								if count > 0 and datetime.strptime(data[i].get("Date"), "%Y-%m-%d") > datetime.strptime('2016-11-01', "%Y-%m-%d"):
									b=0
									#print(str(number) + ' ' + str(data[i].get("Date")) + ' 爆量長紅 + 連續盤整 ' + str(count) + ' 日')

							fiveAVGVolume = 0
							j=0
							while j<5:
								fiveAVGVolume = fiveAVGVolume + float(data[i+j].get("Volume"))
								j=j+1

							if(fiveAVGVolume / 5 > 500000):
								twentyMA = 0
								j=0
								while j<20:
									twentyMA = twentyMA + float(data[i+j].get("Close"))
									j=j+1
								twentyMA = twentyMA/20

								sixtyMA = 0
								j=0
								while j<60:
									sixtyMA = sixtyMA + float(data[i+j].get("Close"))
									j=j+1
								sixtyMA = sixtyMA/60

								hundredTwentyMA = 0
								j=0
								while j<120:
									hundredTwentyMA = hundredTwentyMA + float(data[i+j].get("Close"))
									j=j+1
								hundredTwentyMA = hundredTwentyMA/120

								#print(str(data[i].get("Date")) + ' 20MA:' + str(twentyMA) + ' 60MA:' + str(sixtyMA) + ' 120MA:' + str(hundredTwentyMA))

								if twentyMA > sixtyMA and sixtyMA > hundredTwentyMA:
									#print(str(data[i].get("Date")) + ' 多頭排列')

									tmp = i
									i=i+6
									if i + 120 > len(data):
										i=tmp
									else:
										twentyMA = 0
										j=0
										while j<20:
											twentyMA = twentyMA + float(data[i+j].get("Close"))
											j=j+1
										twentyMA = twentyMA/20

										sixtyMA = 0
										j=0
										while j<60:
											sixtyMA = sixtyMA + float(data[i+j].get("Close"))
											j=j+1
										sixtyMA = sixtyMA/60

										hundredTwentyMA = 0
										j=0
										while j<120:
											hundredTwentyMA = hundredTwentyMA + float(data[i+j].get("Close"))
											j=j+1
										hundredTwentyMA = hundredTwentyMA/120

										if twentyMA > sixtyMA and sixtyMA > hundredTwentyMA:
											a=0
										else:	
											endDate=''										
											m=tmp
											while m < (len(data))-121:
												twentyMA = 0
												j=0
												while j<20:
													twentyMA = twentyMA + float(data[m+j].get("Close"))
													j=j+1
												twentyMA = twentyMA/20

												sixtyMA = 0
												j=0
												while j<60:
													sixtyMA = sixtyMA + float(data[m+j].get("Close"))
													j=j+1
												sixtyMA = sixtyMA/60

												hundredTwentyMA = 0
												j=0
												while j<120:
													hundredTwentyMA = hundredTwentyMA + float(data[m+j].get("Close"))
													j=j+1
												hundredTwentyMA = hundredTwentyMA/120

												if twentyMA < sixtyMA or sixtyMA < hundredTwentyMA:
													endDate=str(data[m].get("Date"))
													break

												if m == (len(data))-122:
													endDate=str(data[m].get("Date"))

												m=m+1
											print(str(number) + ' ' + str(data[tmp].get("Date")) + ' 多頭排列形成在五日內 結束在:' + endDate)
										i=tmp

						i = i + 1
				except:
					print('error:' + str(number))
			
			
	if funcName == 'Get_RonChe_Info':
		pDataPath = os.getenv('PROGRAMDATA')
		crazyStockPath = pDataPath + "\CrazyStock"
		if not os.path.isdir(crazyStockPath):
			os.makedirs(crazyStockPath)

		stockListPath = crazyStockPath + "\source\stockList.csv"

		if not os.path.exists(stockListPath):
			print("error : Lose stockList.csv file.")
			sys.exit()

		stockInfoPath = crazyStockPath + "\stock"
		if not os.path.isdir(stockInfoPath):
			os.makedirs(stockInfoPath)
		
		with open(stockListPath, newline='') as f:		
			reader = csv.reader(f)
			i = 0
			for row in reader:
				if row == []:
					continue
				i = i + 1
				number = str(row[0])
				
				perStockPath = stockInfoPath + "\\" + number
				if not os.path.isdir(perStockPath):
					os.makedirs(perStockPath)

				ronchePath = perStockPath + "\Ronche"
				if not os.path.isdir(ronchePath):
					os.makedirs(ronchePath)

				endDate = ""
				infoPath = ronchePath + "\info.txt"
				if not os.path.exists(infoPath):
					endDate = "2014-01-01"
				else:
					f = open(infoPath, 'r', encoding = 'UTF-8')
					while True :
						   endDate = f.readline()
						   break
						   #if i=='': break
						   #print(i,end='')
					f.close()

				responseText = ""
				try:
					response = requests.get("http://jsjustweb.jihsun.com.tw/z/zc/zcn/zcn.djhtm?a="+number+"&c="+endDate+"&d="+ time.strftime("%Y-%m-%d")+"")
					responseText = response.text
				except:
					print("error : Parse error")
					sys.exit()
				
				try:	
					index = responseText.find('nowrap>相抵</TD>')
					strTmp = responseText[index:]
		
					code = 1
					while code == 1:	
						resultStr = "[{"	
						index = strTmp.find('class="t3n0">')

						if index == -1:
							break

						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</TD>')
						date = strTmp[0:9]

						resultStr = resultStr + "\"Date\": " + "\"" + date + "\", "
						#print(str[0:indexTD])
						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						#print(str[0:indexTD])
						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						#print(str[0:indexTD])
						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						#print(str[0:indexTD])
						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')

						tmpNum = int(strTmp[0:indexTD].replace(',', ''))
						if count ==0:
							num = tmpNum

						#print(str[0:indexTD])
						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')

						dayAddMax = int(strTmp[0:indexTD].replace(',', ''))	

						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')

						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						dayPercent = float(strTmp[0:indexTD].replace('%', ''))

						if dayPercent > maxPercent:
							maxPercent = dayPercent
							maxPercentDate = date

						if count ==0:
							percent = dayPercent
							if dayAddMax > 0 and percent>30 and percent<85:
								dayAdd[number] = dayAddMax
										
						count = count + 1
				except:
					print('E:' + str(number))	
		
		sorted_x = sorted(dayAdd.items(), key=operator.itemgetter(1))						
		print(sorted_x)	
	#投信	
	if funcName == 'Parser_iTrust':
		start = time.time()
		appDataPath = os.getenv('APPDATA')
		if os.path.exists(appDataPath + '\StockData') == False:
			os.makedirs(appDataPath + '\StockData')

		obj = clsPy.Stock()
		#list = []
		dayAdd = {}
		with open(appDataPath + '\\' + 'stockList.csv', newline='') as f:		
			reader = csv.reader(f)
			i = 0
			for row in reader:
				if row == []:
					continue
				i = i + 1
				number = str(row[0])
				#print(number)
				debugStatus = ''
				check = True
				jsonOutput = '['
				try:
					if os.path.exists(appDataPath + '\StockData\\' + str(number)) == False:
						os.makedirs(appDataPath + '\StockData\\' + str(number))

					response = requests.get("http://www.cnyes.com/twstock/itrust/"+number+".htm")
					#index = response.text.find('近一個月三大法人買賣超總表')
					index = response.text.find('投信進出</h3>')
					strTmp = response.text[index:]
		
					code = 1
					tmp = ''
					liDate = []
					count = 0
					iStructCount = 0
					Total = 0
					
					while code == 1:	
						count = count +1

						if count > 1000:
							check = False
							debugStatus = 'Unknown'
							break

						jsonTmp = '{'
						#key = strTmp.find('外資買賣超</a>')	
						indexStart = strTmp.find('<td')
						strTmp = strTmp[indexStart:]
						currentDate = datetime.today()
						data = str(currentDate.year) + '/' + obj.getData(strTmp)
						liDate.append(data)
						jsonTmp = jsonTmp + '"iTrustDate":"' + data + '", '
						debugStatus = 'Date:' + str(data)
						'''
						if datetime.strptime(data, "%Y/%m/%d") < datetime.strptime('2017/03/01', "%Y/%m/%d"):
							if iStructCount > 0:
								print(str(number) + ':' + str(iStructCount) + ' ' + str(iStructCount/int(Total)*100))
							break
						'''
						indexEnd = strTmp.find('</td>')
						strTmp = strTmp[indexEnd+5:]
						data = obj.getData(strTmp)
						jsonTmp = jsonTmp + '"iTrustBuy":"' + data + '", '
						debugStatus = '投信買:' + str(data)

						indexEnd = strTmp.find('</td>')
						strTmp = strTmp[indexEnd+5:]
						data = obj.getData(strTmp)
						jsonTmp = jsonTmp + '"iTrustSell":"' + data + '", '
						debugStatus = '投信賣:' + str(data)

						indexEnd = strTmp.find('</td>')
						strTmp = strTmp[indexEnd+5:]
						data = obj.getData(strTmp)
						iStructCount = iStructCount + int(data)
						jsonTmp = jsonTmp + '"iTrustTotal":"' + data + '", '
						debugStatus = '投信總:' + str(data)

						indexEnd = strTmp.find('</td>')
						strTmp = strTmp[indexEnd+5:]
						data = obj.getData(strTmp)
						Total = data
						jsonTmp = jsonTmp + '"iTrustPublic":"' + data + '" '
						debugStatus = '發行張數:' + str(data)

						indexEnd = strTmp.find('</td>')
						strTmp = strTmp[indexEnd+5:]

						key = strTmp.find('最近訪問股</a>')	
						indexStart = strTmp.find('<td')

						if key < indexStart:
							jsonTmp = jsonTmp + '}'
							jsonOutput = jsonOutput + jsonTmp
							break
						else:
							jsonTmp = jsonTmp + '}'
							jsonTmp = jsonTmp + ','
							jsonOutput = jsonOutput + jsonTmp
						
				except:
					check = False
					print('Error:' + str(number) + '_' + debugStatus)
				
				if check:
					jsonOutput = jsonOutput + ']'

					f = open(appDataPath + '\StockData\\' + str(number) + '\\' + 'iTrust.txt', 'w', encoding = 'UTF-8')
					f.write(jsonOutput)
					f.close()

					log = ''

					if len(liDate) > 0:
						log = log + 'StartDate:' + liDate[0] + ',EndDate:' + liDate[len(liDate)-1] + ', Error:NA'

					f = open(appDataPath + '\StockData\\' + str(number) + '\\' + 'iTrust_log.txt', 'w', encoding = 'UTF-8')
					f.write(log)
					f.close()
					print(number)
				else:
					f = open(appDataPath + '\StockData\\' + str(number) + 'iTrust_log.txt', 'w', encoding = 'UTF-8')
					f.write('Error:' + str(number) + '_' + debugStatus)
					f.close()
		end = time.time()
		elapsed = end - start
		print(elapsed)	
		
	#外資	
	if funcName == 'Parser_Foreign':
		start = time.time()
		appDataPath = os.getenv('APPDATA')
		if os.path.exists(appDataPath + '\StockData') == False:
			os.makedirs(appDataPath + '\StockData')

		obj = clsPy.Stock()
		#list = []
		dayAdd = {}
		with open(appDataPath + '\\' + 'stockList.csv', newline='') as f:		
			reader = csv.reader(f)
			i = 0
			for row in reader:
				if row == []:
					continue
				i = i + 1
				number = str(row[0])
				#print(number)
				debugStatus = ''
				check = True
				jsonOutput = '['
				try:
					if os.path.exists(appDataPath + '\StockData\\' + str(number)) == False:
						os.makedirs(appDataPath + '\StockData\\' + str(number))

					response = requests.get("http://www.cnyes.com/twstock/QFII/"+number+".htm")
					index = response.text.find('外資進出</h3>')
					strTmp = response.text[index:]
		
					code = 1
					tmp = ''
					liDate = []
					count = 0
					iStructCount = 0
					Total = 0
					
					while code == 1:	
						count = count +1

						if count > 1000:
							check = False
							debugStatus = 'Unknown'
							break

						jsonTmp = '{'
						indexStart = strTmp.find('<td')
						strTmp = strTmp[indexStart:]
						currentDate = datetime.today()
						data = str(currentDate.year) + '/' + obj.getData(strTmp)
						liDate.append(data)
						jsonTmp = jsonTmp + '"ForeignDate":"' + data + '", '
						debugStatus = 'Date:' + str(data)
						
						indexEnd = strTmp.find('</td>')
						strTmp = strTmp[indexEnd+5:]
						data = obj.getData(strTmp)
						jsonTmp = jsonTmp + '"ForeignBuy":"' + data + '", '
						debugStatus = '外資買:' + str(data)

						indexEnd = strTmp.find('</td>')
						strTmp = strTmp[indexEnd+5:]
						data = obj.getData(strTmp)
						jsonTmp = jsonTmp + '"ForeignSell":"' + data + '", '
						debugStatus = '外資賣:' + str(data)

						indexEnd = strTmp.find('</td>')
						strTmp = strTmp[indexEnd+5:]
						data = obj.getData(strTmp)
						jsonTmp = jsonTmp + '"ForeignSub":"' + data + '", '
						debugStatus = '外資買賣超:' + str(data)

						indexEnd = strTmp.find('</td>')
						strTmp = strTmp[indexEnd+5:]
						data = obj.getData(strTmp)
						jsonTmp = jsonTmp + '"ForeignKeep":"' + data + '", '
						debugStatus = '外資持有:' + str(data)

						indexEnd = strTmp.find('</td>')
						strTmp = strTmp[indexEnd+5:]
						data = obj.getData(strTmp)
						jsonTmp = jsonTmp + '"ForeignRate":"' + data + '", '
						debugStatus = '外資持有率:' + str(data)

						indexEnd = strTmp.find('</td>')
						strTmp = strTmp[indexEnd+5:]
						data = obj.getData(strTmp)
						iStructCount = iStructCount + int(data)
						jsonTmp = jsonTmp + '"ForeignQuota":"' + data + '", '
						debugStatus = '外資尚可投資張數:' + str(data)

						indexEnd = strTmp.find('</td>')
						strTmp = strTmp[indexEnd+5:]
						data = obj.getData(strTmp)
						Total = data
						jsonTmp = jsonTmp + '"Total":"' + data + '" '
						debugStatus = '發行張數:' + str(data)

						indexEnd = strTmp.find('</td>')
						strTmp = strTmp[indexEnd+5:]

						key = strTmp.find('最近訪問股</a>')	
						indexStart = strTmp.find('<td')

						if key < indexStart:
							jsonTmp = jsonTmp + '}'
							jsonOutput = jsonOutput + jsonTmp
							break
						else:
							jsonTmp = jsonTmp + '}'
							jsonTmp = jsonTmp + ','
							jsonOutput = jsonOutput + jsonTmp
						
				except:
					check = False
					print('Error:' + str(number) + '_' + debugStatus)
				
				if check:
					jsonOutput = jsonOutput + ']'

					f = open(appDataPath + '\StockData\\' + str(number) + '\\' + 'Foreign.txt', 'w', encoding = 'UTF-8')
					f.write(jsonOutput)
					f.close()

					log = ''

					if len(liDate) > 0:
						log = log + 'StartDate:' + liDate[0] + ',EndDate:' + liDate[len(liDate)-1] + ', Error:NA'

					f = open(appDataPath + '\StockData\\' + str(number) + '\\' + 'Foreign_log.txt', 'w', encoding = 'UTF-8')
					f.write(log)
					f.close()
					print(number)
				else:
					f = open(appDataPath + '\StockData\\' + str(number) + 'Foreign_log.txt', 'w', encoding = 'UTF-8')
					f.write('Error:' + str(number) + '_' + debugStatus)
					f.close()
		end = time.time()
		elapsed = end - start
		print(elapsed)			

	#自營商	
	if funcName == 'Parser_Dealer':
		start = time.time()
		appDataPath = os.getenv('APPDATA')
		if os.path.exists(appDataPath + '\StockData') == False:
			os.makedirs(appDataPath + '\StockData')

		obj = clsPy.Stock()
		#list = []
		dayAdd = {}
		with open(appDataPath + '\\' + 'stockList.csv', newline='') as f:		
			reader = csv.reader(f)
			i = 0
			for row in reader:
				if row == []:
					continue
				i = i + 1
				number = str(row[0])
				#print(number)
				debugStatus = ''
				check = True
				jsonOutput = '['
				try:
					if os.path.exists(appDataPath + '\StockData\\' + str(number)) == False:
						os.makedirs(appDataPath + '\StockData\\' + str(number))

					response = requests.get("http://www.cnyes.com/twstock/dealer/"+number+".htm")
					index = response.text.find('自營商進出</h3>')
					strTmp = response.text[index:]
		
					code = 1
					tmp = ''
					liDate = []
					count = 0
					iStructCount = 0
					Total = 0
					
					while code == 1:	
						count = count +1

						if count > 1000:
							check = False
							debugStatus = 'Unknown'
							break

						jsonTmp = '{'
						indexStart = strTmp.find('<td')
						strTmp = strTmp[indexStart:]
						currentDate = datetime.today()
						data = str(currentDate.year) + '/' + obj.getData(strTmp)
						liDate.append(data)
						jsonTmp = jsonTmp + '"DealerDate":"' + data + '", '
						debugStatus = 'Date:' + str(data)
						
						indexEnd = strTmp.find('</td>')
						strTmp = strTmp[indexEnd+5:]
						data = obj.getData(strTmp)
						jsonTmp = jsonTmp + '"DealerBuy":"' + data + '", '
						debugStatus = '自營商買:' + str(data)

						indexEnd = strTmp.find('</td>')
						strTmp = strTmp[indexEnd+5:]
						data = obj.getData(strTmp)
						jsonTmp = jsonTmp + '"DealerSell":"' + data + '", '
						debugStatus = '自營商賣:' + str(data)

						indexEnd = strTmp.find('</td>')
						strTmp = strTmp[indexEnd+5:]
						data = obj.getData(strTmp)
						iStructCount = iStructCount + int(data)
						jsonTmp = jsonTmp + '"DealerTotal":"' + data + '", '
						debugStatus = '投信買賣超:' + str(data)

						indexEnd = strTmp.find('</td>')
						strTmp = strTmp[indexEnd+5:]
						data = obj.getData(strTmp)
						Total = data
						jsonTmp = jsonTmp + '"DealerPublic":"' + data + '" '
						debugStatus = '發行張數:' + str(data)

						indexEnd = strTmp.find('</td>')
						strTmp = strTmp[indexEnd+5:]

						key = strTmp.find('最近訪問股</a>')	
						indexStart = strTmp.find('<td')

						if key < indexStart:
							jsonTmp = jsonTmp + '}'
							jsonOutput = jsonOutput + jsonTmp
							break
						else:
							jsonTmp = jsonTmp + '}'
							jsonTmp = jsonTmp + ','
							jsonOutput = jsonOutput + jsonTmp
						
				except:
					check = False
					print('Error:' + str(number) + '_' + debugStatus)
				
				if check:
					jsonOutput = jsonOutput + ']'

					f = open(appDataPath + '\StockData\\' + str(number) + '\\' + 'Dealer.txt', 'w', encoding = 'UTF-8')
					f.write(jsonOutput)
					f.close()

					log = ''

					if len(liDate) > 0:
						log = log + 'StartDate:' + liDate[0] + ',EndDate:' + liDate[len(liDate)-1] + ', Error:NA'

					f = open(appDataPath + '\StockData\\' + str(number) + '\\' + 'Dealer_log.txt', 'w', encoding = 'UTF-8')
					f.write(log)
					f.close()
					print(number)
				else:
					f = open(appDataPath + '\StockData\\' + str(number) + 'Dealer_log.txt', 'w', encoding = 'UTF-8')
					f.write('Error:' + str(number) + '_' + debugStatus)
					f.close()
		end = time.time()
		elapsed = end - start
		print(elapsed)	

	#股票清單
	if funcName == 'Parser_StockList':
		appDataPath = os.getenv('APPDATA')
		if os.path.exists(appDataPath + '\StockData') == False:
			os.makedirs(appDataPath + '\StockData')

		obj = clsPy.Stock()
		check = True
		tmp = ''
		try:
			response = requests.get("http://stock.wespai.com/p/16647")
			index = response.text.find('<th>股價</th>')
			strTmp = response.text[index:]
		
			code = 1
			count = 0
				
			while code == 1:
				indexStart = strTmp.find('<td>')

				if indexStart == -1:
					break

				indexEnd = strTmp.find('</td>')
				Data = strTmp[indexStart+4:indexEnd]

				if count%3 == 0:
					tmp = tmp + Data + '\n'

				strTmp = strTmp[indexEnd+5:]
				count = count +1
				
		except:
			check = False
			print('Error:')
		
		if check:
			f = open(appDataPath + '\\' + 'stockList.csv', 'w', encoding = 'UTF-8')
			f.write(tmp)
			f.close()

			log = 'OK'

			f = open(appDataPath + '\\' + 'stockList_log.txt', 'w', encoding = 'UTF-8')
			f.write(log)
			f.close()
		else:
			log = 'Fail'

			f = open(appDataPath + '\\' + 'stockList_log.txt', 'w', encoding = 'UTF-8')
			f.write(log)
			f.close()

	#融資融券
	if funcName == 'Parser_RonChe':
		start = time.time()
		appDataPath = os.getenv('APPDATA')
		if os.path.exists(appDataPath + '\StockData') == False:
			os.makedirs(appDataPath + '\StockData')

		obj = clsPy.Stock()
		#list = []
		dayAdd = {}
		with open(appDataPath + '\\' + 'stockList.csv', newline='') as f:		
			reader = csv.reader(f)
			i = 0
			for row in reader:
				if row == []:
					continue
				i = i + 1
				number = str(row[0])
				#print(number)
				debugStatus = ''
				check = True
				jsonOutput = '['
				try:
					if os.path.exists(appDataPath + '\StockData\\' + str(number)) == False:
						os.makedirs(appDataPath + '\StockData\\' + str(number))

					currentDate = datetime.today()
					endDate = currentDate - timedelta(days=90)
					response = requests.get("http://jsjustweb.jihsun.com.tw/z/zc/zcn/zcn.djhtm?a="+number+"&d="+str(currentDate.year) + '-' +str(currentDate.month) + '-' +str(currentDate.day) +"&c="+str(endDate.year) + '-' +str(endDate.month) + '-' +str(endDate.day))
					index = response.text.find('nowrap>相抵</TD>')
					strTmp = response.text[index:]
		
					code = 1
					tmp = ''
					liDate = []
					count = 0
					iStructCount = 0
					Total = 0
					
					while code == 1:
						jsonTmp = '{'
						index = strTmp.find('class="t3n0">')

						if index == -1:
							break

						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</TD>')
						year = int(strTmp[0:3]) + 1911
						data = str(year) + '/' + strTmp[4:9]
						liDate.append(data)
						jsonTmp = jsonTmp + '"RoncheDate":"' + str(data) + '", '
						debugStatus = 'Date:' + str(data)

						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						data = int(strTmp[0:indexTD].replace(',', ''))
						jsonTmp = jsonTmp + '"RoncheBuy":"' + str(data) + '", '
						debugStatus = 'RoncheBuy:' + str(data)
						
						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						data = int(strTmp[0:indexTD].replace(',', ''))
						jsonTmp = jsonTmp + '"RoncheSell":"' + str(data) + '", '
						debugStatus = 'RoncheSell:' + str(data)

						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						data = int(strTmp[0:indexTD].replace(',', ''))
						jsonTmp = jsonTmp + '"RoncheReturn":"' + str(data) + '", '
						debugStatus = 'RoncheReturn:' + str(data)

						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						data = int(strTmp[0:indexTD].replace(',', ''))
						jsonTmp = jsonTmp + '"RoncheUse":"' + str(data) + '", '
						debugStatus = 'RoncheUse:' + str(data)

						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						data = int(strTmp[0:indexTD].replace(',', ''))
						jsonTmp = jsonTmp + '"RoncheChange":"' + str(data) + '", '
						debugStatus = 'RoncheChange:' + str(data)

						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						data = int(strTmp[0:indexTD].replace(',', ''))
						jsonTmp = jsonTmp + '"RoncheTotal":"' + str(data) + '", '
						debugStatus = 'RoncheTotal:' + str(data)

						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						data = float(strTmp[0:indexTD].replace('%', ''))
						jsonTmp = jsonTmp + '"RonchePercent":"' + str(data) + '", '
						debugStatus = 'RoncheTotal:' + str(data)
						
						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						data = int(strTmp[0:indexTD].replace(',', ''))
						jsonTmp = jsonTmp + '"ChenSell":"' + str(data) + '", '
						debugStatus = 'ChenSell:' + str(data)

						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						data = int(strTmp[0:indexTD].replace(',', ''))
						jsonTmp = jsonTmp + '"ChenBuy":"' + str(data) + '", '
						debugStatus = 'ChenBuy:' + str(data)

						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						data = int(strTmp[0:indexTD].replace(',', ''))
						jsonTmp = jsonTmp + '"ChenReturn":"' + str(data) + '", '
						debugStatus = 'ChenReturn:' + str(data)

						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						data = int(strTmp[0:indexTD].replace(',', ''))
						jsonTmp = jsonTmp + '"ChenUse":"' + str(data) + '", '
						debugStatus = 'ChenUse:' + str(data)

						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')						
						data = int(strTmp[0:indexTD].replace(',', ''))
						jsonTmp = jsonTmp + '"ChenChange":"' + str(data) + '", '
						debugStatus = 'ChenChange:' + str(data)

						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						if strTmp[0:indexTD].strip() != '':
							data = float(strTmp[0:indexTD].replace('%', ''))
							jsonTmp = jsonTmp + '"ChenTotal":"' + str(data) + '", '
						debugStatus = 'ChenTotal:' + str(data)

						index = strTmp.find('class="t3n1">')
						strTmp = strTmp[index+13:]
						indexTD = strTmp.find('</td>')
						data = int(strTmp[0:indexTD].replace(',', ''))
						jsonTmp = jsonTmp + '"ChenCheSub":"' + str(data) + '" '
						debugStatus = 'ChenCheSub:' + str(data)

						index = strTmp.find('class="t3n1">')
						
						if index == -1:
							jsonTmp = jsonTmp + '}'
							jsonOutput = jsonOutput + jsonTmp
							break
						else:
							jsonTmp = jsonTmp + '}'
							jsonTmp = jsonTmp + ','
							jsonOutput = jsonOutput + jsonTmp
						
				except:
					check = False
					print('Error:' + str(number) + '_' + debugStatus)
				
				if check:
					jsonOutput = jsonOutput + ']'

					f = open(appDataPath + '\StockData\\' + str(number) + '\\' + 'Ronche.txt', 'w', encoding = 'UTF-8')
					f.write(jsonOutput)
					f.close()

					log = ''

					if len(liDate) > 0:
						log = log + 'StartDate:' + liDate[0] + ',EndDate:' + liDate[len(liDate)-1] + ', Error:NA'

					f = open(appDataPath + '\StockData\\' + str(number) + '\\' + 'Ronche_log.txt', 'w', encoding = 'UTF-8')
					f.write(log)
					f.close()
					print(number)
				else:
					f = open(appDataPath + '\StockData\\' + str(number) + 'Ronche_log.txt', 'w', encoding = 'UTF-8')
					f.write('Error:' + str(number) + '_' + debugStatus)
					f.close()
		end = time.time()
		elapsed = end - start
		print(elapsed)		

		
		
	def getKtype(self,stockInfoPath):
		blackHammerPlus=[]
		#blackHammerMinus=[]
		redHammerPlus=[]
		redHigh=[]
		#redHammerMinus=[]
		with open(stockInfoPath, newline='') as f:		
			reader = csv.reader(f)
			i = 0
			for row in reader:
				if row == []:
					continue
				i = i + 1
				
				#number = row[1]
				try:			
					stockInfo = ast.literal_eval(row[0])	
					stockInfoYesterday = ast.literal_eval(row[1])	
					if float(stockInfo.get("Close")) > float(stockInfo.get("Open")):
						if (float(stockInfo.get("Open")) - float(stockInfo.get("Low"))) > (float(stockInfo.get("Close")) - float(stockInfo.get("Open")))*2:
							if (float(stockInfo.get("High")) - float(stockInfo.get("Close"))) < (float(stockInfo.get("Open")) - float(stockInfo.get("Low"))):
								redHammerPlus.append(stockInfo.get("Symbol"))
								print(stockInfo.get("Symbol") + ",red")
					if float(stockInfo.get("Open")) > float(stockInfo.get("Close")):
						if (float(stockInfo.get("Close")) - float(stockInfo.get("Low"))) > (float(stockInfo.get("Open")) - float(stockInfo.get("Close")))*2:
							if (float(stockInfo.get("High")) - float(stockInfo.get("Open"))) < (float(stockInfo.get("Close")) - float(stockInfo.get("Low"))):
								blackHammerPlus.append(stockInfo.get("Symbol"))
								print(stockInfo.get("Symbol") + ",black")

					if float(stockInfo.get("Close"))/float(stockInfoYesterday.get("Close")) > 1.05:
						redHigh.append(stockInfo.get("Symbol"))
						print(stockInfo.get("Symbol") + ",redHigh")
				except:
					pass
		
		allKCollection = []
		allKCollection.append(blackHammerPlus)
		allKCollection.append(redHammerPlus)
		allKCollection.append(redHigh)
		return allKCollection

	def getRedHammerInDownTrend(self,stockInfoPath, targetDate, stockList, threshold):
		with open(stockInfoPath, newline='') as f:		
			reader = csv.reader(f)
			i = 0
			for row in reader:
				if row == []:
					continue
				i = i + 1
				
				#number = row[1]
				try:			
					stockInfo = ast.literal_eval(row[0])	
					if stockInfo.get("Symbol") in stockList:
						j=0
						targetPrice=0
						while j<len(row):
							if datetime.datetime.strptime(ast.literal_eval(row[j]).get('Date'), "%Y-%m-%d") == datetime.datetime.strptime(targetDate, "%Y-%m-%d"):
								targetPrice = float(ast.literal_eval(row[j]).get('Close'))
								break
							j=j+1

						j=0
						count=0
						total=0
						while j<len(row):
							if datetime.datetime.strptime(ast.literal_eval(row[j]).get('Date'), "%Y-%m-%d") < datetime.datetime.strptime(targetDate, "%Y-%m-%d"):
								total=total+1
								if float(ast.literal_eval(row[j]).get('Close')) > targetPrice:
									count = count+1
							j=j+1

						if count/total > threshold:
							print(stockInfo.get("Symbol"))
				except:
					pass

	def getRedEat(self,stockInfoPath, targetDate):
		RedEatList=[]
		#redHammerMinus=[]
		with open(stockInfoPath, newline='') as f:		
			reader = csv.reader(f)
			i = 0
			for row in reader:
				if row == []:
					continue
				i = i + 1
				
				#number = row[1]
				try:			
					stockInfo = ast.literal_eval(row[0])		
					stockInfoYesterday = ast.literal_eval(row[1])
					if float(stockInfo.get("Close")) > float(stockInfo.get("Open")):
						if float(stockInfoYesterday.get("Open")) > float(stockInfoYesterday.get("Close")):
							if (float(stockInfo.get("Close")) > float(stockInfoYesterday.get("High"))) and (float(stockInfo.get("Open")) < float(stockInfoYesterday.get("Low"))):
								print(stockInfo.get("Symbol"))
								RedEatList.append(stockInfo.get("Symbol"))

				except:
					pass
		
		return RedEatList

	def getOBV(self,stockInfoPath, stockList):
		with open(stockInfoPath, newline='') as f:		
			reader = csv.reader(f)
			i = 0
			for row in reader:
				if row == []:
					continue
				i = i + 1
				
				#number = row[1]
				try:			
					stockInfo = ast.literal_eval(row[0])	
					if stockInfo.get("Symbol") in stockList:
						
						count = len(row)
						OBVlist = []
						OBVDaylist = []
						OBV = 0
						yesterdayPrice = 0
						while count > 0:
							count = count -1

							if float(ast.literal_eval(row[count]).get('Close')) > yesterdayPrice:
								OBV = OBV + float(ast.literal_eval(row[count]).get('Volume'))

							if float(ast.literal_eval(row[count]).get('Close')) < yesterdayPrice:
								OBV = OBV - float(ast.literal_eval(row[count]).get('Volume'))
							
							yesterdayPrice = float(ast.literal_eval(row[count]).get('Close'))
							OBVlist.append(OBV)
							OBVDaylist.append(str(ast.literal_eval(row[count]).get('Date')))
						
						Str = stockInfo.get("Symbol") + "  "
						j=0
						while j<len(OBVlist):
							Str = Str + str(OBVDaylist[j]) + ":"
							Str = Str + str(OBVlist[j]) + ", "
							j = j+1
						print(Str)
				except:
					pass

	
				
		
		
						