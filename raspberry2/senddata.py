import requests
import random

import readus1
import readus2
import readdht 
import rfa    

url = 'http://139.59.17.224:80/users/logQuantumMainTankData/'

d1 = readus1.distance()
d2 = readus2.distance()
humidity, temperature = readdht.dht11()
ph, turbidity = rfa.getVal()

logQuantumMainTankData = {
    "mobile_no": 7351651000,
    "mainTank_level": d1,
    "quantumTank_level": d2,
    "temperature": temperature,
    "humidity": humidity,
    "turbidity": turbidity,
	"ph": ph,
}

print logQuantumMainTankData

try:
        res = requests.post(url, data=logQuantumMainTankData)
        print "success"
except:
        print "failed"
