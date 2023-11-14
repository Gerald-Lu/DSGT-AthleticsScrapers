import requests
import csv
import json
import pandas as pd
def NCAA_box_scraper(game_id, team_name):
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
  #Writes data to pandas dataframe
  def write_df(team_data):
      #Column headers
      headers = ['Name', 'Position', 'Minutes Played', 'Field Goals Made', 'Three Pointers Made', 'Free Throws Made', 'Total Rebounds', 'Offensive Rebounds', 'Assists', 'Personal Fouls', 'Steals', 'Turnovers', 'Blocked Shots', 'Points']
      count = 0
      row_data = []
      df = pd.DataFrame(columns=headers)
      #Iterates throw team_data and fills the pandas dataframe accordingly
      for rows in team_data[0:-1]:
          if count == 0:
              count+= 1
          row_data = [list(rows.values())[0] + ' ' + list(rows.values())[1]] + list(rows.values())[2:15]  
          df.loc[len(df)] = row_data
      #last index which contains data for total stats for the team
      totals = team_data[-1].values()
      row_data = ['Total', ' ', ' '] + list(totals)[0:-3]
      df.loc[len(df)] = row_data
      return df
  def chosen_team(name):
    box_data = fetch_data(f"https://data.ncaa.com/casablanca/game/{game_id}/boxscore.json")
    teams = box_data['meta']['teams']
    #box score data
    team1_data = box_data['teams'][0]['playerStats'] + [box_data['teams'][0]['playerTotals']]
    team2_data = box_data['teams'][1]['playerStats'] + [box_data['teams'][1]['playerTotals']]
    for team in teams:
      if team['shortName'].lower() == name.lower():
        if int(team['id']) == box_data['teams'][0]['teamId']:
          return team1_data
        elif int(team['id']) == box_data['teams'][1]['teamId']:
          return team2_data
        raise Exception("Name inputted incorrectly")
  return write_df(chosen_team(team_name))



