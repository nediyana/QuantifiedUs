SRC_PATH = "."
TEST_PATH = file.path(SRC_PATH, "QuantifiedUs/test")
PROD_PATH = "c:/Dropbox/Data/qus/raw"
source(file.path(SRC_PATH, "QuantifiedUs/qus_library.R"))

dl = ad = aw = am = list()

INPUT_PATH = TEST_PATH
#INPUT_PATH = PROD_PATH # Switch to prod mode
OUT_PATH = paste(INPUT_PATH,"out", sep="_")
if( !file.exists(OUT_PATH) ) dir.create(OUT_PATH)

cfg = yaml.loadfile(file.path(INPUT_PATH,"config_qus.yml"))
for(src in names(cfg))
{
	print(src)
	#if( src != "workflowy") next
	if( cfg[[src]]$Filetype == 'evernote' & INPUT_PATH == PROD_PATH )
		export.evernote(cfg[[src]]$ExportQuery, file.path(INPUT_PATH, src, cfg[[src]]$Filename))
	dl[[src]] = import.data(file.path(INPUT_PATH, src), cfg[[src]])
	export.data(dl[[src]], OUT_PATH, src)

	if(!is.null(cfg[[src]]$Metrics)){
		ad[[src]] = agg.data(dl[[src]], c("Date") , cfg[[src]]$Metrics)
		export.data(ad[[src]], OUT_PATH , sprintf("%s_daily",src))
		#src = "journal"
		aw[[src]] = agg.data(dl[[src]], .(Week=format(Date, "%Y-W%W")) , cfg[[src]]$Metrics)
		export.data(aw[[src]], OUT_PATH, sprintf("%s_weekly",src))
		am[[src]] = agg.data(dl[[src]], .(Month=format(Date, "%Y-%m")) , cfg[[src]]$Metrics)
		export.data(am[[src]], OUT_PATH, sprintf("%s_monthly",src))
	}
}


merge.tables <- function(tbl, col_name)
{
	res = tbl$journal
	for(i in 1:length(tbl)){
		if(names(tbl)[i] == "journal")
			next
		print(colnames(res))
		res = merge(res, tbl[[i]], all.x=T, by=c(col_name), suffixes=c("",toupper(substr(names(tbl)[i],1,1))))
	}
	res
}

td = merge.tables(ad, "Date")
#tw = merge.tables(aw, "Week")
aw$journal
am$journal

