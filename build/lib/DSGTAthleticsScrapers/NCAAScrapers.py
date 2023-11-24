import requests
import pandas as pd
def NCAA_game_id_scraper(date):
  def fetch_data(input_url):
    url = input_url

    #GETs the json file by simulating the request
    payload = {}
    headers = {
      'Cookie': 'akacd_ems=1695693092~rv=26~id=28e986e49e28e11009c7adfe5b3da9da'
    }

    #Sends cookie to server with HTTP headers (which includes the generated cookie) so we can get access
    response = requests.request("GET", url, headers=headers, data=payload)


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

def NCAA_box_scraper(game_id, team_name):
  def fetch_data(input_url):
    url = input_url

    #GETs the json file by simulating the request
    payload = {}
    headers = {
      'Cookie': 'akacd_ems=1695693092~rv=26~id=28e986e49e28e11009c7adfe5b3da9da'
    }

    #Sends cookie to server with HTTP headers (which includes the generated cookie) so we can get access
    response = requests.request("GET", url, headers=headers, data=payload)


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
  return write_df(chosen_team(team_name))

def NCAA_pbp_scraper(game_id):
  def fetch_data(input_url):
    url = input_url

    #GETs the json file by simulating the request
    payload = {}
    headers = {
      'Cookie': 'akacd_ems=1695693092~rv=26~id=28e986e49e28e11009c7adfe5b3da9da'
    }

    #Sends cookie to server with HTTP headers (which includes the generated cookie) so we can get access
    response = requests.request("GET", url, headers=headers, data=payload)


    return response.json()

  def get_pbp_data(id):
    #Play by play data combined from periods
    pbp_data = fetch_data(f"https://data.ncaa.com/casablanca/game/{id}/pbp.json")
    p1_data = pbp_data['periods'][0]['playStats']
    p2_data = pbp_data['periods'][1]['playStats']
    #Adds overtime data if it exists
    OT_data = []
    if len(pbp_data['periods']) >= 3:
      for i in range(2, len(pbp_data['periods'])):
        OT_data += pbp_data['periods'][i]['playStats']
    play_data = p1_data + p2_data + OT_data
    return play_data
  def get_box_data(id):
    box_data = fetch_data(f"https://data.ncaa.com/casablanca/game/{id}/boxscore.json")
    team1_data = box_data['teams'][0]['playerStats']
    team2_data = box_data['teams'][1]['playerStats']
    boxscore_data = team1_data + team2_data
    return boxscore_data
  def write_df(team_data, boxscore_data):
    play_types = ['Personal Foul', 'Offensive foul', 'Technical Foul', 'Turnover', 'Jumper MISSED', 'Layup MISSED', '2 Pointer MISSED', '3 Pointer MISSED', 'Slam Dunk MISSED', 'Free Throw MISSED', 'Jumper', 'Free Throw', '2 Pointer', '3 Pointer', 'Layup', 'Slam Dunk', 'Foul', 'Subbing in', 'Subbing out', 'Defensive REBOUND', 'Offensive REBOUND', 'Assist', 'timeout', 'time out', 'steal', 'block', 'turnover', 'foul', 'Steal', 'Block', 'REBOUND', 'TIMEOUT']
    row_data = ['', '', '', '', '', '', '']
    count = 0
    for period in team_data:
      if count==0:
        header = ['Time Left', 'Score', 'Play Type', 'Player 1 Involved', 'Player 2 Involved', 'Player 3 involved', 'Play Result']
        df = pd.DataFrame(columns = header)
        count+= 1
      tempRow = list(period.values())
      row_data[0] = tempRow[1]
      row_data[1] = tempRow[0]
      row_data[6] = tempRow[2] + " " + tempRow[3]
      index = 0
      for j in boxscore_data:
        if (j['firstName'] + ' ' + j['lastName']).lower() in row_data[6].lower() or (j['lastName'] + ', ' + j['firstName']).lower() in row_data[6].lower():    
          row_data[3 + index] = j['firstName'] + ' ' + j['lastName']
          index += 1
        if (index > 2):
          break
      for i in play_types:
        if i in row_data[6]:
          row_data[2] = i.upper()
          break
      for element in range(3, 6):
        if row_data[element] == '':
          row_data[element] = 'N/A'
      df.loc[len(df)] = row_data
      for a in range(len(row_data)):
        row_data[a] = ''
    return df
  return write_df(get_pbp_data(game_id), get_box_data(game_id))