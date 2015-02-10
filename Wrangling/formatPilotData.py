import csv
import os
import sys
from dateutil import parser
from datetime import datetime

##################################################################
# FORMAT PILOT DATA
#
# Takes CSV (*downloaded from Google spreadsheets!!!*) and 
# converts horizontal format into vertial format needed to 
# make graphs (see graphPilotData.py).
#
# Input: CSV from SleepAsAndroid, located in "./pilotData/[file]"
# Output: CSV in vertical format for graphing, located at
#			"./newPilotData/[input file name].csv"
# 
# To run:
# python formatPilotData.py [input file]
#
# Doc updated: 2/9/15
#
##################################################################

def getTimestamp(dt):
	return str('%d' % ((dt - datetime.datetime(1970, 1, 1)).total_seconds()*1000))

def main():
	csv_file = open(sys.argv[1])
	csv_reader = csv.reader(csv_file)

	csv_outfile = open("pilotData/new"+sys.argv[1], "w+")
	csv_writer = csv.writer(csv_outfile)
	csv_writer.writerow(["id","from", "to","time","accel"])

	nextLineWithTimes = next(csv_reader, None)
	nextLineWithData = next(csv_reader, None)
	while nextLineWithTimes != None: #until all nights are finished
		
		userid = nextLineWithData[0]
		timezone = nextLineWithData[1]
		fromTime = nextLineWithData[2]
		fromDatetime = parser.parse(fromTime)
		fromDate = ( fromDatetime ).date()
		toTime = nextLineWithData[3]
		toDatetime = parser.parse(toTime)
		toDate = ( toDatetime ).date()
		# sched = nextLineWithData[4]
		# hoursSlept = nextLineWithData[5]
		# sleepQuality = nextLineWithData[6]
		# comment = nextLineWithData[7]
		# framerate = nextLineWithData[8]
		# snoring = nextLineWithData[9]
		# noise = nextLineWithData[10]
		# cycles = nextLineWithData[11]
		# deepSleep = nextLineWithData[12]
		# lenAdjust = nextLineWithData[13]
		# geolocation = nextLineWithData[14]

		date = fromDate
		for i in range(15, len(nextLineWithTimes)):
			if not nextLineWithTimes[i][0].isdigit(): #stop before all the bullshit in that row
				break
			currTime = nextLineWithTimes[i]
			currDatetime = parser.parse(currTime)

			if i > 15: #don't do this with the first one where there is no previous time 
				prevTime = nextLineWithTimes[i-1]
				prevDatetime = parser.parse(prevTime)
				
				if currTime < prevTime: #if we just made a jump
					date = toDate #update so that time is always the toDate
				
			accel = nextLineWithData[i]
			csv_writer.writerow([userid, fromDatetime, toDatetime, datetime.combine(date, currDatetime.time()), accel])

		next(csv_reader, None) #skip line with noise stuff
		nextLineWithTimes = next(csv_reader, None)
		nextLineWithData = next(csv_reader, None)

	csv_outfile.close()

if __name__ == '__main__':
	if len(sys.argv) < 2:
			sys.stderr.write('Please provide the name of the infile as a command line argument.\n')
			sys.exit(1)
	else:
		main()