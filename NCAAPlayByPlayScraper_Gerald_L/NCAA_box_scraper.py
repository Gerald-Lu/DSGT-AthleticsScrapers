import requests
import csv
import json
import pandas as pd

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

game = input("Please input game code (can be found in url of specific game; read README.md for example): ")
box_data = fetch_data(f"https://data.ncaa.com/casablanca/game/{game}/boxscore.json")


teamA = box_data['meta']['teams'][0]['sixCharAbbr']
teamB = box_data['meta']['teams'][1]['sixCharAbbr']
date = box_data['updatedTimestamp']

#box score data
team1_data = box_data['teams'][0]['playerStats']
team2_data = box_data['teams'][1]['playerStats']

headers = ['Name', 'Position', 'Minutes Played', 'Field Goals Made', 'Three Pointers Made', 'Free Throws Made', 'Total Rebounds', 'Offensive Rebounds', 'Assists', 'Personal Fouls', 'Steals', 'Turnovers', 'Blocked Shots', 'Points']
count = 0
def write_csv(team_data, team_name):
    data_out = open(f'box_score_{team_name}.csv','w')
    writer = csv.writer(data_out)
    count = 0
    for rows in team_data:
        if count == 0:
            writer.writerow(headers)
            count+= 1
        row_data = [list(rows.values())[0] + ' ' + list(rows.values())[1] ] + list(rows.values())[2:len(list(rows.values()))]
        writer.writerow(row_data)
    data_out.close()

if box_data['teams'][0]['teamId'] == box_data['meta']['teams'][0]['id']:
    write_csv(team1_data, teamA)
    write_csv(team2_data, teamB)
else:
    write_csv(team1_data, teamB)
    write_csv(team2_data, teamA)

print('\nCheck folder for .csv file\n')
    


