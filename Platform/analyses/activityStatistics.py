import json
import sys
from pprint import pprint

f = sys.argv[1]

json_data=open(f)

data = json.load(json_data)
json_data.close()

# pprint(data)

def convertValues(vals):
  # durations = [d['y'] for d in vals]
  duration = vals['y']
  tkns = duration.split(':')
  # convert HH:MM:SS string to seconds integer
  time = int(tkns[0]) * 3600 + int(tkns[1]) * 60 + int(tkns[2])
  return time
def simplifyCategories(c):
  vals = [convertValues(v) for v in c['values']]
  vals.sort()
  name = c['name']

  # time = duration time in seconds
  totalTime = sum(vals)
  medTime = vals[len(vals)/2]
  avgTime = sum(vals)/len(vals)
  results = {'avgDuration':avgTime, 'medianDuration':medTime, 'name':name, 'totalDuration':totalTime, 'values':c['values']}

  return results

newData = [simplifyCategories(c) for c in data]
print json.dumps(newData)
#pprint(newData)