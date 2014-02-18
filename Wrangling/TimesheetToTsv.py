import sys
import datetime
import os
import glob
from dateutil import tz
import json
import dropbox
import xml.etree.ElementTree as ET

# REMARKS
#
# output_schedule_csv Fields: startDate, startTime, duration, projectName, category, description
# This script should be run on a computer where the local timezone is the same as the time zone recorded in Timesheet

# PARAMETERS
TIMESHEET_PATH = '/Apps/Timesheet/'

# CONSTANTS
TIMESHEET_XML = 'timesheet.xml' # intermediate temp file

def read_from_dropbox(input_dropbox_access_token, input_path):
	client = dropbox.client.DropboxClient(input_dropbox_access_token)
	folder_metadata = client.metadata(TIMESHEET_PATH)
	most_recent_file = sorted(folder_metadata['contents'], key=lambda f: f['path'])[-1]
	file_upload_timestamp = most_recent_file['modified'].rsplit(':', 1)[0] # drop time zone (it's always UTC), seconds
	file_upload_datetime = datetime.datetime.strptime(file_upload_timestamp, '%a, %d %b %Y %H:%M')
	file_upload_localtime = file_upload_datetime.replace(tzinfo=tz.gettz('UTC')).astimezone(tz.tzlocal()).replace(tzinfo=None)
	return client.get_file(most_recent_file['path']).read()

def read_from_path(input_path):
    search_path = glob.glob(os.path.join(input_path,'TimesheetBackup*.xml'))
    most_recent_file = sorted(search_path )[-1]
    return open(most_recent_file).read()

def timesheet_to_csv(input_path, output_schedule_csv):
	# download the latest Timesheep backup file to TIMESHEET_XML
	with open(TIMESHEET_XML, 'w') as timesheet:
		fp = read_from_path(input_path)
		timesheet.write(fp)
	
	# gets a list of the valid projects
	projects = {}
	tree = ET.parse(TIMESHEET_XML)
	root = tree.getroot()
	for project in root.find('projects'):
		projemployer = project.find('employer').text
		projid = project.find('projectId').text
		projname = project.find('name').text
		projects[projid] = (projname, projemployer)
	
	# convert TIMESHEET_XML to CSV and output to output_schedule_csv
	timesheetCsv = open(output_schedule_csv, 'w')
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
		timesheetCsv.write('\t'.join([startDate, startTime, duration, projectName, category, description]) + '\n')
	timesheetCsv.close()
	
	os.remove(TIMESHEET_XML)

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print 'Usage: ' + sys.argv[0] + ' input_path output_schedule_csv'
	else:
		timesheet_to_csv(sys.argv[1], sys.argv[2])
