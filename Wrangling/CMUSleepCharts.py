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

for filename in os.listdir('data/'):
	if not filename.endswith('.sqlite'):
		continue
	userid = filename[:-7]

	conn = sqlite3.connect('data/' + userid + '.sqlite')
	c = conn.cursor()
	
	def csv(fields):
		return ','.join([str(i) for i in fields])
	
	def getTimestamp(dt):
		return str('%d' % ((dt - datetime.datetime(1970, 1, 1)).total_seconds()*1000))
	
	def whereSleepDate(dt):
		sleepDateStart = dt - localTimezone - preSleepBuffer
		sleepDateEnd = sleepDateStart + datetime.timedelta(hours=numHours)
		return 'where timestamp >= ' + getTimestamp(sleepDateStart) + ' and timestamp < ' + getTimestamp(sleepDateEnd)

	results = c.execute('select go_to_bed_time from diary_sleep')
	for res in results.fetchall():
		timeOfInterest = parser.parse(res[0])
	
		results = c.execute('select * from log_microphone ' + whereSleepDate(timeOfInterest))
		
		x = []
		maxs = []
		mins = []
		means = []
		for result in results.fetchall():
			if result[1]:
				values = [int(i) for i in result[1].split(',')]
				x.append(datetime.datetime.utcfromtimestamp(int(result[0]/1000)) + localTimezone)
				maxs.append(max(values))
				mins.append(min(values))
				means.append(sum(values)/len(values))
				#print csv([int(result[0] / 1000), max(values), min(values), round(sum(values)/len(values), 1)])
		
		#plot(x, mins)
		#plot(x, maxs)
		fig, ax1 = subplots()
		ax1.xaxis.set_major_formatter(DateFormatter('%H:%M'))
		ax1.yaxis.set_visible(False)
		microphonePlot, = ax1.plot(x, means)
		
		results = c.execute('select * from log_accelerometer ' + whereSleepDate(timeOfInterest))
		
		# do we want raw accelerometer readings or change in accelerometer?
		# change in accelerometer values seems to work better
		x = []
		maxs = []
		mins = []
		means = []
		prevX = prevY = prevZ = None
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
			x.append(datetime.datetime.utcfromtimestamp(int(result[0]/1000)) + localTimezone)
			maxs.append(max(values))
			mins.append(min(values))
			means.append(sum(values)/len(values))
			#print csv([int(result[0] / 1000), max(values), min(values), round(sum(values)/len(values), 1)])
	
		#plot(x, mins)
		#plot(x, maxs)
		ax2 = ax1.twinx()
		ax2.yaxis.set_visible(False)
		accelerometerPlot, = ax2.plot(x, means, 'g-')
		
		results = c.execute('select * from log_light_sensor ' + whereSleepDate(timeOfInterest))
		
		x = []
		maxs = []
		mins = []
		means = []
		for result in results.fetchall():
			if result[1] and result[1] != 'null':
				values = [float(i) for i in result[1].split(',')]
				x.append(datetime.datetime.utcfromtimestamp(int(result[0]/1000)) + localTimezone)
				maxs.append(max(values))
				mins.append(min(values))
				means.append(sum(values)/len(values))
				#print csv([int(result[0] / 1000), max(values), min(values), round(sum(values)/len(values), 1)])
		
		#plot(x, mins)
		#plot(x, maxs)
		ax3 = ax1.twinx()
		ax3.yaxis.set_visible(False)
		lightSensorPlot, = ax3.plot(x, means, 'r-')

		outOfBedTime = parser.parse(c.execute('select out_of_bed_time from diary_sleep where go_to_bed_time = "' + res[0] + '"').fetchone()[0])
		bedPlot = axvspan(timeOfInterest, outOfBedTime, facecolor='orange', edgecolor='none', alpha=0.3)
		fallAsleepTime = parser.parse(c.execute('select fall_asleep_time from diary_sleep where go_to_bed_time = "' + res[0] + '"').fetchone()[0])
		wakeUpTime = parser.parse(c.execute('select wake_up_time from diary_sleep where go_to_bed_time = "' + res[0] + '"').fetchone()[0])
		asleepPlot = axvspan(fallAsleepTime, wakeUpTime, facecolor='grey', edgecolor='none', alpha=0.2)

		legend([microphonePlot, accelerometerPlot, lightSensorPlot, bedPlot, asleepPlot], ['noise', 'movement', 'light', 'bed', 'asleep'], loc=9, ncol=5)

		gcf().autofmt_xdate()
		try:
			savefig('outputCharts/' + userid + '.' + str(timeOfInterest).replace(':', '') + '.png', bbox_inches='tight')
		except:
			# why is this happening?
			print "error:", userid, timeOfInterest
		close(fig)
		del fig