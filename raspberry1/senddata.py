import requests
import random

import readus1
import readus2
import readus3
import readus4

url = 'http://139.59.17.224:80/users/logCategoryTanksData/'

d1 = readus1.distance()
d2 = readus2.distance()
d3 = readus3.distance()
d4 = readus4.distance()

logCategoryTanksData = {

	"mobile_no": 7351651000,
	"drinkingWater_level": d1,
	"carWater_level": d2,
	"bathingWater_level": d3,
	"plantWater_level": d4,
}

print logCategoryTanksData
try:
	res = requests.post(url, data=logCategoryTanksData)
	print "success"
except:
	print "failed"

