import os
from robobrowser import RoboBrowser

login_url = 'https://fantasydata.com/user/login.aspx'
snap_count_url = 'https://fantasydata.com/nfl-stats/nfl-fantasy-football-snap-count-and-snaps-played.aspx?fs=0&stype=0&sn=0&scope=0&w=0&ew=0&s=&t=0&p=2&st=FantasyPointSnapPercentage&d=1&ls=&live=false&pid=true&minsnaps=4'

default_years = [2011, 2012, 2013, 2014, 2015, 2016]
default_weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

# QB, RB, WR, TE
default_pos = [2, 3, 4, 5]

headers = 'rank,id,player,pos,team,gms,snaps,snapsgm,snappct,rushpct,tgtpct,tchpct,utlpct,fantpts,pts100snp'


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
        for week in default_weeks:
            # Assign w and ew params here
            for pos in default_pos:
                # Assign p param here
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
