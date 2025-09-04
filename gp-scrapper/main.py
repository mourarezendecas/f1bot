import requests
import json
from datetime import date
from aws_services_common.s3_client import save_file

URL_API = "http://api.jolpi.ca/ergast/f1"
CURRENT_DATE = date.today()

def get_races(year):
    r = requests.get(f'{URL_API}/{year}')
    return r.json()['MRData']['RaceTable']['Races']

def execute_backup():
    races = get_races(CURRENT_DATE.year)
    for race in races:
        folder_name = f"races/{race['season']}/{race['date']}"
        file_name = f"{race['raceName'].replace(' ', '_').lower()}.json"
        data = json.dumps(race, ensure_ascii=False, indent=4)
        save_file(
            content=data,
            file_name=file_name,
            folder_name=folder_name
        )

def get_next_race():
    pass