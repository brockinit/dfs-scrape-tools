import time
import boto3
from robobrowser import RoboBrowser

login_url = 'https://fantasydata.com/user/login.aspx'

default_years = [
    {'2012': 5},
    {'2013': 4},
    {'2014': 3},
    {'2015': 2},
    {'2016': 1},
    {'2017': 0}
]

default_weeks = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

# rankings by position
default_position_rankings = [
    {'file': 'overall', 'url': 'FanDuelFantasyPointsAllowedAverage'},
    {'file': 'qb', 'url': 'FanDuelQuarterbackFantasyPointsAllowedAverage'},
    {'file': 'rb', 'url': 'FanDuelRunningbackFantasyPointsAllowedAverage'},
    {'file': 'wr', 'url': 'FanDuelWideReceiverFantasyPointsAllowedAverage'},
    {'file': 'te', 'url': 'FanDuelTightEndFantasyPointsAllowedAverage'},
    {'file': 'k', 'url': 'FanDuelKickerFantasyPointsAllowedAverage'}
]

# Full season or week by week stats
scope = 1
# Scoring type (Fanduel default)
fs = 1

headers = 'rank,id,player,week,team,opp,games,qbpts,rbpts,wrpts,tepts,kpts,fanptsgame,seas'
sn = w = ew = None


def def_vs_scraper(
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

            for position_ranking in default_position_rankings:
                w = week
                ew = week
                pts_vs_url = 'https://fantasydata.com/nfl-stats/nfl-fantasy-football-points-allowed-defense-by-position.aspx?fs={}&stype=0&sn={}&scope={}&w={}&ew={}&s=&t=0&p=0&st={}&d=1&ls={}&live=false&pid=true&minsnaps=4'.format(
                    fs,
                    sn,
                    scope,
                    w,
                    ew,
                    position_ranking['url'],
                    position_ranking['url']
                )

                # Delay before retrieving next set of data
                time.sleep(0.5)

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

                # Make the directory for each year of CSV Data
                file_path = '{}/{}/{}/{}.csv'.format(
                    obj_path,
                    year_key,
                    week + 1,
                    position_ranking['file']
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
