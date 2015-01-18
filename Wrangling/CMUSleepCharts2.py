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

print csv(["userid", "currDatetime", "dayOfWeek", "timeSlept", "fallAsleepTime", "wakeUpTime", "outOfBedTime", "moveEvent", "sleepQuality", "timeToFallAsleep", "beforeMidnight", "isWeekend"])

# for filename in os.listdir('data/')[0:1]: #select only a small number
for filename in os.listdir('data/'):

	if not filename.endswith('.sqlite'):
		continue
	userid = filename[:-7]
	averageBedtime = (1000, 0)
	averageTimeSlept = 0
	
	conn = sqlite3.connect('data/' + userid + '.sqlite')
	c = conn.cursor()
	
	results = c.execute('select go_to_bed_time from diary_sleep')
	
	for res in results.fetchall():
		timeOfInterest = parser.parse(res[0])

		###################	
		outOfBedTime = parser.parse(c.execute('select out_of_bed_time from diary_sleep where go_to_bed_time = "' + res[0] + '"').fetchone()[0])
		fallAsleepTimeSeconds = int(int(getTimestamp(parser.parse(c.execute('select fall_asleep_time from diary_sleep where go_to_bed_time = "' + res[0] + '"').fetchone()[0])))/1000)
		fallAsleepTime = parser.parse(c.execute('select fall_asleep_time from diary_sleep where go_to_bed_time = "' + res[0] + '"').fetchone()[0])
		wakeUpTimeSeconds = int(int(getTimestamp(parser.parse(c.execute('select wake_up_time from diary_sleep where go_to_bed_time = "' + res[0] + '"').fetchone()[0])))/1000)
		wakeUpTime = parser.parse(c.execute('select wake_up_time from diary_sleep where go_to_bed_time = "' + res[0] + '"').fetchone()[0])
		sleepQuality = c.execute('select sleep_quality from diary_sleep where go_to_bed_time = "' + res[0] + '"').fetchone()[0]
		
		###################	GET ACCELERATION AT EVERY POINT DURING THE NIGHT ###################
		results = c.execute('select * from log_accelerometer ' + whereSleepDate(timeOfInterest))

		# do we want raw accelerometer readings or change in accelerometer?
		# change in accelerometer values seems to work better
		maxs = []
		mins = []
		means = []
		prevX = prevY = prevZ = None
		moveEvents = 0
		for result in results.fetchall():
			if not result[1]:
				continue

			values = []
			for i in result[1].split('|'):
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
			print currDatetime
			maxs.append(max(values))
			mins.append(min(values))
			means.append(sum(values)/len(values))

			if round(sum(values)/len(values)) > 1.0:
				moveEvents += 1
		#########################################################################################

		if fallAsleepTime.hour > 12:
			averageBedtime = ( (averageBedtime[0] - 24) + fallAsleepTime.hour, averageBedtime[1] + 1)
		else:
			averageBedtime = (averageBedtime[0] + fallAsleepTime.hour, averageBedtime[1] + 1)

		currDatetimeDay = timeOfInterest.day
		currDatetimeHour = timeOfInterest.hour
		currDatetimeSeconds = int(int(getTimestamp(timeOfInterest))/1000)
		dayOfWeek = timeOfInterest.weekday()

		if (dayOfWeek == 4) or (dayOfWeek == 5): #friday or saturday
			isWeekend = 1
		else:
			isWeekend = 0

		timeToFallAsleep = int((fallAsleepTimeSeconds - currDatetimeSeconds)/60) #in minutes

		if currDatetimeHour >= 18:
			beforeMidnight = 1
		else:
			beforeMidnight = 0

		timeSlept = int((wakeUpTimeSeconds - fallAsleepTimeSeconds) / 60) # in minutes

			# print csv([int(result[0] / 1000), max(values), min(values), round(sum(values)/len(values), 1)])
		# print csv([userid, currDatetimeDay, dayOfWeek, timeSlept, fallAsleepTime.hour, wakeUpTime.hour, outOfBedTime.hour, moveEvents, sleepQuality, timeToFallAsleep, beforeMidnight, isWeekend])
		
