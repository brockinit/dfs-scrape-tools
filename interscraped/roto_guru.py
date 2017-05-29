import os
from requests import get
from bs4 import BeautifulSoup

default_years = [2011, 2012, 2013, 2014, 2015, 2016]
default_weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
default_games = ['fd', 'dk', 'yh']
new_headers = 'week;year;gid;name;pos;team;homeaway;oppt;points;salary;league'
base_url = 'http://rotoguru1.com/cgi-bin/fyday.pl'


def scraper(years=None, weeks=None, game=None):
    if years is None or type(years) != list:
        years = default_years
    if weeks is None or type(weeks) != list:
        weeks = default_weeks
    if game is None or type(game) != str:
        game = default_games[0]

    old_headers = 'Week;Year;GID;Name;Pos;Team;h/a;Oppt;{0} points;{0} salary'.format(
        game.upper()
    )

    # Check that game type is valid
    try:
        default_games.index(game)
    except ValueError as err:
        raise err

    # Make the top-level directory for the CSV data
    os.mkdir('./{}'.format(game))

    for year in years:
        # Check that year provided was within boundaries
        try:
            default_years.index(year)
        except ValueError as err:
            print('Year provided is not valid', year)
            raise err

        # Make the directory for each year of CSV Data
        directory = './{}/{}'.format(game, year)
        os.mkdir(directory)

        for week in weeks:
            # Check that week provided was within boundaries
            try:
                default_weeks.index(week)
            except ValueError as err:
                print('Week provided is not valid', week)
                raise err

            url = '{}?year={}&week={}&game=fd&scsv=1'.format(
                base_url,
                year,
                week
            )
            html = get(url)
            soup = BeautifulSoup(html.text, 'lxml')
            raw_data = soup.pre.string.split('\n')

            # Initialize the data to be written to the file
            formatted_data = ''

            # Read each line and filter out malformed data
            for idx, line in enumerate(raw_data):
                if idx == 0:
                    formatted_data = new_headers + '\n'
                elif 'ERR' in line:
                    print('Malformed Line', line)
                else:
                    nullify_na = line.replace('N/A', '')
                    if idx == len(raw_data) - 1:
                        formatted_data = formatted_data + nullify_na.strip()
                    else:
                        next_line = nullify_na.strip() + ';' + game + '\n'
                        formatted_data = formatted_data + next_line

            try:
                # Create new file
                file_path = '{}/{}.csv'.format(directory, week)
                print(file_path)
                create_file = os.open(file_path, os.O_CREAT)
                os.close(create_file)

                # Write to that file
                write_file = open(file_path, 'w')
                write_file.write(formatted_data)
                write_file.close()

            except RuntimeError as err:
                print('Failed to write to file: ', err)
                raise err

    print('Done!! Exiting...')
