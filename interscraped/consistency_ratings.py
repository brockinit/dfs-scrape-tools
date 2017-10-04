import boto3
from robobrowser import RoboBrowser

url = 'http://www.espn.com/fantasy/football/story/_/page/consistency201417/fantasy-football-consistency-ratings-2014-2017'
directory = './consistency_ratings'
headers = 'player,start_pct,cr,ppr_pct,fanptsgame,start,stud,stiff,sat'
positions = ['QB', 'RB', 'WR', 'TE', 'K', 'D/ST', 'DL', 'LB', 'DB']


def consistency_scraper(bucket_name, obj_path, file_path='2014_2017'):
    client = boto3.client('s3')

    position_index = 0
    browser = RoboBrowser()
    browser.open(url)

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
        # Upload object to the S3 bucket
        client.put_object(
            Bucket=bucket_name,
            Body=formatted_data,
            Key='{}/{}.csv'.format(
                obj_path,
                file_path
            )
        )
    except RuntimeError as err:
        print('Failed to upload object: ', err)
        raise err

    print('Success! Uploaded data: {}'.format(file_path))
