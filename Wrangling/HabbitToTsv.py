from Config import *
from os.path import *
from IO_qus import *
from init_qus import *
import sqlite3


def habbits_to_tsv(input_file, output_file):
	tf_name = join(TMP_PATH, "habbits.db")
	tf = open(tf_name, "wb"); tf.write(read_dropbox(input_file)); tf.close()
	con = sqlite3.connect(tf_name)
	c = con.cursor()
	
	c.execute("select H.Name, C.date, C.type AS String, C.note FROM Habits H, CHECKINS C WHERE H._id = C.Habit_id;");
     
	res = ""
	res += ("\t".join(["Habit", "Date", "Result", "Note"]) + "\n")
	for l in c.fetchall():
		#print l
		res += ("\t".join([str(e) for e in l]) + "\n")
	write_dropbox(output_file, res)
	return
