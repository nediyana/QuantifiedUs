from init_qus import *
import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
from evernote.api.client import NoteStore
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return '\n'.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def clean_content(html):
    html = html.replace("<en-todo checked=\"false\"/>", "[task:0]").replace("<en-todo checked=\"true\"/>", "[task:1]")
    html = strip_tags(html)
    html = re.sub("\n\s+\n","\n", html)
    return html

def clean_title(title):
    return re.sub("\W", "_",title)

def extract_tags(text):
    tags1 = re.findall(r"\[([\w\:\,\_]+)\]",text)
    tags2 = re.findall(r"\#([\w\:\,\_]+)", text)
    tags1.extend(tags2) 
    tags = [t for t in tags1 if not re.match(r'[\d\.]+', t)]
    #print(tags)
    return "|".join(tags)
 
def parse_tags(text):
    res = {}
    for tag in text.split("|"):
        if ':' in tag:
            k, v = tag.split(":")
        else:
            k = tag ; v = 1
        if res.has_key(k):
            res[k].append(v)
        else:
            res[k] = [v]
    return res

def read_evernote(en_auth_token, en_search_str, export_path = None):
    client = EvernoteClient(token=en_auth_token, sandbox=False)

    userStore = client.get_user_store()

    version_ok = userStore.checkVersion(
        "Evernote EDAMTest (Python)",
        UserStoreConstants.EDAM_VERSION_MAJOR,
        UserStoreConstants.EDAM_VERSION_MINOR
    )
    #print "Is my Evernote API version up to date? ", str(version_ok)
    if not version_ok:
        exit(1)

    ## Read Notes
    noteStore = client.get_note_store()
    filter = NoteStore.NoteFilter()
    filter.words = en_search_str
    spec = NoteStore.NotesMetadataResultSpec()
    spec.includeTitle = True
    note_list = noteStore.findNotesMetadata(en_auth_token, filter, 0, 100, spec)
    
    ## Get note contents
    res = []
    for note in note_list.notes:
        note_html = noteStore.getNoteContent(en_auth_token, note.guid)
        note_title = clean_title(note.title)
        note_text = clean_content(note_html)
        note_tags = extract_tags(note_text)
        print note_title
        res.append({"title":note.title, "text":note_text, "tags":note_tags, "tags2":parse_tags(note_tags)})
        if(export_path):
            of = open(os.path.join(export_path, note_title+".txt"), 'w')
            of.write(note_text)
    return res

def parse_datestr(dateval):
    try:
        return datetime.strptime(re.search(r'^\d{8}',str(dateval)).group(), "%Y%m%d").date()
    except:
        return

def evernote_journal(en_auth_token, en_search_str, output_csv):
    notes = read_evernote(en_auth_token, en_search_str) #, dirname(output_csv)
    ndf = pd.DataFrame(notes)
    ndf['Date'] = ndf.title.apply( parse_datestr )
    #print(format(ndf))
    ndf[["Date","title","tags","tags2"]].to_csv(output_csv, sep="\t", index=False)

#en_auth_token = "S=s10:U=11824f:E=14b22279c62:C=143ca767064:P=1cd:A=en-devtoken:V=2:H=b416828af6f07c37938c46c427600dc8"
# python EvernoteJournals.py "S=s10:U=11824f:E=14b22279c62:C=143ca767064:P=1cd:A=en-devtoken:V=2:H=b416828af6f07c37938c46c427600dc8" "notebook:Current tag:journal created:20140101" test.csv
debug = False#True
if __name__ == "__main__":
    if debug:
        en_auth_token = "S=s10:U=11824f:E=14b22279c62:C=143ca767064:P=1cd:A=en-devtoken:V=2:H=b416828af6f07c37938c46c427600dc8"
        search_str = "notebook:Current tag:journal created:20140215"
        output_file = r"c:\Src\root\sandbox\qus_evernote\journal.tsv"
        en_notes = evernote_journal(en_auth_token, search_str, output_file)
    elif len(sys.argv) < 3:
        print 'Usage: ' + sys.argv[0] + 'en_auth_token en_search_str output_csv'
    else:
        evernote_journal(sys.argv[1], sys.argv[2], sys.argv[3])
