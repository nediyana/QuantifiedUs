import sys
import math

DISTANCE_THRESHOLD = 10 # meters of distance changed until we consider it a movement

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

def main(input_location_csv):
	prevLocation = None
	prevLine = None
	reducedLines = []
	for line in open(input_location_csv):
		line = line.strip()
		(latitude, longitude, timestamp) = line.split(',')
		longitude = float(longitude)
		latitude = float(latitude)
		if prevLocation is None or distance(prevLocation, (latitude, longitude)) > DISTANCE_THRESHOLD:
			if prevLine is not None and reducedLines[-1] != prevLine:
				reducedLines.append(prevLine)
			reducedLines.append(line)
			prevLocation = (latitude, longitude)
			prevLine = line
	for line in reducedLines:
		print line

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print 'Usage: ' + sys.argv[0] + ' input_location_csv'
	else:
		main(sys.argv[1])
