import datetime
import sys
import math
from pylab import *

# REMARKS
#
# input_location_csv fields: latitude, longitude, timestamp in '%Y-%m-%d %H:%M:%S'
#
# TODO: input_poi_csv should be a file listing points of interest (your home, office, etc.)
#       probably would be good to choose the closest POI if there are multiple within ACCEPTABLE_DISTANCE

# PARAMETERS
EARLIEST_POI = 'Home' # where you started on EARLIEST_DATETIME
EARLIEST_DATETIME = datetime.datetime(2013, 8, 1)
POINTS_OF_INTEREST = {'Home': (FILLIN_HOME_LATITUDE, FILLIN_HOME_LONGITUDE, '#4682B4'),
                      'Office': (FILLIN_OFFICE_LATITUDE, FILLIN_OFFICE_LONGITUDE, '#E0830A')}
DEFAULT_POI = ('Other', '#BA55D3')
ACCEPTABLE_DISTANCE = 100 # in meters. seems to work better than 150

def matchColor(currentLocation):
	if currentLocation in POINTS_OF_INTEREST:
		return POINTS_OF_INTEREST[currentLocation][2]
	elif currentLocation == DEFAULT_POI[0]:
		return DEFAULT_POI[1]

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
	for poi in POINTS_OF_INTEREST:
		if distance((latitude, longitude), (POINTS_OF_INTEREST[poi][0], POINTS_OF_INTEREST[poi][1])) < ACCEPTABLE_DISTANCE:
			return poi
	return DEFAULT_POI[0]

def main(input_location_csv, output_chart_name):
	data = [] # list of tuples in the form (locationName, duration in seconds, arrival time in datetime)
	currentLocation = EARLIEST_POI # where you were at 12am on EARLIEST_DATETIME
	arrivalTime = EARLIEST_DATETIME
	prevArrivalTime = EARLIEST_DATETIME
	for line in open(input_location_csv):
		(latitude, longitude, timestamp) = line.split(',')
		timestamp = datetime.datetime.strptime(timestamp.strip(), '%Y-%m-%d %H:%M:%S')
		longitude = float(longitude)
		latitude = float(latitude)
		locationName = getLocationName(latitude, longitude)
		# we assume you're there until you're not
		if locationName != currentLocation:
			data.append((currentLocation, int((timestamp - arrivalTime).total_seconds()), arrivalTime))
			arrivalTime = timestamp
			currentLocation = locationName
		prevArrivalTime = timestamp
	data.append((currentLocation, int((timestamp - arrivalTime).total_seconds()), arrivalTime)) # leftover
	
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
			colors.append(matchColor(currentLocation))
			
			duration = leftoverDuration
			arrivalTime = leftoverArrivalTime
			startTime = arrivalTime.time().second + arrivalTime.time().minute * 60 + arrivalTime.time().hour * 60 * 60

		# leftover
		days.append((arrivalTime - EARLIEST_DATETIME).days + 1)
		startTimes.append(startTime)
		durations.append(duration)
		colors.append(matchColor(currentLocation))

	daysPlusOne = max(days) + 1
	
	def dayFormatter(pos, day):
		return (EARLIEST_DATETIME + datetime.timedelta(daysPlusOne-day-1)).strftime("%b %d")

	days = [daysPlusOne - day for day in days]
	figure(figsize=(9, 1.5*daysPlusOne / 7)) # seems to be a reasonable approximation
	barplot = barh(days, durations, left=startTimes, color=colors, linewidth=0, height=1)
	ylim(1, daysPlusOne)
	xlim(0, 24)
	xlabel('Hour of Day')
	gca().xaxis.set_ticks_position('none')
	gca().yaxis.set_ticks_position('none')
	gca().yaxis.set_major_locator(MultipleLocator(1))
	gca().yaxis.set_minor_locator(FixedLocator([i+0.5 for i in range(daysPlusOne)]))
	gca().yaxis.set_minor_formatter(FuncFormatter(dayFormatter))
	gca().yaxis.set_major_formatter(NullFormatter())
	rectangles = [Rectangle((0, 0), 1, 1, fc=DEFAULT_POI[1])]
	labels = [DEFAULT_POI[0]]
	for poi in POINTS_OF_INTEREST:
		rectangles.append(Rectangle((0, 0), 1, 1, fc=POINTS_OF_INTEREST[poi][2]))
		labels.append(poi)
	legend(rectangles, labels, bbox_to_anchor=(0, 0, 1, 0.95), bbox_transform=gcf().transFigure, loc=9, ncol=5)
	grid(b=True, which='major', color='#C0C0C0', linestyle='-', alpha=0.9)
	xticksmarks = range(0, 24 * 60 * 60 + 1, 60 * 60) # the +1 is to show the last tick
	xlabels = range(len(xticksmarks) + 1) # the +1 is to show the last tick
	xticks(xticksmarks, xlabels)
	savefig(output_chart_name, bbox_inches='tight')

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print 'Usage: ' + sys.argv[0] + ' input_location_csv output_chart_name'
	else:
		main(sys.argv[1], sys.argv[2])
