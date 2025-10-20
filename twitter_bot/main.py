import tweepy
import os
import logging
import json
import sys
from datetime import datetime, timedelta
from translate import Translator
from gp_scrapper.Models import *
from gp_scrapper.scrapper import get_next_race
from zoneinfo import ZoneInfo

CURRENT_DATE = date.today()
translator = Translator(to_lang="pt-br")


def converter_para_horario_brasil(utc_datetime_str: str) -> str:
    utc_time = datetime.strptime(utc_datetime_str, '%Y-%m-%dT%H:%M:%SZ')
    utc_time = utc_time.replace(tzinfo=ZoneInfo('UTC'))
    br_time = utc_time.astimezone(ZoneInfo('America/Sao_Paulo'))
    return br_time.strftime('%H:%M:%S')


def generate_tweet(race: Race) -> str:
    days_until_fp = (race.first_practice.date.date() - CURRENT_DATE).days
    translated_race_name = translator.translate(race.race_name)
    fp_time = converter_para_horario_brasil(f"{date.strftime(race.first_practice.date, '%Y-%m-%d')}T{race.first_practice.time}")

    if days_until_fp == 0:
        tweet = f'Começa hoje o {translated_race_name} 🏁\n'
        tweet += f'- FP1: {race.first_practice.date.strftime("%d/%m/%Y")} às {fp_time}\n'

        if race.sprint is not None:
            quali_sprint_time = converter_para_horario_brasil(f'{race.sprint_qualify.date.strftime('%Y-%m-%d')}T{race.sprint_qualify.time}')
            tweet += f'- Quali Sprint: {race.sprint_qualify.date.strftime("%d/%m/%Y")} às {quali_sprint_time}\n'

            sprint_time = converter_para_horario_brasil(f'{race.sprint_qualify.date.strftime('%Y-%m-%d')}T{race.sprint.time}')
            tweet += f'- Sprint: {race.sprint.date.strftime("%d/%m/%Y")} às {sprint_time}\n'

        else:
            fp2_time = converter_para_horario_brasil(f'{race.second_practice.date.strftime("%Y-%m-%d")}T{race.second_practice.time}')
            tweet += f'- FP2: {race.second_practice.date.strftime("%d/%m/%Y")} às {fp2_time}\n'

            fp3_time = converter_para_horario_brasil(f'{race.third_practice.date.strftime("%Y-%m-%d")}T{race.third_practice.time}')
            tweet += f'- FP3: {race.third_practice.date.strftime("%d/%m/%Y")} às {fp3_time}\n'

        race_quali_time = converter_para_horario_brasil(f'{race.qualifying.date.strftime("%Y-%m-%d")}T{race.qualifying.time}')
        tweet += f'- Quali: {race.qualifying.date.strftime("%d/%m/%Y")} às {race_quali_time}\n'

        race_time = converter_para_horario_brasil(f'{race.date.strftime('%Y-%m-%d')}T{race.time}')
        tweet += f'- Corrida: {race.date.strftime("%d/%m/%Y")} às {race_time}'
    else:
        if days_until_fp > 1:
            tweet = f'Faltam {days_until_fp} dias para o {translated_race_name}! 🏁🏎️'
        else:
            tweet = f'Falta {days_until_fp} dia para o {translated_race_name}! 🏁🏎️'

    return tweet

def post_tweet(tweet: str):
    client = tweepy.Client(
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("CONSUMER_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
    )

    post = client.create_tweet(text=tweet)
    if len(post.errors) > 0:
        print(post.errors)
    else:
        return post.data


if __name__ == '__main__':
    next_race = get_next_race()
    tweet = generate_tweet(next_race)
    post = post_tweet(tweet)
