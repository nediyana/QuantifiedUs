import csv
import json

# Start date YY-MM-DD, start time HH:MM:SS, duration HH:MM:SS, category
f = open( 'activities.csv', 'r' )
reader = csv.DictReader(f, fieldnames = ('startDate', 'startTime', 'duration', 'category'))
rawData = [row for row in reader]

# Group data by category
outData = {}
for d in rawData:
  name = d['category']
  valueStr = [d['startDate'], d['duration']] # x, y values
  if name in outData:
    outData[name]['values'].append(value)
  else:
    outData[name] = {'values':[value]}

outArray = []
for k, v in outData.iteritems():
  outArray.append({'name': k, 'values':v['values']})
print json.dumps([d for d in outArray])