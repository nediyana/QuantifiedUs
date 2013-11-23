import time
import datetime
import sys
import itertools
import numpy
from pylab import *

# REMARKS
#
# input_schedule_csv fields: startDate in '%Y-%m-%d', startTime in '%H:%M:%S', duration in '%H:%M:%S', projectName, category, description

# PARAMETERS
EARLIEST_DATE = datetime.date(2013, 8, 1)
ACTIVITIES = ['Sleeping'] # activities that will be charted
CATEGORIES = ['Work'] # categories that will be charted. alternate values: ['Uncategorized'] or ['Work', 'Uncategorized']
WEEKLY_OR_DAILY = 'both' # alternate values: 'daily', 'weekly'

def main(input_schedule_csv, output_prefix):
	def HHMMToMinutes(hhmm):
		hhmmsplit = hhmm.split(':')
		(hh, mm, ss) = tuple(hhmmsplit)
		assert(int(ss) == 0)
		return int(hh) * 60 + int(mm)

	def chunks(l, n):
		for i in xrange(0, len(l), n):
			yield l[i:i+n]
	
	def process(startDate, startTime, duration, activity, d):
		if startTime + duration > 60 * 24:
			process(startDate + datetime.timedelta(1), 0, startTime + duration - 60 * 24, activity, d)
			duration = 60 * 24 - startTime
		if startDate < EARLIEST_DATE:
			return
		if startDate not in d:
			d[startDate] = {}
		if activity not in d[startDate]:
			d[startDate][activity] = 0
		d[startDate][activity] += duration

	def getActivityNames(filepath):
		ActivityNames = set()
		for line in open(filepath, 'rU'):
			(startDate, startTime, duration, activity, category, description) = line.split(',')
			if activity in ACTIVITIES or category in CATEGORIES:
				ActivityNames.add(activity)
		return list(ActivityNames)

	def generateChart(datas, dates, aggregation):
		names = sorted(datas.keys(), key=lambda name: sum(datas[name]), reverse=True)
		minutes = [datas[ActivityName] for ActivityName in names]
		if aggregation == 'weekly':
			minutes = [[sum(t) for t in chunks(activityMinutes, 7)] for activityMinutes in minutes]
			dates = dates[::7]
		output = []
		for index, name in enumerate(names):
			output.append({'key': name, 'values': [[dates[idx], m] for idx, m in enumerate(minutes[index])]}) 
		with open(output_prefix + '.' + aggregation + '.json', 'w') as out:
			out.write(str(output).replace("'", '"'));

	d = {}
	for line in open(input_schedule_csv, 'rU'):
		(startDate, startTime, duration, activity, category, description) = line.split(',')
		startTime = HHMMToMinutes(startTime)
		duration = HHMMToMinutes(duration)
		year, month, day = [int(i) for i in startDate.split('-')]
		startDate = datetime.date(year, month, day)
		if activity in ACTIVITIES or category in CATEGORIES:
			process(startDate, startTime, duration, activity, d)
	
	dates = []
	datas = {}
	activityNames = getActivityNames(input_schedule_csv)
	for activityName in activityNames:
		datas[activityName] = []
	for date in sorted(d):
		dates.append(int(date2num(date))) # convert to unix epoch in milliseconds
		for activityName in activityNames:
			datas[activityName].append(0)
		dayTotal = 0
		for k in sorted(d[date], key=d[date].get, reverse=True):
			datas[k][-1] = d[date][k]
			dayTotal += d[date][k]
	
	if WEEKLY_OR_DAILY == 'weekly' or 'both':
		generateChart(datas, dates, 'weekly')
	if WEEKLY_OR_DAILY == 'daily' or 'both':
		generateChart(datas, dates, 'daily')
	
if __name__ == "__main__":
	if len(sys.argv) < 3:
		print 'Usage: ' + sys.argv[0] + ' input_schedule_csv output_prefix'
	else:
		main(sys.argv[1], sys.argv[2])
