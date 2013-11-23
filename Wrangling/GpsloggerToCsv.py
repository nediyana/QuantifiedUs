import sys
import os
import datetime
import xml.etree.ElementTree as ET
from dateutil import tz
import json
import zipfile
import dropbox

# REMARKS
# GPSLogger values always used
# Supplemented with Google Location values when within GOOGLE_LOCATION_RANGES
# Everything converted to local time, so ensure server is running on local time too
# - Daylight savings will cause problems [TODO]

# PARAMETERS
GPSLOGGER_ZIP_DROPBOX_PATH = '/Apps/GPSLogger for Android/gpslogger.zip'
GOOGLELOCATION_ZIP_DROPBOX_PATH = '/Apps/GoogleLocationHistory/LocationHistory.zip' # Set to None if not using. Assumed to be sorted by time already
GOOGLE_LOCATION_RANGES = [(datetime.datetime(2013, 8, 1), datetime.datetime(2013, 8, 10))]
ACCURACY_THRESHOLD = 200

# CONSTANTS
GPSLOGGER_FILENAME_ZIP = 'gpslogger.zip' # intermediate file
GOOGLELOCATION_FILENAME_ZIP = 'LocationHistory.zip' # intermediate file
GOOGLELOCATION_FILENAME_JSON = 'LocationHistory.json' # filename inside zip file
GPSLOGGER_FILENAME_GPX = 'gpslogger.gpx' # filename inside zip file

def main(dropbox_access_token, output_csv_filename):
	client = dropbox.client.DropboxClient(dropbox_access_token)
	
	geolocations = []
	if GOOGLELOCATION_ZIP_DROPBOX_PATH:
		googleZipFile = open(GOOGLELOCATION_FILENAME_ZIP, 'wb')
		googleZipFileContent = client.get_file(GOOGLELOCATION_ZIP_DROPBOX_PATH).read()
		googleZipFile.write(googleZipFileContent)
		googleZipFile.close()
		zfile = zipfile.ZipFile(GOOGLELOCATION_FILENAME_ZIP)
		googleLocationFile = zfile.open(GOOGLELOCATION_FILENAME_JSON)
		coords = json.load(googleLocationFile)['locations']
		for coord in coords:
			if coord['accuracy'] > ACCURACY_THRESHOLD:
				continue
			latitude = str(coord['latitudeE7'])[:-7] + '.' + str(coord['latitudeE7'])[-7:]
			longitude = str(coord['longitudeE7'])[:-7] + '.' + str(coord['longitudeE7'])[-7:]
			timestamp = datetime.datetime.fromtimestamp(float(coord['timestampMs']) / 1000) # converts to local timestamp
			geolocations.append((latitude, longitude, timestamp, 'google'))
		# Note that geolocations is in reverse time order at this point
		googleLocationFile.close()
		zfile.close()
		os.remove(GOOGLELOCATION_FILENAME_ZIP)
	
	gpxZipFile = open(GPSLOGGER_FILENAME_ZIP, 'wb')
	gpxZipFileContent = client.get_file(GPSLOGGER_ZIP_DROPBOX_PATH).read()
	gpxZipFile.write(gpxZipFileContent)
	gpxZipFile.close()
	zfile = zipfile.ZipFile(GPSLOGGER_FILENAME_ZIP)
	gpxFile = zfile.open(GPSLOGGER_FILENAME_GPX)
	gpxTree = ET.parse(gpxFile)
	for trkseg in gpxTree.getroot().getchildren()[2].getchildren():
		for trkpt in trkseg.getchildren():
			dateandtime = datetime.datetime.strptime(trkpt.find('{http://www.topografix.com/GPX/1/0}time').text, '%Y-%m-%dT%H:%M:%SZ')
			dateandtime = dateandtime.replace(tzinfo=tz.gettz('UTC')).astimezone(tz.tzlocal()).replace(tzinfo=None)
			geolocations.append((trkpt.attrib['lat'], trkpt.attrib['lon'], dateandtime, 'gpslogger'))
	gpxFile.close()
	zfile.close()
	os.remove(GPSLOGGER_FILENAME_ZIP)
	
	cleanedGeolocations = []
	for geolocation in geolocations:
		if geolocation[3] == 'google':
			for timeRange in GOOGLE_LOCATION_RANGES:
				if timeRange[0] < geolocation[2] < timeRange[1]:
					cleanedGeolocations.append(geolocation)
					break
		elif geolocation[3] == 'gpslogger':
			cleanedGeolocations.append(geolocation)
		else:
			assert(False) # geolocation[3] should have been 'google' or 'geolocation'
	
	sortedGeolocations = sorted(cleanedGeolocations, key=lambda geolocation: geolocation[2])
	
	mergedLocationFile = open(output_csv_filename, 'w')
	for geolocation in sortedGeolocations:
		mergedLocationFile.write(str(float(geolocation[0])) + ',' + str(float(geolocation[1])) + ',' + str(geolocation[2].replace(microsecond=0)) + '\n')
	mergedLocationFile.close()

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print 'Usage: ' + sys.argv[0] + ' dropbox_access_token output_location_csv'
	else:
		main(sys.argv[1], sys.argv[2])
