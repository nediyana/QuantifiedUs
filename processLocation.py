import datetime
import sys
import math
from pylab import *

HOME = TODO
OFFICE = TODO
EARLIEST_DATETIME = TODO
#EARLIEST_DATETIME = datetime.datetime(2013, 8, 1)
ACCEPTABLE_DISTANCE = 100 # seems to work better than 150
HOME_COLOR = '#4682B4'
OFFICE_COLOR = '#E0830A'
OTHER_COLOR = '#BA55D3'

# these numbers are in seconds
Stats = {
		'WeekdayOffice': 0,
		'WeekdayHome': 0,
		'WeekdayOther': 0,
		'WeekendOffice': 0,
		'WeekendHome': 0,
		'WeekendOther': 0,
	}

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 * 1000 # meters
 
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
 
    return d

def getLocationName(latitude, longitude):
	if distance((latitude, longitude), HOME) < ACCEPTABLE_DISTANCE:
		return 'Home'
	elif distance((latitude, longitude), OFFICE) < ACCEPTABLE_DISTANCE:
		return 'Office'
	else:
		return 'Other'

def main(filepath):
	data = [] # list of tuples in the form (locationName, duration in seconds, arrival time in datetime)
	currentLocation = 'Home' # just because on 2013-08-01 12am I was at home
	arrivalTime = EARLIEST_DATETIME
	prevArrivalTime = EARLIEST_DATETIME
	for line in open(filepath):
		(latitude, longitude, timestamp) = line.split(',')
		timestamp = datetime.datetime.strptime(timestamp.strip(), '%Y-%m-%d %H:%M:%S')
		longitude = float(longitude)
		latitude = float(latitude)
		locationName = getLocationName(latitude, longitude)
		# we assume you're there until you're not
		if locationName != currentLocation: # uncommenting this optimizes things, but we can't identify gaps			
			if (timestamp - prevArrivalTime).total_seconds() > 60 * 10: # split the different if we don't know what happened in between
				data.append((currentLocation, int((prevArrivalTime - arrivalTime).total_seconds() + (timestamp - prevArrivalTime).total_seconds() / 2), arrivalTime))
				data.append((locationName, int((timestamp - prevArrivalTime).total_seconds() / 2), prevArrivalTime + (timestamp - prevArrivalTime) / 2))
			else:
				data.append((currentLocation, int((timestamp - arrivalTime).total_seconds()), arrivalTime))
			arrivalTime = timestamp
			currentLocation = locationName
		prevArrivalTime = timestamp
	# last one (we don't do the split thing but not that important)
	data.append((currentLocation, int((timestamp - arrivalTime).total_seconds()), arrivalTime))
	
	days = []
	durations = []
	startTimes = []
	colors = []
	for currentLocation, duration, arrivalTime in data:
		startTime = arrivalTime.time().second + arrivalTime.time().minute * 60 + arrivalTime.time().hour * 60 * 60
		while startTime + duration > 60 * 60 * 24:
			leftoverDuration = startTime + duration - 60 * 60 * 24
			leftoverArrivalTime = datetime.datetime.combine((arrivalTime.date() + datetime.timedelta(1)), datetime.time()) # add 1 day and cut off time portion of the datetime
			duration = 60 * 60 * 24 - startTime

			# identical code as below
			days.append((arrivalTime - EARLIEST_DATETIME).days + 1)
			startTimes.append(startTime)
			durations.append(duration)
			if currentLocation == 'Home':
				if arrivalTime.weekday() >= 5:
					Stats['WeekendHome'] += duration
				else:
					Stats['WeekdayHome'] += duration
				colors.append(HOME_COLOR)
			elif currentLocation == 'Office':
				if arrivalTime.weekday() >= 5:
					Stats['WeekendOffice'] += duration
				else:
					Stats['WeekdayOffice'] += duration
				colors.append(OFFICE_COLOR)
			else:
				if arrivalTime.weekday() >= 5:
					Stats['WeekendOther'] += duration
				else:
					Stats['WeekdayOther'] += duration
				colors.append(OTHER_COLOR)
			
			duration = leftoverDuration
			arrivalTime = leftoverArrivalTime
			startTime = arrivalTime.time().second + arrivalTime.time().minute * 60 + arrivalTime.time().hour * 60 * 60
			
		days.append((arrivalTime - EARLIEST_DATETIME).days + 1)
		startTimes.append(startTime)
		durations.append(duration)
		if currentLocation == 'Home':
			if arrivalTime.weekday() >= 5:
				Stats['WeekendHome'] += duration
			else:
				Stats['WeekdayHome'] += duration
			colors.append(HOME_COLOR)
		elif currentLocation == 'Office':
			if arrivalTime.weekday() >= 5:
				Stats['WeekendOffice'] += duration
			else:
				Stats['WeekdayOffice'] += duration
			colors.append(OFFICE_COLOR)
		else:
			if arrivalTime.weekday() >= 5:
				Stats['WeekendOther'] += duration
			else:
				Stats['WeekdayOther'] += duration
			colors.append(OTHER_COLOR)

	figure(figsize=(12,8))
	clf()
	barplot = bar(days, durations, bottom=startTimes, color=colors, linewidth=0, width=1)
	gca().xaxis.set_ticks_position('none')
	gca().yaxis.set_ticks_position('none')
	xlabel('Days -->')
	gca().xaxis.set_major_locator(MultipleLocator(1))
	gca().xaxis.set_minor_formatter(FixedFormatter(range(1, max(days)+1)))
	gca().xaxis.set_major_formatter(NullFormatter())
	xlim(1, max(days)+1)
	ylim(0, 24)
	ylabel('Hour of Day')
	legend([barplot[0], barplot[1], barplot[2]], ['Home', 'Other', 'Office'], bbox_to_anchor=(0, 0, 1, 1), bbox_transform=gcf().transFigure, loc=9, ncol=5)
	grid(b=True, which='major', color='#C0C0C0', linestyle='-', alpha=0.9)
	yticksmarks = range(0, 24 * 60 * 60 + 1, 60 * 60) # the +1 is to show the last tick
	ylabels = range(len(yticksmarks) + 1) # the +1 is to show the last tick
	yticks(yticksmarks, ylabels)
	savefig('location.daily.png', bbox_inches='tight')

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print 'Need input file (csv) as argument.'
	else:
		main(sys.argv[1])
