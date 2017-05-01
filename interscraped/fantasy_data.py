import os
from robobrowser import RoboBrowser

login_url = 'https://fantasydata.com/user/login.aspx'

# 2012, 2013, 2014, 2015, 2016
default_years = [0, 1, 2, 3, 4]

default_weeks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

# QB, RB, WR, TE
default_pos = [2, 3, 4, 5]

# Full season or week by week stats
scope = 1
# Scoring type (Fanduel default)
fs = 2

headers = 'rank,id,player,pos,team,gms,snaps,snapsgm,snappct,rushpct,tgtpct,tchpct,utlpct,fantpts,pts100snp'
sn = w = ew = p = None

def scraper():
    browser = RoboBrowser(parser='lxml')
    browser.open(login_url)
    login_form = browser.get_forms()[0]

    # Set login credentials
    login_form['ctl00$Body$EmailTextbox'].value = my_email
    login_form['ctl00$Body$PasswordTextbox'].value = my_pass
    login_form.serialize()

    # Submit login form
    browser.submit_form(login_form)

    # Open the previously hidden page
    for year in default_years:
        # Assign sn param here
        sn = year
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
                browser.open(snap_count_url)
                content = browser.find_all('tr')

                # Initialize the data to be written to the file
                formatted_data = ''

                for idx, line in enumerate(content):
                    # Handle header here
                    if idx == 0:
                        formatted_data = headers + '\n'
                    else:
                        parsed_data = ','.join(line.find_all(text=True))
                        stripped_line = parsed_data.strip('\n').strip(',')
                        next_line = stripped_line + '\n'

                        if idx == len(content) - 1:
                            formatted_data = formatted_data + stripped_line
                        else:
                            formatted_data = formatted_data + next_line

                        print(formatted_data, 'FORMAT')
