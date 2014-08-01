import glob
import dropbox
from Config import *

# -*- coding: utf-8 -*-
"""
Created on Sun Jul 20 21:32:43 2014

@author: jink
"""

def read_dropbox(filename, dropbox_access_token = DROPBOX_TOKEN):
	client = dropbox.client.DropboxClient(dropbox_access_token)
	return client.get_file(filename).read()

def write_dropbox(filename, content, dropbox_access_token = DROPBOX_TOKEN):
	client = dropbox.client.DropboxClient(dropbox_access_token)
	return client.put_file(filename, content, overwrite=True)

def read_recent_from_dropbox(db_path, dropbox_access_token = DROPBOX_TOKEN):
	client = dropbox.client.DropboxClient(dropbox_access_token)
	folder_metadata = client.metadata(db_path)
	most_recent_file = sorted(folder_metadata['contents'], key=lambda f: f['path'])[-1]
	print "File read : " + most_recent_file['path']
	return client.get_file(most_recent_file['path']).read()

def read_recent_from_path(db_path):
    search_path = glob.glob(os.path.join(db_path,'TimesheetBackup*.xml'))
    most_recent_file = sorted(search_path )[-1]
    return open(most_recent_file).read()

