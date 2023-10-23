import requests
import csv
import json
import pandas as pd

'''
Get data from pbp.json file and organize data
'''
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

#Play by play data combined from two periods
playByPlayData = data['periods'][0]['playStats'] + data['periods'][1]['playStats']


'''
Writing .csv file with data
'''
#writes a csv file where the data will be stored
teamA = data['meta']['teams'][0]['sixCharAbbr']
teamB = data['meta']['teams'][1]['sixCharAbbr']
date = data['updatedTimestamp']
dataOut = open(f'playByPlay{teamA}v{teamB}{date[:7]}.csv','w')

#initiates a csv writer
writer = csv.writer(dataOut)

#Appends headers and corresponding values to .csv file
playTypes = ['Personal Foul', 'Offensive foul', 'Technical Foul', 'Turnover', 'Jumper MISSED', 'Layup MISSED', '2 Pointer MISSED', 'Slam Dunk MISSED', 'Free Throw MISSED', 'Jumper', 'Free Throw', '2 Pointer', '3 Pointer', 'Layup', 'Slam Dunk', 'Foul', 'Subbing in', 'Subbing out', 'Defensive REBOUND', 'Offensive REBOUND', 'Assist', 'timeout', 'time out', 'steal']
rowData = ['', '', '', '', '', '', '']
count = 0
for period in playByPlayData:
  if count==0:
    header = ['Time Left', 'Score', 'Play Type', 'Player 1 Involved', 'Player 2 Involved', 'Player 3 involved', 'Play Result']
    writer.writerow(header)
    count+= 1
  tempRow = list(period.values())
  rowData[0] = tempRow[1]
  rowData[1] = tempRow[0]
  rowData[6] = tempRow[2] + " " + tempRow[3]
  for i in playTypes:
    if i in rowData[6]:
      rowData[2] = i
      break
  writer.writerow(rowData)
dataOut.close()
#print(play_by_play['periods'][0]['periodNumber'])








