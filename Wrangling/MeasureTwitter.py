from twitter_auth import *
#from init_qus import *
from IO_qus import *
import datetime

filename = r'/home/jink/dev/QuantifiedUs/tmp/MeasureTwitter.tsv'

tuser = ta.users.show(screen_name='lifidea')
tdata = [datetime.datetime.now(), tuser['friends_count'], tuser['followers_count'], tuser['statuses_count']]
print tdata
f = open(filename,'a')
f.write( "\t".join([str(e) for e in tdata])+'\n' )
ret = write_dropbox(ujoin(OUTPUT_PATH, "MeasureTwitter.tsv"), file.read(open(filename,'r')))
print "Written to dropbox, result:", ret
