from __future__ import division
import sqlite3
import datetime
import math
import os
from dateutil import parser
from matplotlib.pyplot import *
from matplotlib.dates import *

localTimezone = -datetime.timedelta(hours=4)
preSleepBuffer = datetime.timedelta(hours=4)
numHours = 20 # 4 hours before, 4 hours after, 12 hours of sleep

def csv(fields):
	return ','.join([str(i) for i in fields])
	
def getTimestamp(dt):
	return str('%d' % ((dt - datetime.datetime(1970, 1, 1)).total_seconds()*1000))

def whereSleepDate(dt):
	sleepDateStart = dt - localTimezone - preSleepBuffer
	sleepDateEnd = sleepDateStart + datetime.timedelta(hours=numHours)
	return 'where timestamp >= ' + getTimestamp(sleepDateStart) + ' and timestamp < ' + getTimestamp(sleepDateEnd)

######### PRINT CSV HEADER #########
# print csv(["userid", "currDatetime", "timeSlept", "fallAsleepTime", "wakeUpTime", "outOfBedTime", "moveEvent", "sleepQuality", "timeToFallAsleep", "beforeMidnight"])
####################################

for filename in os.listdir('data/'): #for each file (each person)

	if not filename.endswith('.sqlite'): #check file type (must be .sqlite)
		continue
	userid = filename[:-7]
	
	conn = sqlite3.connect('data/' + userid + '.sqlite')
	c = conn.cursor()
	
	results = c.execute('select go_to_bed_time from diary_sleep') #for each night, get their self-reported go-to-bed time
	# print results
	for res in results.fetchall(): #for each night
		timeOfInterest = parser.parse(res[0]) #the time they say they fell asleep is our time of interest

		###################	
		outOfBedTime = parser.parse(c.execute('select out_of_bed_time from diary_sleep where go_to_bed_time = "' + res[0] + '"').fetchone()[0])
		fallAsleepTimeSeconds = int(int(getTimestamp(parser.parse(c.execute('select fall_asleep_time from diary_sleep where go_to_bed_time = "' + res[0] + '"').fetchone()[0])))/1000)
		fallAsleepTime = parser.parse(c.execute('select fall_asleep_time from diary_sleep where go_to_bed_time = "' + res[0] + '"').fetchone()[0])
		wakeUpTimeSeconds = int(int(getTimestamp(parser.parse(c.execute('select wake_up_time from diary_sleep where go_to_bed_time = "' + res[0] + '"').fetchone()[0])))/1000)
		wakeUpTime = parser.parse(c.execute('select wake_up_time from diary_sleep where go_to_bed_time = "' + res[0] + '"').fetchone()[0])
		sleepQuality = c.execute('select sleep_quality from diary_sleep where go_to_bed_time = "' + res[0] + '"').fetchone()[0]
		
		###################	
		results = c.execute('select * from log_accelerometer ' + whereSleepDate(timeOfInterest))
		# results is for all times in 20-hour window (4 hrs before self-reported asleep time, 16 hours after that)

		# do we want raw accelerometer readings or change in accelerometer?
		# change in accelerometer values seems to work better <-- yup, that (danae agrees with jeff).
		x = []
		maxs = []
		mins = []
		means = []
		prevX = prevY = prevZ = None
		moveEvents = 0

		for result in results.fetchall(): #for each time point in 20 hour window
			if not result[1]:
				continue

			values = []
			# count = 0
			for i in result[1].split('|'): #for each acceleration reading per time point (150-600 of these per 2min)
				# count += 1
				currX, currY, currZ = [float(v) for v in i.split(',')]
				if prevX is None:
					prevZ = currZ
					prevY = currY
					prevX = currX
					continue
				values.append(math.sqrt((currZ - prevZ) ** 2 + (currY - prevY) ** 2 + (currX - prevX) ** 2))
				prevZ = currZ
				prevY = currY
				prevX = currX
			currDatetime = (datetime.datetime.utcfromtimestamp(int(result[0]/1000)) + localTimezone)
			currDatetimeDay = currDatetime.day
			currDatetimeHour = currDatetime.hour
			currDatetimeMinute = currDatetime.minute
			currDatetimeSeconds = int(int(getTimestamp(currDatetime))/1000)
			x.append(currDatetime)
			# maxs.append(max(values))
			# mins.append(min(values))
			# means.append(sum(values)/len(values))
			# print count

			if round(sum(values)/len(values)) > 1.0:
				moveEvents += 1

			#figure out whether asleep by self-reported data
			isAsleep = 0
			if currDatetimeSeconds > fallAsleepTimeSeconds and currDatetimeSeconds < wakeUpTimeSeconds:
				isAsleep = 1
			
			# print user id, the time (2min interval), the average amount of movement in that 2min, whether asleep or awake
			print csv([userid, sum(values)/len(values), isAsleep])

			timeToFallAsleep = fallAsleepTimeSeconds - int(result[0] / 1000)
			if currDatetimeHour >= 18:
				beforeMidnight = "True"
			else:
				beforeMidnight = "False"

			# print csv([userid, timeOfInterest, currDatetimeSeconds, int(result[0] / 1000), max(values), min(values), round(sum(values)/len(values))])
			# print csv([int(result[0] / 1000), max(values), min(values), round(sum(values)/len(values), 1)])
		# print csv([userid, currDatetimeDay, int(result[0] / 1000), fallAsleepTime, wakeUpTime, outOfBedTime, moveEvents, sleepQuality, timeToFallAsleep, beforeMidnight])
		

		########################

		#plot(x, mins)
		#plot(x, maxs)
		# ax2 = ax1.twinx()
		# ax2.yaxis.set_visible(False)
		# accelerometerPlot, = ax2.plot(x, means, 'g-')
		
		# results = c.execute('select * from log_light_sensor ' + whereSleepDate(timeOfInterest))
		
		# x = []
		# maxs = []
		# mins = []
		# means = []
		# for result in results.fetchall():
		# 	if result[1] and result[1] != 'null':
		# 		values = [float(i) for i in result[1].split(',')]
		# 		x.append(datetime.datetime.utcfromtimestamp(int(result[0]/1000)) + localTimezone)
		# 		maxs.append(max(values))
		# 		mins.append(min(values))
		# 		means.append(sum(values)/len(values))
		# 		#print csv([int(result[0] / 1000), max(values), min(values), round(sum(values)/len(values), 1)])
		
		# #plot(x, mins)
		# #plot(x, maxs)
		# ax3 = ax1.twinx()
		# ax3.yaxis.set_visible(False)
		# lightSensorPlot, = ax3.plot(x, means, 'r-')

		# outOfBedTime = parser.parse(c.execute('select out_of_bed_time from diary_sleep where go_to_bed_time = "' + res[0] + '"').fetchone()[0])
		# bedPlot = axvspan(timeOfInterest, outOfBedTime, facecolor='orange', edgecolor='none', alpha=0.3)
		# fallAsleepTime = parser.parse(c.execute('select fall_asleep_time from diary_sleep where go_to_bed_time = "' + res[0] + '"').fetchone()[0])
		# wakeUpTime = parser.parse(c.execute('select wake_up_time from diary_sleep where go_to_bed_time = "' + res[0] + '"').fetchone()[0])
		# asleepPlot = axvspan(fallAsleepTime, wakeUpTime, facecolor='grey', edgecolor='none', alpha=0.2)

		# legend([microphonePlot, accelerometerPlot, lightSensorPlot, bedPlot, asleepPlot], ['noise', 'movement', 'light', 'bed', 'asleep'], loc=9, ncol=5)

		# gcf().autofmt_xdate()
		# try:
		# 	savefig('outputCharts/' + userid + '.' + str(timeOfInterest).replace(':', '') + '.png', bbox_inches='tight')
		# except:
		# 	# why is this happening?
		# 	print "error:", userid, timeOfInterest
		# close(fig)
		# del fig