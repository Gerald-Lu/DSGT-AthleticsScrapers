# DSGT Athletics Web Scrapers

## About
This tool allows users to gather sports data from [NCAA](https://www.ncaa.com/) and [HOOP-MATH](https://hoop-math.com/) efficiently. The available scrapers can scrape NCAA box scores, play by plays, game ids, and also HOOP-MATH defensive and offensive transition splits. All data is returned as a pandas dataframe. Specific instructions for each scraper are provided below. 

#### Notes

For some play by play sets, the terminology used may be different so the "Play Type" field may not populate for some plays (sometimes the data will say "time-out", "timeout", or "time out", which the scraper might not register). 
If that is the case, please contact me so I can check the specific terminology related to that game at glu49@gatech.edu

Furthermore, some of the box scores and play by plays are incomplete on the NCAA website, so please be aware of that as a potential source of error. 

## To use HoopMath_scraper: 
Find the specific name and year of the team in the URL. For example: https://hoop-math.com/GeorgiaTech2023.php

GeorgiaTech2023 is the specific name and year of the team.

Please input the name and year of the team as a string as a parameter for the function.

Example: `HoopMath_scraper('GeorgiaTech2023')`

## To use NCAA_pbp_scraper:

Find the specific code for the game in the URL. For example:
https://www.ncaa.com/game/6049153/play-by-play

6049153 would be the specific code.

Please input the code as a parameter for the function.

Example: `NCAA_pbp_scraper(6049153)`

## To use NCAA_box_scraper:

Find the specific code for the game in the URL. For example:
https://www.ncaa.com/game/6049153/play-by-play

6049153 would be the specific code.

Determine which team you want the box score from.

Please input the code and team name (as a string) as parameters for the function.

Example: `NCAA_box_scraper(6049153, 'Georgia Tech')`

## To use NCAA_game_id_scraper:

Find the specific date for the game in the URL. For example:
https://www.ncaa.com/scoreboard/basketball-men/d1/2022/11/10/all-conf

2022/11/10 would be the specific date.

Please input the date as a string as a parameter for the function.

Example: `NCAA_game_id_scraper('2022/11/10')`


