from flask import Flask, render_template
from flask import request
import csv
from time import gmtime, strftime
from datetime import datetime


app = Flask(__name__)
  
@app.route('/')

@app.route('/homepage')
def index():
	return render_template('homepage.html')
	
@app.route('/booking_1')	
def booking_1():
	return render_template('booking_1.html')
	
@app.route('/booking_2')	
def booking_2():

	with open('static/stations.csv', 'r') as inFile:
		reader = csv.reader(inFile)
		stations = [row for row in reader]# For each row in the reader create a row in a List. //
		stations.reverse()
	with open('static/hours.csv', 'r') as inFile:
		reader = csv.reader(inFile)
		hours = [row for row in reader]# For each row in the reader create a row in a List. //
	
	with open('static/minutes.csv', 'r') as inFile:
		reader = csv.reader(inFile)
		minutes = [row for row in reader]# For each row in the reader create a row in a List. //
	
	return render_template('booking_2.html', stations = stations, hours = hours, minutes =  minutes )
	
@app.route('/booking_3')	
def booking_3():

	with open('static/saveddepart.csv', 'r') as inFile:
		reader = csv.reader(inFile)
		tickList = [row for row in reader]
		
	with open('static/savedReturn.csv', 'r') as inFile:
		reader = csv.reader(inFile)
		tickList2 = [row for row in reader]
	
	with open('static/ticktype.csv', 'r') as inFile:
		reader = csv.reader(inFile)
		ticks = [row for row in reader]
		ticks.reverse()
		
	tickList.reverse()
	tickList2.reverse()
	tickType = ticks[0]
	return render_template('booking_3.html', tickList = tickList , tickList2 = tickList2, tickType = tickType )
	
@app.route('/booking_4')	
def booking_4():
	return render_template('booking_4.html')
	
@app.route('/delays')	
def delays():
	return render_template('delays.html')
	
@app.route('/delays_2')	
def delays_2():

	with open('static/issueFile.csv', 'r') as inFile:
		reader = csv.reader(inFile)
		aList = [row for row in reader]# For each row in the reader create a row in a List. //
		aList.reverse()

	return render_template('delays_2.html', aList = aList)
	


@app.route('/delay_report')
def delay_report():
		return render_template('delay_report.html')

@app.route('/bookTimes', methods =['POST'])
def bookTimes():
	with open('static/stations.csv', 'r') as inFile:
		reader = csv.reader(inFile)
		stations = [row for row in reader]# For each row in the reader create a row in a List. //
		stations.reverse()
	needed = stations[0]
	toStation = needed[0]
	fromStation = needed[1]
	
	tickType = request.form[('options')]
	if tickType == '1':
		toDate = request.form[('startDate')]
		toHours = request.form[('hours1')]
		toMins = request.form[('minutes1')]
		
		TicketFile = 'static/ticket1.csv'
		TicketList = readFile(TicketFile)
		
		TrainTicket = [tickType, toStation, fromStation, toDate, toHours, toMins]
		TicketList.append(TrainTicket)
		
		writeFile(TicketList, TicketFile)
		TicketList.reverse()
		time = [toHours,toMins]
		time2 = getOnelower(time[0], time[1])
		time3 = getOnelower(time2[0], time2[1])
		time4 = getOnehigher(time[0], time[1])
		time5 = getOnehigher(time4[0], time4[1])
		timeList = [time3, time2, time, time4, time5]
		tickList= getListOftickets(timeList)
		
		
		testFile = 'static/ticket_data.csv'
		
		writeFile(tickList,testFile )
		

		return render_template('booking_3.html', tickList = tickList , tickType = tickType)
	elif tickType == '2':
		toDate = request.form[('startDate')]
		toHours = request.form[('hours1')]
		toMins = request.form[('minutes1')]
		fromDate = request.form[('returnDate')]
		fromHours = request.form[('hours2')]
		fromMins = request.form[('minutes2')]
		TicketFile = 'static/ticket1.csv'
		TicketList = readFile(TicketFile)
		
		TrainTicket = [tickType, toStation, fromStation, toDate, toHours, toMins,fromDate, fromHours, fromMins]
		TicketList.append(TrainTicket)
		
		writeFile(TicketList, TicketFile)
		TicketList.reverse()
		time = [toHours,toMins]
		time2 = getOnelower(time[0], time[1])
		time3 = getOnelower(time2[0], time2[1])
		time4 = getOnehigher(time[0], time[1])
		time5 = getOnehigher(time4[0], time4[1])
		timeList = [time3, time2, time, time4, time5]
		tickList= getListOftickets(timeList)
		time_1 = [fromHours,fromMins]
		time_2 = getOnelower(time_1[0], time_1[1])
		time_3 = getOnelower(time_2[0], time_2[1])
		time_4 = getOnehigher(time_1[0], time_1[1])
		time_5 = getOnehigher(time_4[0], time_4[1])
		timeList2 = [time_3, time_2, time_1, time_4, time_5]
		tickList2= getListOftickets(timeList2)
		tickList.reverse()
		testFile1 = 'static/saveddepart.csv'
		tickList2.reverse()
		
		
		testFile2 = 'static/savedReturn.csv'
		writeFile(tickList2,testFile2)
		
		testFile1 = 'static/saveddepart.csv'
		writeFile(tickList,testFile1)
		
		
		
		testFile3 =  'static/ticktype.csv'
		writeFile(tickType, testFile3)
		tickList.reverse()
		tickList2.reverse()
		
		return render_template('booking_3.html', tickList = tickList , tickList2 = tickList2, tickType = tickType)
		
		
