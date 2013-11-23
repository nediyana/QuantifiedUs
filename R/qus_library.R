source(paste(SRC_PATH, "QuantifiedUs/qus_library_parse.R",sep="/"))
source(paste(SRC_PATH, "QuantifiedUs/qus_library_etc.R",sep="/"))
check.and.install.packages(c("yaml", "ggmap", "plyr", "stringr"))
library(yaml)
library(plyr)
library(ggmap)
library(stringr)

import.data <- function(path, o = list())
{
	printf("Processing %s", path)
	files = file.path(path, sort(dir(path, o$Filename), dec=T))
	if(length(files) == 0)
		return(data.frame())
	# Parse fildes into table
	dt = adply(files, 1, function(f){
		printf("  reading file %s", f)
		if(o$Filetype == "evernote")
			parse.evernote(f)
		else if(o$Filetype == "kindle")
			parse.kindle(f)
		else if(o$Filetype == "followmee")
			parse.followmee(f)
		else if(o$Filetype == "csv")
			parse.table(f, sep=",")
		else
			parse.table(f, sep="\t")
	})
	# Apply transformation
	printf("  %d records read", nrow(dt))
	if(!is.null(o$PrimaryKeys)){
		dt = dt[!duplicated(dt[,o$PrimaryKeys]),]
		printf("  %d records left", nrow(dt))
	}
	# Process date column
	if(!is.null(o$DateCol))
	{
		DateColName = "Date"
		if(!is.null(o$DateCol$Name))
			DateColName = o$DateCol$Name
		dt$Date = as.Date(as.character(dt[[DateColName]]), o$DateCol$Format)
		if(!is.null(o$DateCol$Offset))
			dt$Date = dt$Date + as.numeric(o$DateCol$Offset)
	}
	# Process row/column filtering
	if(!is.null(o$IncludeRows))
	{
		for(key in names(o$IncludeRows)){
			dt = dt[dt[[key]] %in% o$IncludeRows[[key]], ]
		}
	}
	if(!is.null(o$ExcludeRows))
	{
		for(key in names(o$ExcludeRows)){
			dt = dt[!(dt[[key]] %in% o$ExcludeRows[[key]]), ]
		}
	}
	if(!is.null(o$IncludeCols))
		dt = dt[,o$IncludeCols]
	dt
}

agg.data <- function(tbl, key, m = list())
{
	ddply(tbl, key, function(t){
		#printf("key: %s / count: %d", format(t$Date[1], "%Y-W%W"), nrow(t))
		res = list()
		for(mkey in names(m)){
			res[[mkey]] = eval(parse(text=m[[mkey]]))
		}
		as.data.frame(res)
	})
}

run.cmd <- function(cmd, debug = T)
{
	if(debug)
		printf("[run.cmd] %s",cmd)
	system(cmd)
}

export.data <- function(tbl, output_loc, filename, o = list())
{
	filepath = file.path(output_loc, paste(filename, ".tsv", sep=""))
	printf("  %d records written to %s", nrow(tbl), filepath)
	export.table(tbl, filepath)
}

yaml.loadfile <- function(filename)
{
	if(file.exists(filename)){
		res = yaml.load(import.file(filename))
		format(res)
		res
	}
	else
		list()
}

# Extract tag value & apply a function
extract.tag <- function(data, tag.name, fun = NULL)
{
	result = c()
	for(kv in strsplit(data, ":")) {
		if(length(kv) == 0)
			next
		if(tag.name == (kv[1])){
			if(length(kv) > 1 & str_detect(kv[2], "[0-9.]+"))
				value = as.numeric(kv[2])
			else
				value = 1
			result = c(result, value)
		}
	}
	if(length(result) > 0){
		if( is.null(fun) ){
			data2text(result)			
		}
		else
			do.call(fun, list(result))
	}
	else
		NA
}

tag.vals <- function(col, tag.name, fun = NULL)
{
	sapply( strsplit(col, split="[, ]+"), extract.tag, tag.name, fun)
}

extract.workflowy <- function(content)
{
	#browser()
	pattern = ".*\\((\\d+) completed, (\\d+) created, .*"
	list(completed = as.numeric(gsub(pattern,"\\1", content, perl=T)), created=as.numeric(gsub(pattern,"\\2", content, perl=T)))
}
