import sys
import hashlib
import binascii
#import html2text
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

#en_auth_token = "S=s10:U=11824f:E=14b22279c62:C=143ca767064:P=1cd:A=en-devtoken:V=2:H=b416828af6f07c37938c46c427600dc8"
# python EvernoteJournals.py "S=s10:U=11824f:E=14b22279c62:C=143ca767064:P=1cd:A=en-devtoken:V=2:H=b416828af6f07c37938c46c427600dc8" "notebook:Current tag:journal created:20140101" test.csv

def main(en_auth_token, en_search_str, output_csv):
    client = EvernoteClient(token=en_auth_token, sandbox=False)

    userStore = client.get_user_store()

    version_ok = userStore.checkVersion(
        "Evernote EDAMTest (Python)",
        UserStoreConstants.EDAM_VERSION_MAJOR,
        UserStoreConstants.EDAM_VERSION_MINOR
    )
    print "Is my Evernote API version up to date? ", str(version_ok)
    print ""
    if not version_ok:
        exit(1)

    ## Read Notes
    noteStore = client.get_note_store()
    filter = NoteStore.NoteFilter()
    filter.words = en_search_str
    spec = NoteStore.NotesMetadataResultSpec()
    spec.includeTitle = True
    note_list = noteStore.findNotesMetadata(en_auth_token, filter, 0, 10, spec)

    ## Get note contents
    of = open(output_csv, "w")
    for note in note_list.notes:
        wholeNote = noteStore.getNoteContent(en_auth_token, note.guid)
        print note.title
        of.write("%s,%d\n" % (note.title, len(wholeNote)))
        file = open("temp\\"+note.title+".txt", 'w')
        try:
            file.write(html2text.html2text(wholeNote))
        except:
            file.write(strip_tags(wholeNote))
        #wholeNotes.append(wholeNote)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print 'Usage: ' + sys.argv[0] + 'en_auth_token en_search_str output_csv'
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
