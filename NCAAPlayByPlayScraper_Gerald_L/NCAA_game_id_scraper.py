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
date = input("Please input the date you want game ids from (format: 2022/11/09)--refer to the README file if unclear: ")
game_id_data = fetch_data(f'https://data.ncaa.com/casablanca/scoreboard/basketball-men/d1/{date}/scoreboard.json')


formatted_date = date.replace('/', '-', 2)
print(formatted_date)
game_ids = game_id_data['games']

data_out = open(f'game_id_{formatted_date}.csv','w', newline='')
writer = csv.writer(data_out)

count = 0

for games in game_ids:
    if count == 0:
        header = ['Game ID', 'Teams']
        writer.writerow(header)
        count+= 1
    contents = [games['game']['url'][6:len(games['game']['url'])], games['game']['title']]
    writer.writerow(contents)
data_out.close()
                