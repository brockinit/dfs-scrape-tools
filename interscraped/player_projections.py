import time
import boto3
from robobrowser import RoboBrowser

default_years = [
    {'2013': 4},
    {'2014': 3},
    {'2015': 2},
    {'2016': 1},
    {'2017': 0}
]
default_stat_types = [
    {'game': 1},
]
default_weeks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

# QB, RB, WR, TE, DL, LB, DB, K, DST
default_pos = [
    {'QB': 1},
    {'RB': 2},
    {'WR': 3},
    {'TE': 4},
    {'K': 5},
    {'DST': 6}
]

# Scoring type (Fanduel default)
fs = 2

headers = 'rank,id,player,pos,week,team,opp,passyds,td,int,proj,seas'
sn = w = ew = p = scope = None

login_url = 'https://fantasydata.com/user/login.aspx'


def player_projections_scraper(
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

    # Submit login form
    browser.submit_form(login_form)

    # Open the previously hidden page
    for yearIdx, year in enumerate(years):
        year_dict = years[yearIdx]
        year_key = list(year_dict.keys())[0]
        sn = year_dict[year_key]

        for week in weeks:
            w = week
            ew = week

            for pos_idx, pos in enumerate(default_pos):
                pos_dict = default_pos[pos_idx]
                pos_key = list(pos_dict.keys())[0]
                p = pos_dict[pos_key]

                for stat_idx, stat_type in enumerate(default_stat_types):
                    # Assign scope param here
                    stat_type_dict = default_stat_types[stat_idx]
                    stat_type_key = list(stat_type_dict.keys())[0]
                    scope = stat_type_dict[stat_type_key]
                    player_data_url = 'https://fantasydata.com/nfl-stats/fantasy-football-weekly-projections.aspx?fs={}&stype=0&sn={}&scope={}&w={}&ew={}&s=&t=0&p={}&st=FantasyPointsFanDuel&d=1&ls=&live=false&pid=true&minsnaps=4'.format(
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
                        if idx == 0 and week == 0 and p == 2:
                            formatted_data = headers + '\n'
                        elif idx != 0:
                            parsed_data = ','.join(line.find_all(text=True))
                            stripped_line = parsed_data.strip('\n').strip(',')
                            extra_fields = ',' + stat_type_key + ',' + year_key
                            next_line = stripped_line + extra_fields + '\n'

                            formatted_data = formatted_data + next_line

                    file_path = '{}/{}/{}/{}.csv'.format(
                        obj_path,
                        year_key,
                        week + 1,
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
