import json
from pprint import pprint

data = []

with open('keywords') as data_file:    
    data = json.load(data_file)

popularities = []
sentiments = []

for key in data:
	sentiments.append(data[key][0])
	popularities.append(data[key][1])

sentiments.sort()
popularities.sort()

print popularities[-10:-9]

print sentiments[4:6]
print sentiments[-6:-4]