def getListOftickets(tickList):
	tickets = list()
	with open('static/times-prices.csv', 'r') as inFile :
		reader = csv.reader(inFile)
		ticketprices = [row for row in reader]
		
	for line in tickList:
		hours = line[0]
		minutes = line[1]
		for tick in ticketprices:
			if ( tick[1] == hours and tick[2] == minutes):
				tickets.append(tick)
				break
 
 
	return tickets
	
		
		
		
		
		
		
def getOnelower(hours, minutes):

	if minutes == '0':
		hours = int(hours) - 1
		minutes = '45'
		time = [str(hours), minutes]
		return time
	elif minutes == '15':
		hours = hours
		minutes = '0'
		time = [hours, minutes]
		return time
	elif minutes == '30':
		hours = hours
		minutes = '15'
		time = [hours, minutes]
		return time
	elif minutes == '45':
		hours = hours
		minutes = '30'
		time = [hours, minutes]
		return time

def getOnehigher(hours, minutes):

	if minutes == '45':
		hours = int(hours) + 1
		minutes = '0'
		time = [str(hours), minutes]
		return time
	elif minutes == '30':
		hours = hours
		minutes = '45'
		time = [hours, minutes]
		return time
	elif minutes == '15':
		hours = hours
		minutes = '30'
		time = [hours, minutes]
		return time
	elif minutes == '0':
		hours = hours
		minutes = '15'
		time = [hours, minutes]
		return time


		
		
@app.route('/issueFilter', methods=['POST'])
def issueFilter():

	station = request.form[('station')]
	if station != 'All':
		with open('static/issueFile.csv', 'r') as inFile:
			reader = csv.reader(inFile)
			aList = [row for row in reader]# For each row in the reader create a row in a List. //
			aList.reverse()
			bList = [row for row in aList]
			aList = list()
			for row in bList:
				if row[0] == station :
					aList.append(row)
			


		return render_template('delays_2.html', aList = aList)
	else:
		with open('static/issueFile.csv', 'r') as inFile:
			reader = csv.reader(inFile)
			aList = [row for row in reader]# For each row in the reader create a row in a List. //
			aList.reverse()
	return render_template('delays_2.html', aList = aList)

@app.route('/issueFilter2', methods=['POST'])
def issueFilter2():

	station = request.form[('station')]
	if station != 'All':
		with open('static/issueFile.csv', 'r') as inFile:
			reader = csv.reader(inFile)
			aList = [row for row in reader]# For each row in the reader create a row in a List. //
			aList.reverse()
			bList = [row for row in aList]
			aList = list()
			for row in bList:
				if row[0] == station :
					aList.append(row)
			


		return render_template('delays_2.html', aList = aList)
	else:
		with open('static/issueFile.csv', 'r') as inFile:
			reader = csv.reader(inFile)
			aList = [row for row in reader]# For each row in the reader create a row in a List. //
			aList.reverse()
	return render_template('delays_2.html', aList = aList)
	
#@app.route('/listen1')
#def listen1():
#	#if request.form['submitbutton'] == 'remove from file':
#		f = open("static/stations.csv", "w")
#		f.truncate()
#		f.close()
#		return render_template('booking_1.html')
#	elif request.form['submitbutton'] == 'next':
#		return render_template('booking_3.html')
#		










	
@app.route('/bookStation', methods=['POST'])
def bookStation():
	stationFile = 'static/stations.csv'
	stationList = readFile(stationFile)

	station1 = request.form[('station1')]
	station2 = request.form[('station2')]
	
	trainStations = [station1, station2]
	stationList.append(trainStations)
	
	writeFile(stationList, stationFile)
	
	with open('static/stations.csv', 'r') as inFile:
		reader = csv.reader(inFile)
		stations = [row for row in reader]# For each row in the reader create a row in a List. //
		stations.reverse()
		
	with open('static/hours.csv', 'r') as inFile:
		reader = csv.reader(inFile)
		hours = [row for row in reader]# For each row in the reader create a row in a List. //
	
	with open('static/minutes.csv', 'r') as inFile:
		reader = csv.reader(inFile)
		minutes = [row for row in reader]# For each row in the reader create a row in a List. //
		
	return render_template('booking_2.html', stations = stations, hours = hours, minutes =  minutes)


	
@app.route('/addIssue', methods=['POST']) 
def addIssue():
   # read the issues from the csv
	issueFile = 'static/issueFile.csv'
	issueList = readFile(issueFile)
   
   # add the new entry
	station = request.form[('station')]
	issue = request.form[('issueText')]
	time= strftime("%d-%m-%Y %H:%M", gmtime())
   
   
	newIssue = [station, issue, time]
	issueList.append(newIssue)
   
   # save the updated issue list back to the file
	writeFile(issueList, issueFile)
   
	with open('static/issueFile.csv', 'r') as inFile:
		reader = csv.reader(inFile)
		aList = [row for row in reader]# For each row in the reader create a row in a List. //
		aList.reverse()
	    
	return render_template('delays_2.html', aList = aList)
		
	
def readFile(aFile):
#read in 'aFile'
   with open(aFile, 'r') as inFile:
      reader = csv.reader(inFile)
      theList = [row for row in reader]
   return theList
	
def writeFile(aList, aFile):
#write 'aList' to 'aFile'
   with open(aFile, 'w', newline='') as outFile:
      writer = csv.writer(outFile)
      writer.writerows(aList)
   return
	
	
	
	
if __name__ == '__main__':
    app.run(debug = True)

	