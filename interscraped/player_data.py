import os
import time
from robobrowser import RoboBrowser

default_years = [
    {'2002': 14},
    {'2003': 13},
    {'2004': 12},
    {'2005': 11},
    {'2006': 10},
    {'2007': 9},
    {'2008': 8},
    {'2009': 7},
    {'2010': 6},
    {'2011': 5},
    {'2012': 4},
    {'2013': 3},
    {'2014': 2},
    {'2015': 1},
    {'2016': 0}
]
default_stat_types = [
    {'game': 1},
    # {'redzone': 2},
    # {'3rddwn': 3}
]
default_weeks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

# QB, RB, WR, TE, DL, LB, DB, K, DST
default_pos = [
    {'QB': 2},
    {'RB': 3},
    {'WR': 4},
    {'TE': 5},
    {'DL': 7},
    {'LB': 8},
    {'DB': 9},
    {'K': 10},
    {'DST': 11}
]

# Scoring type (Fanduel default)
fs = 2
# Top level directory name
directory = './player_data'

headers = 'rank,id,player,pos,week,team,opp,opprank,oppposrank,salary,proj,seas'
sn = w = ew = p = scope = None


def scraper():
    browser = RoboBrowser(parser='lxml')

    # Make the top-level directory for the CSV data
    os.mkdir(directory)

    # Open the previously hidden page
    for yearIdx, year in enumerate(default_years):
        year_dict = default_years[yearIdx]
        year_key = list(year_dict.keys())[0]
        sn = year_dict[year_key]

        # Make the top-level directory for the CSV data
        os.mkdir('{}/{}'.format(directory, year_key))

        for pos_idx, pos in enumerate(default_pos):
            pos_dict = default_pos[pos_idx]
            pos_key = list(pos_dict.keys())[0]
            p = pos_dict[pos_key]

            file_path = '{}/{}/{}.csv'.format(directory, year_key, pos_key)
            create_year_file = os.open(file_path, os.O_CREAT)
            os.close(create_year_file)

            for week in default_weeks:
                w = week
                ew = week

                for stat_idx, stat_type in enumerate(default_stat_types):
                    # Assign scope param here
                    stat_type_dict = default_stat_types[stat_idx]
                    stat_type_key = list(stat_type_dict.keys())[0]
                    scope = stat_type_dict[stat_type_key]

                    player_data_url = 'https://fantasydata.com/nfl-stats/nfl-fantasy-football-stats.aspx?fs={}&stype=0&sn={}&scope={}&w={}&ew={}&s=&t=0&p={}&st=FantasyPointsFanDuel&d=1&ls=&live=false&pid=true&minsnaps=4'.format(
                        fs,
                        sn,
                        scope,
                        w,
                        ew,
                        p
                    )

                    # Delay before retrieving next set of data
                    time.sleep(1)

                    browser.open(player_data_url)
                    content = browser.find_all('tr')

                    # Initialize the data to be written to the file
                    formatted_data = ''

                    for idx, line in enumerate(content):
                        # Only add the header once per year
                        if idx == 0 and week == 0 and pos == 2:
                            formatted_data = headers + '\n'
                        elif idx != 0:
                            parsed_data = ','.join(line.find_all(text=True))
                            stripped_line = parsed_data.strip('\n').strip(',')
                            extra_fields = ',' + stat_type_key + ',' + year_key
                            next_line = stripped_line + extra_fields + '\n'

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
