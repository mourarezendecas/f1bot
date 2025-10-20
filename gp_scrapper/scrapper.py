import requests
import json
from translate import Translator
from datetime import date, datetime
from aws_services_common.s3_client import save_file, list_folders, get_json_to_dict
from .Models import *

URL_API = "http://api.jolpi.ca/ergast/f1"
CURRENT_DATE = date.today()
translator = Translator(to_lang="pt-br")

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

def get_next_race_date():
    pastas = list_folders(str(CURRENT_DATE.year))
    datas_obtidas = []

    for pasta in pastas:
        data = datetime.strptime(pasta.strip('/').split('/')[-1], "%Y-%m-%d").date()
        datas_obtidas.append(data)

    datas_futuras = [d for d in datas_obtidas if d >= CURRENT_DATE]

    proxima_data = min(datas_futuras)
    return proxima_data

def get_next_race():
    next_race_date = get_next_race_date()
    dict_race = get_json_to_dict(f'races/{next_race_date.year}/{next_race_date.strftime("%Y-%m-%d")}/')
    race_obj = Race(
        season=dict_race['season'],
        round=dict_race['round'],
        race_name=dict_race['raceName'],
        date=datetime.strptime(dict_race['date'], '%Y-%m-%d').date(),
        time=dict_race['time'],
        first_practice=FirstPractice(
            date=datetime.strptime(dict_race['FirstPractice']['date'], '%Y-%m-%d'),
            time=dict_race['FirstPractice']['time']
        ),
        qualifying=Qualifying(
            date=datetime.strptime(dict_race['Qualifying']['date'], '%Y-%m-%d'),
            time=dict_race['Qualifying']['time']
        ),
        circuit=Circuit(
            circuit_name=dict_race['Circuit']['circuitName'],
            location=Location(
                city=dict_race['Circuit']['Location']['locality'],
                country=dict_race['Circuit']['Location']['country']
            )
        )
    )

    if 'Sprint' in dict_race:
        sprint_qualify = SprintQualifying(
            date=datetime.strptime(dict_race['SprintQualifying']['date'], '%Y-%m-%d'),
            time=dict_race['SprintQualifying']['time']
        )
        sprint = Sprint(
            date=datetime.strptime(dict_race['Sprint']['date'], '%Y-%m-%d'),
            time=dict_race['Sprint']['time']
        )
        race_obj.sprint = sprint
        race_obj.sprint_qualify = sprint_qualify
    else:
        secound_practice = SecondPractice(
            date=datetime.strptime(dict_race['SecondPractice']['date'], '%Y-%m-%d'),
            time=dict_race['SecondPractice']['time']
        )
        third_practice = ThirdPractice(
            date=datetime.strptime(dict_race['ThirdPractice']['date'], '%Y-%m-%d'),
            time=dict_race['ThirdPractice']['time']
        )
        race_obj.second_practice = secound_practice
        race_obj.third_practice = third_practice

    return race_obj