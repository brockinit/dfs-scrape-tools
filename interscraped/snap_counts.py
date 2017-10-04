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
    {'2017': 0},
]

default_weeks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

# QB, RB, WR, TE
default_pos = [
    {'QB': 2},
    {'RB': 3},
    {'WR': 4},
    {'TE': 5}
]

# Full season or week by week stats
scope = 1
# Scoring type (Fanduel default)
fs = 2

headers = 'rank,id,player,pos,team,opp,week,snaps,snappct,rushpct,tgtpct,tchpct,utlpct,fantpts,pts100snp,seas'
sn = w = ew = p = None


def snap_counts_scraper(
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
        # Assign sn param here
        year_dict = default_years[yearIdx]
        year_key = list(year_dict.keys())[0]
        sn = year_dict[year_key]

        for week in weeks:
            # Assign w and ew params here
            w = week
            ew = week
            for pos_idx, pos in enumerate(default_pos):
                pos_dict = default_pos[pos_idx]
                pos_key = list(pos_dict.keys())[0]
                pos_value = pos_dict[pos_key]
                # Assign p param here
                p = pos_value
                snap_count_url = 'https://fantasydata.com/nfl-stats/nfl-fantasy-football-snap-count-and-snaps-played.aspx?fs={}&stype=0&sn={}&scope={}&w={}&ew={}&s=&t=0&p={}&st=FantasyPointSnapPercentage&d=1&ls=FantasyPointSnapPercentage&live=false&pid=true&minsnaps=4'.format(
                    fs,
                    sn,
                    scope,
                    w,
                    ew,
                    p
                )

                # Delay before retrieving next set of data
                time.sleep(0.5)

                browser.open(snap_count_url)
                content = browser.find_all('tr')

                # Initialize the data to be written to the file
                formatted_data = ''

                for idx, line in enumerate(content):
                    # Only add the header once per year
                    if idx == 0 and week == 0 and pos_value == 2:
                        formatted_data = headers + '\n'
                    elif idx != 0:
                        parsed_data = ','.join(line.find_all(text=True))
                        stripped_line = parsed_data.strip('\n').strip(',')
                        year_value = str(list(year.keys())[0])
                        next_line = stripped_line + ',' + year_value + '\n'

                        if idx == len(content) - 1 and week == 16:
                            formatted_data = formatted_data + stripped_line
                        else:
                            formatted_data = formatted_data + next_line

                # Make the directory for each year of CSV Data
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
