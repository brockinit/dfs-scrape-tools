import os
import time
from robobrowser import RoboBrowser

default_years = [
    {'2012': 4},
    {'2013': 3},
    {'2014': 2},
    {'2015': 1},
    {'2016': 0}
]
default_weeks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

# Full season or week by week stats
scope = 1
# Scoring type (Fanduel default)
fs = 2
# Top level directory name
directory = './def_points_vs'

headers = 'rank,id,player,week,team,opp,games,qbpts,rbpts,wrpts,tepts,kpts,fanptsgame,seas'
sn = w = ew = None


def scraper():
    browser = RoboBrowser(parser='lxml')

    # Make the top-level directory for the CSV data
    os.mkdir(directory)

    # Open the previously hidden page
    for yearIdx, year in enumerate(default_years):
        year_dict = default_years[yearIdx]
        year_key = list(year_dict.keys())[0]
        sn = year_dict[year_key]

        # Make the directory for each year of CSV Data
        file_path = '{}/{}.csv'.format(directory, year_key)
        create_year_file = os.open(file_path, os.O_CREAT)
        os.close(create_year_file)

        for week in default_weeks:
            w = week
            ew = week
            pts_vs_url = 'https://fantasydata.com/nfl-stats/nfl-fantasy-football-points-allowed-defense-by-position.aspx?fs={}&stype=0&sn={}&scope={}&w={}&ew={}&s=&t=0&p=0&st=FantasyPointsAllowedAverage&d=1&ls=FantasyPointsAllowedAverage&live=false&pid=true&minsnaps=4'.format(
                fs,
                sn,
                scope,
                w,
                ew
            )

            # Delay before retrieving next set of data
            time.sleep(2)

            browser.open(pts_vs_url)
            content = browser.find_all('tr')

            # Initialize the data to be written to the file
            formatted_data = ''

            for idx, line in enumerate(content):
                # Only add the header once per year
                if idx == 0 and week == 0:
                    formatted_data = headers + '\n'
                elif idx != 0:
                    parsed_data = ','.join(line.find_all(text=True))
                    stripped_line = parsed_data.strip('\n').strip(',')
                    year_value = str(list(year.keys())[0])
                    next_line = stripped_line + ',' + year_value + '\n'

                    formatted_data = formatted_data + next_line

            try:
                # Write to the current year file
                print(file_path, ':', week)
                write_file = open(file_path, 'a')
                write_file.write(formatted_data)
                write_file.close()

            except RuntimeError as err:
                print('Failed to write to file: ', err)
                raise err
