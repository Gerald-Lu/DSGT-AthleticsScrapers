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

play_by_play = response.json()

periods = play_by_play['periods']

play = play_by_play['playStats']

#output.to_csv('playByPlayTest.csv', index = False)






