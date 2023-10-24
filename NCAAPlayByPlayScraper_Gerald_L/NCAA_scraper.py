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

#Prompts user for the game
game = input("Please input game code (can be found in url of specific game; read README.md for example): ")

#Play by play data combined from periods
pbp_data = fetch_data(f"https://data.ncaa.com/casablanca/game/{game}/pbp.json")
p1_data = pbp_data['periods'][0]['playStats']
p2_data = pbp_data['periods'][1]['playStats']
OT_data = []
if len(pbp_data['periods']) >= 3:
  for i in range(2, len(pbp_data['periods'])):
    OT_data += pbp_data['periods'][i]['playStats']
play_data = p1_data + p2_data + OT_data

#Boxscore data
box_data = fetch_data(f"https://data.ncaa.com/casablanca/game/{game}/boxscore.json")
team1_data = box_data['teams'][0]['playerStats']
team2_data = box_data['teams'][1]['playerStats']
boxscore_data = team1_data + team2_data


#First and last names of players
first_names1 = [''] * len(team1_data)
last_names1 = [''] * len(team1_data)
first_names2 = [''] * len(team2_data)
last_names2 = [''] * len(team2_data)

index = 0
for players in team1_data:
  first_names1[index] = list(players.values())[0]
  last_names1[index] = list(players.values())[1]
  index += 1
index = 0
for players in team2_data:
  first_names2[index] = list(players.values())[0]
  last_names2[index] = list(players.values())[1]
  index += 1


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
play_types = ['Personal Foul', 'Offensive foul', 'Technical Foul', 'Turnover', 'Jumper MISSED', 'Layup MISSED', '2 Pointer MISSED', '3 Pointer MISSED', 'Slam Dunk MISSED', 'Free Throw MISSED', 'Jumper', 'Free Throw', '2 Pointer', '3 Pointer', 'Layup', 'Slam Dunk', 'Foul', 'Subbing in', 'Subbing out', 'Defensive REBOUND', 'Offensive REBOUND', 'Assist', 'timeout', 'time out', 'steal', 'block', 'turnover', 'foul', 'Steal', 'Block', 'REBOUND', 'TIMEOUT']
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
  '''
  Iterates through player names to see if it matches play by play output so we can determine what players were involved
  '''
  index = 0
  for j in boxscore_data:
    if (j['firstName'] + ' ' + j['lastName']).lower() in row_data[6].lower() or (j['lastName'] + ', ' + j['firstName']).lower() in row_data[6].lower():    
      row_data[3 + index] = j['firstName'] + ' ' + j['lastName']
      index += 1
    if (index > 2):
      break
  for i in play_types:
    if i in row_data[6]:
      row_data[2] = i
      break
  for element in range(3, 6):
    if row_data[element] == '':
      row_data[element] = 'N/A'
  writer.writerow(row_data)
  for a in range(len(row_data)):
    row_data[a] = ''
data_out.close()

print('\nCheck folder for .csv file\n')








