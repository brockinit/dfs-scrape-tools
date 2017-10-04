import time
import boto3
from robobrowser import RoboBrowser

login_url = 'https://fantasydata.com/user/login.aspx'

default_years = [
    {'2002': 15},
    {'2003': 14},
    {'2004': 13},
    {'2005': 12},
    {'2006': 11},
    {'2007': 10},
    {'2008': 9},
    {'2009': 8},
    {'2010': 7},
    {'2011': 6},
    {'2012': 5},
    {'2013': 4},
    {'2014': 3},
    {'2015': 2},
    {'2016': 1},
    {'2017': 0}
]

redzone_3rddwn_years = [
    {'2015': 2},
    {'2016': 1},
    {'2017': 0}
]

# Available stat data
default_stat_types = [
    {'game': 1},
    {'redzone': 2},
    {'3rddwn': 3}
]

default_weeks = [
    {'1': 0},
    {'2': 1},
    {'3': 2},
    {'4': 3},
    {'5': 4},
    {'6': 5},
    {'7': 6},
    {'8': 7},
    {'9': 8},
    {'10': 9},
    {'11': 10},
    {'12': 11},
    {'13': 12},
    {'14': 13},
    {'15': 14},
    {'16': 15}
]

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

redzone_3rddwn_pos = [
    {'QB': 2},
    {'RB': 3},
    {'WR': 4},
    {'TE': 5},
]

# Scoring type (Fanduel default)
fs = 2

headers = 'rank,id,player,pos,week,team,opp,opprank,oppposrank,salary,proj,seas'
sn = w = ew = p = scope = None


def player_stats_scraper(
    credentials,
    bucket_name,
    obj_path,
    years=default_years,
    weeks=default_weeks
):
    client = boto3.client('s3')
    browser = RoboBrowser()
    browser.open(login_url)
    login_form = browser.get_forms()[0]

    # Set login credentials
    login_form['ctl00$Body$EmailTextbox'].value = credentials['email']
    login_form['ctl00$Body$PasswordTextbox'].value = credentials['password']
    login_form.serialize()

    for stat_idx, stat_type in enumerate(default_stat_types):
        years_list = years

        if list(stat_type.keys())[0] != 'game':
            pos_list = redzone_3rddwn_pos
        else:
            pos_list = default_pos

        # Open the previously hidden page
        for yearIdx, year in enumerate(years_list):
            year_dict = years_list[yearIdx]
            year_key = list(year_dict.keys())[0]
            sn = year_dict[year_key]

            for pos_idx, pos in enumerate(pos_list):
                pos_dict = default_pos[pos_idx]
                pos_key = list(pos_dict.keys())[0]
                p = pos_dict[pos_key]

                for week_idx, week in enumerate(weeks):
                    week_dict = weeks[week_idx]
                    week_key = list(week_dict.keys())[0]
                    cur_week = week_dict[week_key]
                    w = cur_week
                    ew = cur_week

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
                    time.sleep(0.5)

                    browser.open(player_data_url)
                    content = browser.find_all('tr')

                    # Initialize the data to be written to the file
                    formatted_data = ''

                    for idx, line in enumerate(content):
                        # Only add the header once per year
                        if idx == 0 and cur_week == 0 and pos == 2:
                            formatted_data = headers + '\n'
                        elif idx != 0:
                            parsed_data = ','.join(line.find_all(text=True))
                            stripped_line = parsed_data.strip('\n').strip(',')
                            extra_fields = ',' + stat_type_key + ',' + year_key
                            next_line = stripped_line + extra_fields + '\n'

                            formatted_data = formatted_data + next_line

                    file_path = '{}{}/{}/{}/{}.csv'.format(
                        obj_path,
                        stat_type_key,
                        year_key,
                        week_key,
                        pos_key
                    )

                    try:
                        # Upload object to the S3 bucket
                        client.put_object(
                            Bucket=bucket_name,
                            Body=formatted_data,
                            Key=file_path
                        )
                    except RuntimeError as err:
                        print('Failed to write to file: ', err)
                        raise err

                    print('Success! Uploaded data: {}'.format(file_path))
