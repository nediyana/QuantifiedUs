import csv

def csv_make(fields):
	return ','.join([str(i) for i in fields])

def main():
	csv_file = open("moveEventsByDay3.csv")
	csv_reader = csv.reader(csv_file) #read the tweets
	next(csv_reader, None) # skip the header in the csv file

	print csv_make(["userid", "averageFallAsleepHour", "averageSleepQuality", "minutesSlept"])

	next_line = next(csv_reader, None) #get one actor's tweets
	fallAsleepTime = {} #maps user ID to (sum of sleep times, number of days)
	sleepQuality = {}
	minutesSlept = {}

	while next_line != None: #go through all actor tweets
		userid = next_line[0]
		#####
		if userid not in fallAsleepTime:
			fallAsleepTime[userid] = (int(next_line[4]), 1)
		else:
			if int(next_line[4]) > 12:
				converted = int(next_line[4]) - 24 #put into negative
			else:
				converted = int(next_line[4])
			fallAsleepTime[userid] = ( fallAsleepTime[userid][0] + converted, int(fallAsleepTime[userid][1]) + 1)
		#####
		if userid not in sleepQuality:
			sleepQuality[userid] = (int(next_line[8]), 1)
		else:
			sleepQuality[userid] = (sleepQuality[userid][0] + int(next_line[8]), sleepQuality[userid][1] + 1)
		#####
		if userid not in minutesSlept:
			minutesSlept[userid] = (int(next_line[3]), 1)
		else:
			minutesSlept[userid] = (minutesSlept[userid][0] + int(next_line[3]), minutesSlept[userid][1] + 1)
		#####
		next_line = next(csv_reader, None)
	csv_file.close()

	averageQuality = {1:(0,0), 2:(0,0), 3:(0,0), 4:(0,0), 5:(0,0)}

	for userid in fallAsleepTime:
		time = int(fallAsleepTime[userid][0]/fallAsleepTime[userid][1])
		if time < 0:
			time += 24
		sleepQual = int(sleepQuality[userid][0]/sleepQuality[userid][1])
		minSlept = int(minutesSlept[userid][0]/minutesSlept[userid][1])

		averageQuality[sleepQual] = (averageQuality[sleepQual][0] + minSlept, averageQuality[sleepQual][1] + 1 )

	for qual in averageQuality:
		if averageQuality[qual][1] is not 0:
			print csv_make([qual, int(averageQuality[qual][0]/averageQuality[qual][1])])

		# print csv_make([userid, time, sleepQual, minSlept])



if __name__ == '__main__':
	main()
