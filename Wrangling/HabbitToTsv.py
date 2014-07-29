from init_qus import *
import sqlite3


def export_habbits(input_file, output_file):
	con = sqlite3.connect(input_file)
	c = con.cursor()
	
	c.execute("select H.Name, C.date, C.type AS String, C.note FROM Habits H, CHECKINS C WHERE H._id = C.Habit_id;");
     
	f = open(output_file, "w")
	f.write("\t".join(["Habit", "Date", "Result", "Note"]) + "\n")
	for l in c.fetchall():
		#print l
		f.write("\t".join([str(e) for e in l]) + "\n")
	return
