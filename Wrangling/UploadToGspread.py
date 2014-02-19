from init_qus import *
import gspread
import string
import pdb

AP = argparse.ArgumentParser(description='Upload TSV into Google Drive')
AP.add_argument("input_file")
AP.add_argument("gdrive_id")
AP.add_argument("gdrive_pw")
AP.add_argument("gdrive_file")
AP.add_argument("gdrive_sheet")

def number_to_col(num):
    res = ""
    while num >= 24:
        res = res + string.uppercase[num % 24]
        num = int(num / 24)
    res = res + string.uppercase[num]
    return res
number_to_col(25)

def upload_to_gspread(input_file, gdrive_id, gdrive_pw, gdrive_file, gdrive_sheet):
	input_data = pd.read_csv(input_file, sep="\t")
	input_list = [list(x) for x in input_data.itertuples()]

	# Login with your Google account
	gs = gspread.login(gdrive_id, gdrive_pw).open(gdrive_file)

	#pdb.set_trace()
	# Open a worksheet from spreadsheet with one shot
	try:
		gs.del_worksheet(gs.worksheet(gdrive_sheet))
	except:
		print("No sheet found...")

	wks = gs.add_worksheet(title=gdrive_sheet, rows=len(input_data), cols=len(input_data.columns))

	# Fetch a cell range
	range_str = 'A1:' + string.uppercase[len(input_data.columns)-1]+str(len(input_data))
	print(range_str)
	cell_list = wks.range(range_str)
	for cell in cell_list:
	    cell.value = input_list[cell.row-1][cell.col]
	wks.update_cells(cell_list)

if __name__ == '__main__':
	AG = AP.parse_args()
	upload_to_gspread(AG.input_file, AG.gdrive_id, AG.gdrive_pw, AG.gdrive_file, AG.gdrive_sheet)
