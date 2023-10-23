import requests
import csv
import json
import pandas as pd

#json file url with play by play contents
#For another game, replace the numbers after game/ with the specific numbers in the game you are trying to scrape
url = "https://data.ncaa.com/casablanca/game/6049153/pbp.json"

#GETs the json file by simulating the request
payload = {}
headers = {
  'Cookie': 'akacd_ems=1695693092~rv=26~id=28e986e49e28e11009c7adfe5b3da9da'
}

#Sends cookie to server with HTTP headers (which includes the generated cookie) so we can get access
response = requests.request("GET", url, headers=headers, data=payload)


#json data stored in 'data' variable, where we can access data in the json file as a dictionary
data = response.json()

playByPlayData = data['periods'][0]['playStats'] + data['periods'][1]['playStats']

#writes a csv file where the data will be stored
teamA = data['meta']['teams'][0]['sixCharAbbr']
teamB = data['meta']['teams'][1]['sixCharAbbr']
date = data['updatedTimestamp']

dataOut = open(f'playByPlay{teamA}v{teamB}{date[:7]}.csv','w')

#initiates a csv writer
writer = csv.writer(dataOut)

#Appends headers and corresponding values to .csv file
'''
count = 0
for period in playByPlayData:
    if count==0:
        header = period.keys()
        print(header)
        writer.writerow(header)
        count+= 1
    writer.writerow(period.values())
dataOut.close()
'''
print(playByPlayData)
playTypes = ['Personal Foul', 'Turnover', '']
count = 0
for period in playByPlayData:
  if count==0:
    header = ['Time Left', 'Score', 'Play Type', 'Player 1 Involved', 'Player 2 Involved', 'Player 3 involved', 'Play Result']
    writer.writerow(header)
dataOut.close()
#print(play_by_play['periods'][0]['periodNumber'])








