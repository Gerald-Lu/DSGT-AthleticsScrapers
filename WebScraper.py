from bs4 import BeautifulSoup
import requests
import csv
import json
import pandas as pd

url = "https://data.ncaa.com/casablanca/game/6136947/pbp.json"

payload = {}
headers = {
  'Cookie': 'akacd_ems=1695693092~rv=26~id=28e986e49e28e11009c7adfe5b3da9da'
}

response = requests.request("GET", url, headers=headers, data=payload)

data = response.json()

playByPlayData = data['periods'][0]['playStats']


dataOut = open('playByPlayTest.csv','w')

writer = csv.writer(dataOut)

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








