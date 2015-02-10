from __future__ import division
import csv
import datetime
import math
import os
from dateutil import parser
from matplotlib.pyplot import *
from matplotlib.dates import *
	
localTimezone = -datetime.timedelta(hours=0)	

##################################################################
# GRAPH PILOT DATA
#
# Takes CSV of sleep data (from SleepAsAndroid and proccessed by 
# formatPilotData.py) and graphs all nights of sleep for that user. 
#
# Input: CSV in formatPilotData format
# Output: graphs of sleep, located in "./pilotCharts/userID/",
#			or an error if something fucks up
# 
# To run:
# 	python graphPilotData.py [input file] [userid]
#
# Doc updated: 2/9/15
#
# NOTE: NEED TO MAKE DIR WITH USER ID BEFORE RUNNING BECAUSE I SUCK
#
##################################################################

def print_csv(fields):
	return ','.join([str(i) for i in fields])

def parseDatetime(dt): #2015-04-02 23:57:00
	return datetime.datetime.strptime(dt, "%Y-%d-%m %H:%M:%S")

def getTimestamp(dt):
	return str('%d' % ((dt - datetime.datetime(1970, 1, 1)).total_seconds()*1000))

def getDay(dt): #NOTE: MONTH AND DAY ARE SWITCHED. app records in format that python thinks is month/day but is really day/month
	# return parser.parse(dt).month
	return parseDatetime(dt).day

def makeDatetime(dt):
	return (datetime.datetime.utcfromtimestamp(int(dt)/1000) + localTimezone)

def main():
	csv_file = open(sys.argv[1])
	userid = sys.argv[2]
	csv_reader = csv.reader(csv_file)
	next(csv_reader, None) # skip the header in the csv file
	next_item = next(csv_reader, None)

	while next_item != None: #until all nights are finished
		# asleepDateTime = parser.parse(next_item[1]) #converts asleep time to datetime 
		# wakeUpDateTime = parser.parse(next_item[2])
		asleepDateTime = parseDatetime(next_item[1])
		wakeUpDateTime = parseDatetime(next_item[2])
		day = getDay(next_item[1])

		wakeUpTime = outOfBedTime = makeDatetime(getTimestamp(wakeUpDateTime))
		fallAsleepTime = makeDatetime(getTimestamp(asleepDateTime))

		x = []
		maxs = []
		mins = []
		means = []
		asleep = []

		while next_item != None and day == getDay(next_item[1]): #for all data belonging to the same night (each timestamp)...
			currTimeString = next_item[3]
			# currDatetime = parser.parse(currTimeString)
			currDatetime = parseDatetime(currTimeString)
			values = []
			isAsleep = None

			while next_item != None and currTimeString == next_item[3]: #for all data belonging to the same time point during the night
				if next_item[5]	 != 'None':
					isAsleep = float(next_item[5])* 0.5
				currAccel = next_item[4]
				values.append(float(currAccel))

				next_item = next(csv_reader, None)

			# print currDatetime, currAccel, isAsleep
			asleep.append(isAsleep)
			x.append(currDatetime)
			maxs.append(max(values))
			mins.append(min(values))
			means.append(sum(values)/len(values))

			# print user id, the time (2min interval), the average amount of movement in that 2min, whether asleep or awake
			# print print_csv([userid, sum(values)/len(values), isAwake])

		# print x
		asleep[0] = 0
		plot(x, mins)
		plot(x, maxs)
		fig, ax1 = subplots()
		ax1.xaxis.set_major_formatter(DateFormatter('%H:%M'))
		ax1.yaxis.set_visible(True)
		accelerometerPlot, = ax1.plot(x, means)
		# asleepDots, = ax1.plot(x, asleep, 'r')

		# asleepPlot = axvspan(fallAsleepTime, wakeUpTime, facecolor='orange', edgecolor='none', alpha=0.2)
		# bedPlot = axvspan(fallAsleepTime, outOfBedTime, facecolor='orange', edgecolor='none', alpha=0.3)
		#make the legend
		# legend([ accelerometerPlot, asleepDots], ['movement', 'awake'], loc=9, ncol=5)
		# legend([ accelerometerPlot, bedPlot, asleepPlot], ['movement', 'bed', 'asleep'], loc=9, ncol=5)
		legend([ accelerometerPlot], ['movement'], loc=9, ncol=5)

		gcf().autofmt_xdate()
		# try:
		savefig('pilotCharts/' + userid + '/' + str(fallAsleepTime).replace(':', '') + '.png', bbox_inches='tight')
		# except:
		# 	print "error:", userid, fallAsleepTime
		close(fig)
		del fig

if __name__ == '__main__':
	if len(sys.argv) < 3:
			sys.stderr.write('Please provide the name of the infile and user id as command line arguments.\n')
			sys.exit(1)
	else:
		main()

