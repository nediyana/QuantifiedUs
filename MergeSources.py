from StringIO import StringIO
from os.path import *
from init_qus import *
from TimesheetToTsv import *
from EvernoteJournals import *
from HabbitToTsv import *
from Config import *

### Process Input Files

timesheet_to_csv(TIMESHEET_PATH, ujoin(OUTPUT_PATH, "Timesheet.tsv"))
tt = pd.read_csv(StringIO(read_dropbox(ujoin(OUTPUT_PATH, "Timesheet.tsv"))), sep='\t', parse_dates=['Date'])
tta = tt.groupby('Date', as_index = False).agg({'Duration':np.sum})
tta2 = tt[tt.Project == 'Work'].groupby('Date', as_index = False).agg({'Duration':np.sum})

habbits_to_tsv(HABBITS_PATH, ujoin(OUTPUT_PATH, "Habbits.tsv"))
th = pd.read_csv(StringIO(read_dropbox(ujoin(OUTPUT_PATH, "Habbits.tsv"))), sep='\t')

tm = pd.read_csv(StringIO(read_dropbox(ujoin(OUTPUT_PATH, "iMoodJournal.csv"))), sep=',')
fix_columns(tm)
tm['Date'] = tm.Date.apply(lambda e: datetime.strptime(e, '%B %d, %Y'))
tma = tm.groupby('Date', as_index = False).agg({'Level':np.mean})

#evernote_journal(EN_AUTH_TOKEN, EN_SEARCH_STR, join(OUTPUT_PATH, "journal.tsv"))
#tj = pd.read_csv(join(OUTPUT_PATH, "journal.tsv"), sep='\t')

### Merge Files

mt = pd.merge(tma, tta2, on=['Date'] )
tmpstr = StringIO()
mt.to_csv(tmpstr)
write_dropbox(ujoin(OUTPUT_PATH, "Merged.tsv"), tmpstr.getvalue())
#mt = pd.merge(mt, th, on=['Date'] )
#mt = pd.merge(mt, tma, on=['Date'] )
