import matplotlib.pyplot as plt
from StringIO import StringIO
from os.path import *
from init_qus import *
from TimesheetToTsv import *
from EvernoteJournals import *
from HabbitToTsv import *
from Config import *

### Process Input Files ###

## Timesheet
timesheet_to_csv(TIMESHEET_PATH, ujoin(OUTPUT_PATH, "Timesheet.tsv"))
tt = pd.read_csv(StringIO(read_dropbox(ujoin(OUTPUT_PATH, "Timesheet.tsv"))), sep='\t', parse_dates=['Date'])
tta = tt.groupby(['Project','Date'], as_index = False).agg({'Duration':np.sum})
ttar = tta.pivot(index='Date', columns='Project', values='Duration')
ttar['Date'] = ttar.index
#tta2 = tt[tt.Project == 'Work'].groupby('Date', as_index = False).agg({'Duration':np.sum})

## Habbits
habbits_to_tsv(HABBITS_PATH, ujoin(OUTPUT_PATH, "Habbits.tsv"))
th = pd.read_csv(StringIO(read_dropbox(ujoin(OUTPUT_PATH, "Habbits.tsv"))), sep='\t', parse_dates=['Date'])
thr = th.pivot(index='Date', columns='Habit', values='Result')

## iMoodJournal
tm = pd.read_csv(StringIO(read_dropbox(ujoin(OUTPUT_PATH, "iMoodJournal.csv"))), sep=',')
fix_columns(tm)
tm['Date'] = tm.Date.apply(lambda e: datetime.strptime(e, '%B %d, %Y'))
tm['Mood'] = tm['Level'] - 3
tma = tm.groupby('Date', as_index = False).agg({'Mood':np.mean})

## Evernote
#evernote_journal(EN_AUTH_TOKEN, EN_SEARCH_STR, join(OUTPUT_PATH, "journal.tsv"))
#tj = pd.read_csv(join(OUTPUT_PATH, "journal.tsv"), sep='\t')

## SleepAsAndroid
sleep_str = filter_str(read_dropbox(ujoin(SLEEP_CLOUD_PATH, "Sleep as Android Data")), r"^\"\d",0,15)
colnames = ['Id','Tz','From','To','Sched','Hours','Rating','Comment','Framerate','Snore','Noise','Cycles','DeepSleep','LenAdjust','Geo']
ts = pd.read_csv(StringIO(sleep_str), sep=',', header=None, names=colnames, parse_dates=['Sched'])
fix_columns(ts)
ts['Date'] = ts.Sched.apply(lambda e: e.replace(hour=0, minute=0, second=0))
ts['Time'] = ts.Sched.apply(lambda e: e.time())
ts2 = ts[['Hours','Snore','Rating','Date','Time']]

## Twitter
import datetime
tw = pd.read_csv(StringIO(read_dropbox(ujoin(OUTPUT_PATH, "MeasureTwitter.tsv"))), sep='\t', parse_dates=["Date"])
tw['Date'] = tw.Date.apply(lambda e: e.replace(hour=0, minute=0, second=0, microsecond=0))
tw2 = tw.copy()
tw2['Date'] = tw2.Date - datetime.timedelta(days=1)
twm = pd.merge(tw, tw2, on=['Date'] )
twm['Fol_diff'] = twm.Followers_y - twm.Followers_x
twm['Fri_diff'] = twm.Friends_y - twm.Friends_x
twm['Sta_diff'] = twm.Statuses_y - twm.Statuses_x

### Merge Files ###

mt = pd.merge(ttar, thr, how='left', left_on=['Date'], right_index=True )
mt = pd.merge(mt, tma, how='left', on=['Date'])
#mt = pd.merge(mt, ts2, how='left', on=['Date'] )
mt = pd.merge(mt, twm[['Date','Fol_diff','Fri_diff','Sta_diff']], how='left', on=['Date'] )


tmpstr = StringIO()
mt.to_csv(tmpstr)
mt.to_csv(ujoin(TMP_PATH, "Merged.tsv"))
write_dropbox(ujoin(OUTPUT_PATH, "Merged.tsv"), tmpstr.getvalue())
#mt = pd.merge(mt, th, on=['Date'] )
#mt = pd.merge(mt, tma, on=['Date'] )
