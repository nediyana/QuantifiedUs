from os.path import *
from init_qus import *
from TimesheetToTsv import *
from EvernoteJournals import *
from HabbitToTsv import *

DROPBOX_TOKEN = r"bdOpEz-TVPwAAAAAAAAMC4Eaft6Ktst66KXuwcoroxNa1RaTvZNuU4B4WPqvEHZc"
OUTPUT_PATH = r"C:\Dropbox\Apps\QUS"
timesheet_to_csv(TIMESHEET_PATH, join(OUTPUT_PATH, "Timesheet.tsv") , DROPBOX_TOKEN)

#EN_AUTH_TOKEN = "S=s10:U=11824f:E=14b22279c62:C=143ca767064:P=1cd:A=en-devtoken:V=2:H=b416828af6f07c37938c46c427600dc8"
#EN_SEARCH_STR = "notebook:Current tag:journal created:20140701"
#evernote_journal(EN_AUTH_TOKEN, EN_SEARCH_STR, join(OUTPUT_PATH, "journal.tsv"))

HB_INPUT = r'C:\Dropbox\Apps\Habbits\backup\Habits.db'
export_habbits(HB_INPUT, join(OUTPUT_PATH, "Habbits.tsv"))


th = pd.read_csv(join(OUTPUT_PATH, "Habbits.tsv"), sep='\t')

tm = pd.read_csv(join(OUTPUT_PATH, "iMoodJournal.csv"), sep=',')
fix_columns(tm)
tm['Date'] = tm.Date.apply(lambda e: datetime.strptime(e, '%B %d, %Y'))
tma = tm.groupby('Date', as_index = False).agg({'Level':np.mean})

#tj = pd.read_csv(join(OUTPUT_PATH, "journal.tsv"), sep='\t')

tt = pd.read_csv(join(OUTPUT_PATH, "Timesheet.tsv"), sep='\t', parse_dates=['Date'])
tta = tt.groupby('Date', as_index = False).agg({'Duration':np.sum})
tta2 = tt[tt.Project == 'Work'].groupby('Date', as_index = False).agg({'Duration':np.sum})


mt = pd.merge(tma, tta2, on=['Date'] )

mt = pd.merge(mt, th, on=['Date'] )
mt = pd.merge(mt, tma, on=['Date'] )
