from robobrowser import RoboBrowser
import os

url = 'http://www.espn.com/fantasy/football/story/_/page/consistency201416/fantasy-football-consistency-ratings-2014-2016'
directory = './consistency_ratings'
file_path = '{}/2014_2016.csv'.format(directory)
headers = 'player,start_pct,cr,ppr_pct,fanptsgame,start,stud,stiff,sat'
positions = ['QB', 'RB', 'WR', 'TE', 'K', 'D/ST', 'DL', 'LB', 'DB']


def scraper():
    position_index = 0
    browser = RoboBrowser(parser='lxml')
    browser.open(url)

    os.mkdir(directory)

    rows = browser.find_all('tr')

    # Strip unnecessary data
    player_data = rows[4:]

    formatted_data = ''

    for idx, row in enumerate(player_data):
        # Add new headers
        if idx == 0:
            formatted_data = formatted_data + headers + '\n'
        else:
            inner_text = row.find_all(text=True)
            # Skip older headers and switch to next position
            if 'Stiff' in inner_text:
                position_index += 1
            else:
                position_label = positions[position_index]
                parsed_row = ','.join(inner_text) + ',' + position_label
                formatted_data = formatted_data + parsed_row + '\n'

    try:
        # Write to the file
        write_file = open(file_path, 'a')
        write_file.write(formatted_data)
        write_file.close()

    except RuntimeError as err:
        print('Failed to write to file: ', err)
        raise err
