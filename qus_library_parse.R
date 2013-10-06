### Various parser functions for each input type
parse.table <- function(filename, sep = "\t", ...)
{
	read.table(filename, encoding="UTF-8", sep = sep, comment.char = "", stringsAsFactors=F, header=T, strip.white=T, ...)
}

parse.kindle <- function(filename, sep = "\t", ...)
{
	out.filename = file.path(dirname(filename), "kindle.tsv")
	system(sprintf("ruby QuantifiedUs/kindle/kproc.rb \"%s\" %s", filename, out.filename))
	#browser()
	if(file.exists(out.filename))
		parse.table(out.filename, quote="")
	else
		data.frame()
}

export.evernote <- function(export.query, export.filename)
{
	run.cmd(sprintf("ENScript.exe exportNotes /q %s /f %s", export.query, export.filename))
}

parse.evernote <- function(filename, ...)
{
	out.filename = str_replace(filename, ".enex" ,".tsv")
	run.cmd(sprintf("ruby -I lib/rb QuantifiedUs/evernote/evernote_parse.rb \"%s\" %s", filename, out.filename))
	if(file.exists(out.filename))
		parse.table(out.filename, quote="")
	else
		data.frame()
}

parse.followmee <- function(filename, sep = "\t", ...)
{
	dt = parse.table(filename, sep=",")
	ha = c(47.66648,-122.3117)#geocode("5204 15th ave ne Seattle, WA")
	wa = c(47.61453,-122.194) #geocode("555 110th ave ne bellevue, wa") #c(wa[2], wa[1,1])
	dt2 = ddply(dt, c("Date"), function (t){
		t$DistHome = gps.distance(ha, unlist(t[1,2:3]))
		t$DistWork = gps.distance(wa, unlist(t[1,2:3]))
		t
	})
}

# loc1 = c(lat1, long1)
# loc2 = c(lat2, long2)
gps.distance <- function(loc1, loc2)
{
	degree_to_rad = pi / 180.0

	d_lat = (loc2[1] - loc1[1]) * degree_to_rad
	d_long = (loc2[2] - loc1[2]) * degree_to_rad
	#browser()
	a = (sin(d_lat / 2) ** 2) + cos(loc1[1] * degree_to_rad) * cos(loc2[1] * degree_to_rad) * (sin(d_long / 2) ** 2)
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	km = 6367 * c
	#mi = 3956 * c
	km
}
