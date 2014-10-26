import re
import os
import glob
import dropbox
from Config import *

# -*- coding: utf-8 -*-
"""
Created on Sun Jul 20 21:32:43 2014

@author: jink
"""

def ujoin(path1, path2):
	return path1 + "/" + path2

def read_dropbox(filename, dropbox_access_token = DROPBOX_TOKEN):
	client = dropbox.client.DropboxClient(dropbox_access_token)
	contents = client.get_file(filename).read()
	ofile = open(ujoin(TMP_PATH, os.path.basename(filename)),'w')
	ofile.write(contents)
	return contents

def write_dropbox(filename, content, dropbox_access_token = DROPBOX_TOKEN):
	client = dropbox.client.DropboxClient(dropbox_access_token)
	return client.put_file(filename, content, overwrite=True)

def read_recent_from_dropbox(db_path, dropbox_access_token = DROPBOX_TOKEN):
	client = dropbox.client.DropboxClient(dropbox_access_token)
	folder_metadata = client.metadata(db_path)
	most_recent_file = sorted(folder_metadata['contents'], key=lambda f: f['path'])[-1]
	#print "File read : " + most_recent_file['path']
	return client.get_file(most_recent_file['path']).read()

def read_recent_from_path(db_path):
	search_path = glob.glob(os.path.join(db_path,'TimesheetBackup*.xml'))
	most_recent_file = sorted(search_path )[-1]
	return open(most_recent_file).read()

def filter_str(argstr, row_ptn, col_start, col_end, col_sep=","):
	res = []
	for line in argstr.split("\n"):
		if re.search(row_ptn, line) is not None:
			res.append(col_sep.join(line.split(col_sep)[col_start:col_end]))
	return "\n".join(res)
