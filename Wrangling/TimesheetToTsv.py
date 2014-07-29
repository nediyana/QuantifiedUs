from IO_qus import *
from init_qus import *
import glob
import json
import datetime
import xml.etree.ElementTree as ET
from dateutil import tz

# REMARKS
#
# output_schedule_csv Fields: startDate, startTime, duration, projectName, category, description
# This script should be run on a computer where the local timezone is the same as the time zone recorded in Timesheet

# PARAMETERS
TIMESHEET_PATH = '/Apps/Timesheet/'

def parse_time(timestr):
    res = map(lambda(e): int(e), re.findall(r"\d\d?", timestr))
    #print timestr, res
    return res[0] * 60 + res[1]

def timesheet_to_csv(input_path, output_schedule_csv, input_dropbox_access_token = None):
	print input_path, output_schedule_csv
	# download the latest Timesheep backup file to TIMESHEET_XML
	if input_dropbox_access_token:
		TIMESHEET_XML = read_from_dropbox(input_path, input_dropbox_access_token)
	else:
		TIMESHEET_XML = read_from_path(input_path)
	
	# gets a list of the valid projects
	projects = {}
	root = ET.fromstring(TIMESHEET_XML)
	#root = tree.getroot()
	for project in root.find('projects'):
		projemployer = project.find('employer').text
		projid = project.find('projectId').text
		projname = project.find('name').text
		projects[projid] = (projname, projemployer)
	
	# convert TIMESHEET_XML to CSV and output to output_schedule_csv
	timesheetCsv = open(output_schedule_csv, 'w')
	timesheetCsv.write('\t'.join(["Date", "StartTime", "Duration", "Project", "Category", "Description"]) + '\n')
	for task in root.find('tasks'):
		projid = task.find('projectId').text
		if projid not in projects:
			continue
		projectName, category = projects[projid]
		startDatetime = task.find('startDate').text
		endDateNode = task.find('endDate')
		#endDatetime = file_upload_localtime
		if endDateNode is not None and endDateNode.text is not None:
			endDatetime = endDateNode.text
			endDatetime = datetime.datetime.strptime(endDatetime, '%Y-%m-%dT%H:%M:%S')
		description = task.find('description').text
		(startDate, startTime) = startDatetime.split('T')
		startDatetime = datetime.datetime.strptime(startDatetime, '%Y-%m-%dT%H:%M:%S')
		duration = str(endDatetime - startDatetime)
		if category is None:
			category = 'Uncategorized'
		if description is None:
			description = ''
		timesheetCsv.write('\t'.join([startDate, startTime, str(parse_time(duration)), projectName, category, description]) + '\n')
	timesheetCsv.close()
	return

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print 'Usage: ' + sys.argv[0] + ' input_path output_schedule_csv'
	else:
		timesheet_to_csv(sys.argv[1], sys.argv[2])
