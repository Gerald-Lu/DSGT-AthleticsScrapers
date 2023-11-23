import requests
from bs4 import BeautifulSoup
import pandas as pd

def HoopMath_scraper(team_name):
    def fetch_data(url):
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Failed to load page.")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        def parse_table(table):
            headers = [header.get_text(strip=True) for header in table.find_all('th')]
            body = table.find('tbody')
            table_data = []

            cells = body.find_all('td')
            row_data = [cell.get_text(strip=True) for cell in cells]
            table_data.append(row_data)
            
            return {"headers": headers, "data": table_data}

        # Extract the offensive and defensive transition splits tables
        offensive_table = soup.find('table', {'id': 'TransOTable1'})
        defensive_table = soup.find('table', {'id': 'TransDTable1'})
        offensive_data = parse_table(offensive_table) if offensive_table else None
        defensive_data = parse_table(defensive_table) if defensive_table else None

        data = {
            'offensive_transition': offensive_data,
            'defensive_transition': defensive_data
        }
        
        return data
    def write_df(name):
        team_data = fetch_data(f"https://hoop-math.com/{name}.php")
        df_offense = pd.DataFrame(columns = team_data['offensive_transition']['headers'])
        df_defense = pd.DataFrame(columns = team_data['defensive_transition']['headers'])
        for data1, data2 in zip(team_data['offensive_transition']['data'], team_data['defensive_transition']['data']):
            count = 0
            for rows in range(0, int((len(data1)/9))):
                df_offense.loc[len(df_offense)] = data1[count:count + 9]
                df_defense.loc[len(df_defense)] = data2[count:count + 9]
                count += 9
        return df_offense, df_defense
    return write_df(team_name)