import requests
import csv
import json
import pandas as pd
def NCAA_game_id_scraper(date):
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
  def write_df(game_date):
    game_id_data = fetch_data(f'https://data.ncaa.com/casablanca/scoreboard/basketball-men/d1/{game_date}/scoreboard.json')
    headers = ['Game ID', 'Teams']
    df = pd.DataFrame(columns=headers)

    game_ids = game_id_data['games']
    
    count = 0

    for games in game_ids:
      contents = [games['game']['url'][6:len(games['game']['url'])], games['game']['title']]
      df.loc[len(df)] = contents
    return df
  return write_df(date)
print(NCAA_game_id_scraper('2022/11/10'))
    

