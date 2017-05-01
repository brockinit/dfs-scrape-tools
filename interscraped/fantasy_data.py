import os
import time
from robobrowser import RoboBrowser

login_url = 'https://fantasydata.com/user/login.aspx'

default_years = [
    {'2012': 4},
    {'2013': 3},
    {'2014': 2},
    {'2015': 1},
    {'2016': 0}
]

default_weeks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

# QB, RB, WR, TE
default_pos = [2, 3, 4, 5]

# Full season or week by week stats
scope = 1
# Scoring type (Fanduel default)
fs = 2
# Top level directory name
directory = './snap_count'

headers = 'rank,id,player,pos,team,opp,week,snaps,snappct,rushpct,tgtpct,tchpct,utlpct,fantpts,pts100snp,seas'
sn = w = ew = p = None


def scraper(email, password):
    browser = RoboBrowser(parser='lxml')
    browser.open(login_url)
    login_form = browser.get_forms()[0]

    # Set login credentials
    login_form['ctl00$Body$EmailTextbox'].value = email
    login_form['ctl00$Body$PasswordTextbox'].value = password
    login_form.serialize()

    # Submit login form
    browser.submit_form(login_form)

    # Make the top-level directory for the CSV data
    os.mkdir(directory)

    # Open the previously hidden page
    for yearIdx, year in enumerate(default_years):
        # Assign sn param here
        year_dict = default_years[yearIdx]
        year_key = list(year_dict.keys())[0]
        sn = year_dict[year_key]

        # Make the directory for each year of CSV Data
        file_path = '{}/{}.csv'.format(directory, year_key)
        create_year_file = os.open(file_path, os.O_CREAT)
        os.close(create_year_file)

        for week in default_weeks:
            # Assign w and ew params here
            w = week
            ew = week
            for pos in default_pos:
                # Assign p param here
                p = pos
                snap_count_url = 'https://fantasydata.com/nfl-stats/nfl-fantasy-football-snap-count-and-snaps-played.aspx?fs={}&stype=0&sn={}&scope={}&w={}&ew={}&s=&t=0&p={}&st=FantasyPointSnapPercentage&d=1&ls=&live=false&pid=true&minsnaps=4'.format(
                    fs,
                    sn,
                    scope,
                    w,
                    ew,
                    p
                )

                # Delay before retrieving next set of data
                time.sleep(2)

                browser.open(snap_count_url)
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
                        year_value = str(list(year.keys())[0])
                        next_line = stripped_line + ',' + year_value + '\n'

                        if idx == len(content) - 1 and week == 16:
                            formatted_data = formatted_data + stripped_line
                        else:
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
