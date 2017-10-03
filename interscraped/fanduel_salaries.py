import time
import boto3
from robobrowser import RoboBrowser

default_years = [
    {'2015': 2},
    {'2016': 1},
    {'2017': 0}
]

default_weeks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

# QB, RB, WR, TE, DL, LB, DB, K, DST
default_pos = [
    {'QB': 2},
    {'RB': 3},
    {'WR': 4},
    {'TE': 5},
    {'K': 6},
    {'DST': 7}
]

# Scoring type (Fanduel default)
fs = 0

headers = 'rank,id,player,pos,week,team,opp,opprank,oppposrank,salary,proj,seas'
sn = w = ew = p = scope = None

login_url = 'https://fantasydata.com/user/login.aspx'


def fanduel_salaries_scraper(credentials, bucket_name, obj_path, years=default_years, weeks=default_weeks):
    client = boto3.client('s3')
    browser = RoboBrowser(parser='lxml')
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

            # Initialize the data to be written to the file
            formatted_data = ''

            for pos_idx, pos in enumerate(default_pos):
                pos_dict = default_pos[pos_idx]
                pos_key = list(pos_dict.keys())[0]
                p = pos_dict[pos_key]

                salary_data_url = 'https://fantasydata.com/nfl-stats/daily-fantasy-football-salary-and-projection-tool.aspx?fs={}&stype=0&sn={}&scope=0&w={}&ew={}&s=&t=0&p={}&st=FantasyPointsFanDuel&d=1&ls=&live=false&pid=true&minsnaps=4'.format(
                    fs,
                    sn,
                    w,
                    ew,
                    p
                )

                # Delay before retrieving next set of data
                time.sleep(0.25)

                browser.open(salary_data_url)
                content = browser.find_all('tr')

                for idx, line in enumerate(content):
                    # Only add the header once per year
                    if idx == 0 and week == 0 and p == 2:
                        formatted_data = headers + '\n'
                    elif idx != 0:
                        parsed_data = ','.join(line.find_all(text=True))
                        stripped_line = parsed_data.strip('\n').strip(',')
                        extra_fields = ',' + year_key
                        next_line = stripped_line + extra_fields + '\n'

                        formatted_data = formatted_data + next_line

                file_path = '{}/{}/{}.csv'.format(
                    obj_path,
                    year_key,
                    week + 1
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
