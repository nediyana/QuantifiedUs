check.and.install.packages <- function(list.of.packages)
{
	new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
	if(length(new.packages)) install.packages(new.packages, repos="http://cran.us.r-project.org")
}

import.file <- function(filename){
	data2text(readLines(filename), sep="\n")
}

# Serialize R array into human-friendly text
data2text <- function(data, sep = " ", quote=NA)
{
	if(is.null(data) ||is.na(data))
		text = ""
	if(!is.na(quote))
		text = paste(quote, data[1], quote, sep="")
	else
		text = data[1]
	if(length(data) == 1)
		return(text)
	for(i in 2:length(data))
	{
		if(!is.na(quote))
			text = paste(text, paste(quote, data[i], quote, sep=""), sep=sep)
		else
			text = paste(text, data[i], sep=sep)
	}
	text
}

printf <- function(...)
{
	print(sprintf(...))
}


export.table <- function(tbl, file, ...)
{
	write.table(tbl, file=file, sep='\t', row.names=F, quote=F, ...)
}
