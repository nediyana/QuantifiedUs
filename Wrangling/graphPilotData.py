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

################################################
# print_csv
# input: list of things to be comma-separated
# output: print correct format for CSV
################################################
def print_csv(fields):
	return ','.join([str(i) for i in fields])

################################################
# parseDatetime 
# input: string of the form "%Y-%d-%m %H:%M:%S"
# output: datetime object
################################################
def parseDatetime(dt): #2015-04-02 23:57:00
	return datetime.datetime.strptime(dt, "%Y-%d-%m %H:%M:%S")

################################################
# getTimestamp 
# input: datetime object
# output: total seconds since epoch
################################################
def getTimestamp(dt):
	return int('%d' % ((dt - datetime.datetime(1970, 1, 1)).total_seconds()*1000))

################################################
# makeDatetime
# input: total seconds since epoch
# output: datetime object
################################################
def makeDatetime(t):
	return (datetime.datetime.utcfromtimestamp(int(t)/1000) + localTimezone)

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
		day = asleepDateTime.day

		wakeUpTime = outOfBedTime = wakeUpDateTime
		fallAsleepTime = asleepDateTime

		x = []
		maxs = []
		mins = []
		means = []
		asleep = []
		noise = []

		while next_item != None and day == parseDatetime(next_item[1]).day: #for all data belonging to the same night (each timestamp)...
			currTimeString = next_item[3]
			# currDatetime = parser.parse(currTimeString)
			currDatetime = parseDatetime(currTimeString)
			values = []
			isAsleep = None

			while next_item != None and currTimeString == next_item[3]: #for all data belonging to the same time point during the night
				### movement data
				if next_item[5]	 != 'None':
					isAsleep = float(next_item[5])* 0.5
				currAccel = next_item[4]
				values.append(float(currAccel))

				### noise data
				if next_item[6] != "None":
					noise.append(round(float(next_item[6])))

				next_item = next(csv_reader, None)

			asleep.append(isAsleep)
			x.append(currDatetime)
			maxs.append(max(values))
			mins.append(min(values))
			means.append(sum(values)/len(values))

			# print user id, the time (2min interval), the average amount of movement in that 2min, whether asleep or awake
			# print print_csv([userid, sum(values)/len(values), isAwake])

		### PLOT MOVEMENT
		plot(x, mins)
		plot(x, maxs)
		# fig, axr = subplots(2, sharex=True)
		# ax1 = axr[0]
		# ax2 = axr[1]
		fig, ax1 = subplots()
		if asleepDateTime.date() == wakeUpTime.date(): #if they went to bed after midnight
			first_time = ( asleepDateTime-datetime.timedelta(1) ).replace(hour=21, minute=00)
			last_time = wakeUpDateTime.replace(hour=11, minute=59)
		else:
			first_time = asleepDateTime.replace(hour=20, minute=00)
			last_time = wakeUpDateTime.replace(hour=11, minute=59)
		ax1.xaxis.set_major_formatter(DateFormatter('%H:%M'))
		ax1.yaxis.set_visible(True)
		ax1.set_xlabel('Time (HH:MM)')
		ax1.set_ylabel('Acceleration')
		ax1.tick_params(axis='y', colors='b')
		ax1.set_ylim(0, 2)
		ax1.yaxis.label.set_color('b')
		
		accelerometerPlot = ax1.bar(x, means, 0.0001, color='b', edgecolor = 'b')
		for tl in ax1.get_yticklabels():
			tl.set_color('b')

		# asleepDots, = ax1.plot(x, asleep, 'ro')

		### calculate noise x labels
		start_x = getTimestamp(x[0])
		end_x = getTimestamp(x[len(x)-1])
		increment = int( (end_x - start_x) / len(noise) )
		noise_x = []
		curr_x = start_x + increment
		while curr_x < end_x:
			noise_x.append(makeDatetime(curr_x))
			curr_x += increment

		### PLOT NOISE
		plot(noise_x, noise)
		ax2 = ax1.twinx()
		ax2.yaxis.set_visible(True)
		ax2.yaxis.label.set_color('g')
		ax2.set_ylabel('Noise')
		ax2.tick_params(axis='y', colors='g')
		ax2.set_ylim(0, 3000)
		noisePlot = ax2.bar(noise_x, noise, 0.0001, color='g', edgecolor = 'g')
		for tl in ax2.get_yticklabels():
			tl.set_color('g')

		ax1.set_xlim(first_time, last_time) #need to call this last or limits will be overridden

		ax1.set_title('User ' + str(userid)+  ', Date: ' + str(first_time.date()) )
		

		# asleepPlot = axvspan(fallAsleepTime, wakeUpTime, facecolor='orange', edgecolor='none', alpha=0.2)
		# bedPlot = axvspan(fallAsleepTime, outOfBedTime, facecolor='orange', edgecolor='none', alpha=0.3)
		
		#make the legend
		# legend([ accelerometerPlot, asleepDots], ['movement', 'awake'], loc=9, ncol=5)
		# legend([ accelerometerPlot, bedPlot, asleepPlot], ['movement', 'bed', 'asleep'], loc=9, ncol=5)
		# legend([ accelerometerPlot], ['movement'], loc=9, ncol=5)
		# legend([ accelerometerPlot, noisePlot], ['movement', 'noise'], loc=9, ncol=5)

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

