from bs4 import BeautifulSoup
import requests
import csv
import json
import pandas as pd

#GETs the json file by simulating the request
url = "https://data.ncaa.com/casablanca/game/6136947/pbp.json"

payload = {}
headers = {
  'Cookie': 'akacd_ems=1695693092~rv=26~id=28e986e49e28e11009c7adfe5b3da9da'
}

response = requests.request("GET", url, headers=headers, data=payload)

#json data stored in 'data' variable, where we can access data in the json file as a dictionary
data = response.json()

playByPlayData = data['periods'][0]['playStats']

#writes a csv file where the data will be stored
dataOut = open('playByPlayTest.csv','w')

#initiates a csv writer
writer = csv.writer(dataOut)

#Appends headers and corresponding values to .csv file
count = 0
for period in playByPlayData:
    if count==0:
        header = period.keys()
        print(header)
        writer.writerow(header)
        count+= 1
    writer.writerow(period.values())
dataOut.close()
#print(play_by_play['periods'][0]['periodNumber'])








