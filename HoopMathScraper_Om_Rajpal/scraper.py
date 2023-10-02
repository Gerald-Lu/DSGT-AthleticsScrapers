import requests
from bs4 import BeautifulSoup

# Define a function to fetch and parse data for a specific team
def fetch_data(team_url):
    response = requests.get(team_url)
    if response.status_code != 200:
        raise Exception("Failed to load page.")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    def parse_table(table):
        # Extract headers
        headers = [header.get_text(strip=True) for header in table.find_all('th')]
        #print(headers)
        
        # Extract row data
        rows = table.find_all('tr')[1:]  # skip the header row
        table_data = []
        for row in rows:
            cells = row.find_all('td')
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

# Fetch data for both teams
auburn_data = fetch_data("https://hoop-math.com/Auburn2023.php")
georgia_tech_data = fetch_data("https://hoop-math.com/GeorgiaTech2023.php")
print(georgia_tech_data)

# Printing the fetched data

for team, data in [("Auburn", auburn_data), ("Georgia Tech", georgia_tech_data)]:
    print(f"\n{team} Offensive Transition Splits:")
    print(data['offensive_transition']['headers'])
    for row in data['offensive_transition']['data']:
        print(row)

    print(f"\n{team} Defensive Transition Splits:")
    print(data['defensive_transition']['headers'])
    for row in data['defensive_transition']['data']:
        print(row)

print(georgia_tech_data['offensive_transition']['data'])
