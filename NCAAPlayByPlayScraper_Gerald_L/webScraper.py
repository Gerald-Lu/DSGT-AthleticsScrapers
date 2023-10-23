import requests
import csv
import json
import pandas as pd

'''
Get data from pbp.json file and organize data
'''
def fetch_data(input_url):
  #json file url with play by play contents
  #For another game, replace the numbers after game/ with the specific numbers in the game you are trying to scrape
  url = input_url

  #GETs the json file by simulating the request
  payload = {}
  headers = {
    'Cookie': 'akacd_ems=1695693092~rv=26~id=28e986e49e28e11009c7adfe5b3da9da'
  }

  #Sends cookie to server with HTTP headers (which includes the generated cookie) so we can get access
  response = requests.request("GET", url, headers=headers, data=payload)


  #json data stored in 'data' variable, where we can access data in the json file as a dictionary
  return response.json()

#Play by play data combined from two periods
pbp_data = fetch_data("https://data.ncaa.com/casablanca/game/6049153/pbp.json")
play_data = pbp_data['periods'][0]['playStats'] + pbp_data['periods'][1]['playStats']

#Boxscore data
box_data = fetch_data("https://data.ncaa.com/casablanca/game/6049153/boxscore.json")
#boxs

'''
Writing .csv file with data
'''
#writes a csv file where the data will be stored
teamA = pbp_data['meta']['teams'][0]['sixCharAbbr']
teamB = pbp_data['meta']['teams'][1]['sixCharAbbr']
date = pbp_data['updatedTimestamp']
data_out = open(f'playByPlay{teamA}v{teamB}{date[:7]}.csv','w')

#initiates a csv writer
writer = csv.writer(data_out)

#Appends headers and corresponding values to .csv file
play_types = ['Personal Foul', 'Offensive foul', 'Technical Foul', 'Turnover', 'Jumper MISSED', 'Layup MISSED', '2 Pointer MISSED', 'Slam Dunk MISSED', 'Free Throw MISSED', 'Jumper', 'Free Throw', '2 Pointer', '3 Pointer', 'Layup', 'Slam Dunk', 'Foul', 'Subbing in', 'Subbing out', 'Defensive REBOUND', 'Offensive REBOUND', 'Assist', 'timeout', 'time out', 'steal']
row_data = ['', '', '', '', '', '', '']
count = 0
for period in play_data:
  if count==0:
    header = ['Time Left', 'Score', 'Play Type', 'Player 1 Involved', 'Player 2 Involved', 'Player 3 involved', 'Play Result']
    writer.writerow(header)
    count+= 1
  tempRow = list(period.values())
  row_data[0] = tempRow[1]
  row_data[1] = tempRow[0]
  row_data[6] = tempRow[2] + " " + tempRow[3]
  for i in play_types:
    if i in row_data[6]:
      row_data[2] = i
      break
  writer.writerow(row_data)
data_out.close()
#print(play_by_play['periods'][0]['periodNumber'])








