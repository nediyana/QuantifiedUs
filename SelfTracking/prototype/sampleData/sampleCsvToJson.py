import csv
import json

f = open( 'sampleGeoPoints.csv', 'r' )
reader = csv.DictReader( f, fieldnames = ( 'lat', 'lon', 'date' ))
out = json.dumps( [ row for row in reader ] )
print out