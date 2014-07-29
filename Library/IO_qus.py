import dropbox
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 20 21:32:43 2014

@author: jink
"""

def read_from_dropbox(input_path, input_dropbox_access_token):
	client = dropbox.client.DropboxClient(input_dropbox_access_token)
	folder_metadata = client.metadata(input_path)
	most_recent_file = sorted(folder_metadata['contents'], key=lambda f: f['path'])[-1]
	print "File read : " + most_recent_file['path']
	#file_upload_timestamp = most_recent_file['modified'].rsplit(':', 1)[0] # drop time zone (it's always UTC), seconds
	#file_upload_datetime = datetime.datetime.strptime(file_upload_timestamp, '%a, %d %b %Y %H:%M')
	#file_upload_localtime = file_upload_datetime.replace(tzinfo=tz.gettz('UTC')).astimezone(tz.tzlocal()).replace(tzinfo=None)
	return client.get_file(most_recent_file['path']).read()

def read_from_path(input_path):
    search_path = glob.glob(os.path.join(input_path,'TimesheetBackup*.xml'))
    most_recent_file = sorted(search_path )[-1]
    return open(most_recent_file).read()

