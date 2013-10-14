import numpy
import datetime
import sys
import itertools
from pylab import *

# REMARKS
#
# The extension in output_chart_name determines the file type
# input_schedule_csv fields: startDate in '%Y-%m-%d', startTime in '%H:%M:%S', duration in '%H:%M:%S', projectName, category, description

# PARAMETERS
EARLIEST_DATE = datetime.date(2013, 8, 1)
CATEGORIES = ['Work'] # categories that will be charted. alternate values: ['Uncategorized'] or ['Work', 'Uncategorized']
WEEKLY_OR_DAILY = 'weekly' # alternate value: 'daily'
COLORS = ['#87CEEB','#32CD32','#BA55D3','#F08080','#4682B4','#9ACD32','#40E0D0','#FF69B4','#F0E68C','#D2B48C', 'black']

def main(input_schedule_csv, output_chart_name):
	def MinutesToHHMM(minutes):
		return str(minutes / 60) + ':' + ('0' if minutes % 60 < 10 else '') + str(minutes % 60)
	
	def HHMMToMinutes(hhmm):
		hhmmsplit = hhmm.split(':')
		if len(hhmmsplit) == 3:
			(hh, mm, ss) = tuple(hhmmsplit)
			assert(int(ss) == 0)
		else:
			(hh, mm) = tuple(hhmmsplit)
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
			if category in CATEGORIES:
				ActivityNames.add(activity)
		return list(ActivityNames)

	def generateChart(datas, dates, output_chart_name):
		names = sorted(datas.keys(), key=lambda name: sum(datas[name]), reverse=True)
		figure(figsize=(12,8))
		gca().spines['top'].set_visible(False)
		gca().spines['right'].set_visible(False)
		gca().xaxis.set_ticks_position('bottom')
		gca().yaxis.set_ticks_position('none')
		ylabel('Total Hours')
		grid(b=True, which='major', color='#C0C0C0', linestyle='-', alpha=0.9)
		minutes = [datas[ActivityName] for ActivityName in names]
		if WEEKLY_OR_DAILY == 'daily':
			xlabel('Days -->')
			ytickmarks = range(0, 7 * 24 * 60, 60)
			ylabels = range(len(ytickmarks))
			xtickmarks = range(int(dates[0]), int(dates[-1]) + 1)
			x = dates
		else:
			xlabel('Weeks -->')
			ytickmarks = range(0, 7 * 24 * 60, 60 * 10)
			ylabels = range(0, len(ytickmarks) * 10, 10)
			xtickmarks = range(0, len(dates))
			minutes = [[sum(t) for t in chunks(activityMinutes, 7)] for activityMinutes in minutes]
			x = range(len(minutes[0]))
		yticks(ytickmarks, ylabels)
		xticks(xtickmarks, [])
		# wish I could plot this horizontally, but couldn't figure out how to rotate the orientation
		polys = stackplot(x, *minutes, linewidth=0, colors=COLORS) # baseline='weighted_wiggle' is interesting
		legend([Rectangle((0, 0), 1, 1, fc=poly.get_facecolor()[0]) for poly in polys][::-1], names[::-1], bbox_to_anchor=(0, 0, 1, 1), bbox_transform=gcf().transFigure, loc=9, ncol=5)
		savefig(output_chart_name, bbox_inches='tight')

	d = {}
	for line in open(input_schedule_csv, 'rU'):
		(startDate, startTime, duration, activity, category, description) = line.split(',')
		startTime = HHMMToMinutes(startTime)
		duration = HHMMToMinutes(duration)
		year, month, day = [int(i) for i in startDate.split('-')]
		startDate = datetime.date(year, month, day)
		if category in CATEGORIES:
			process(startDate, startTime, duration, activity, d)
	
	dates = []
	datas = {}
	activityNames = getActivityNames(input_schedule_csv)
	for activityName in activityNames:
		datas[activityName] = []
	for date in sorted(d):
		dates.append(date2num(date))
		for activityName in activityNames:
			datas[activityName].append(0)
		dayTotal = 0
		for k in sorted(d[date], key=d[date].get, reverse=True):
			datas[k][-1] = d[date][k]
			dayTotal += d[date][k]
	
	generateChart(datas, dates, output_chart_name)
	
if __name__ == "__main__":
	if len(sys.argv) < 3:
		print 'Usage: ' + sys.argv[0] + ' input_schedule_csv output_chart_name'
	else:
		main(sys.argv[1], sys.argv[2])
