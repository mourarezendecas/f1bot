import tweepy
import os
import logging
import json
import sys
from datetime import datetime
from translate import Translator

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)
json_file_path = os.path.join(project_root, "gp-list", "resources", "races.json")

logger = logging.getLogger(__name__)
logging.basicConfig(filename="exec_main.log", encoding="utf-8", level=logging.DEBUG)
current_data = datetime.now()
translator = Translator(to_lang="pt-br")


def read_data():
    logger.info("Reading data from file")
    json_file = open(json_file_path)
    return json.load(json_file)


def get_next_race():
    logger.info("Getting next upcoming race")
    races = read_data()

    for race in races:
        race_date = datetime.strptime(race["date"], "%Y-%m-%d").date()
        if current_data.date() <= race_date:
            logger.info(f"{race['raceName']} is the next upcoming race.")
            return race


def generate_tweet_string():
    logger.info("Generating tweet text")
    next_race = get_next_race()
    has_sprint = False
    race_date = datetime.strptime(next_race["date"], "%Y-%m-%d").date()
    race_name_translated = translator.translate(next_race["raceName"])
    first_practice_date = datetime.strptime(
        next_race["FirstPractice"]["date"], "%Y-%m-%d"
    ).date()
    qualifying_date = datetime.strptime(
        next_race["Qualifying"]["date"], "%Y-%m-%d"
    ).date()
    try:
        sprint_date = datetime.strptime(next_race["Sprint"]["date"], "%Y-%m-%d").date()
    except KeyError:
        sprint_date = None

    if sprint_date is not None:
        has_sprint = True

    days_until_first_event = (first_practice_date - current_data.date()).days

    logger.info(
        f"{race_name_translated} is the next GP. {days_until_first_event} days until it."
    )

    tweet = ""

    if days_until_first_event == 0:
        tweet = f"Começa hoje o {race_name_translated} 🏁\nQualificação: {qualifying_date.strftime('%d/%m')} ⏱️"
        if has_sprint:
            tweet += f"\nSprint: {sprint_date.strftime('%d/%m')} 🚨"
        tweet += f"\nCorrida: {race_date.strftime('%d/%m')} 🏎️"
    if days_until_first_event == 1:
        tweet = f"Falta 1 dia para o {race_name_translated}! 🏁🏎️"
    if days_until_first_event > 1:
        tweet = f"Faltam {days_until_first_event} dias para {race_name_translated}! 🏁🏎️"
    return tweet


def post_tweet():
    tweet = generate_tweet_string()
    client = tweepy.Client(
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("CONSUMER_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
    )
    try:
        logger.info(f"Tweeting: {tweet}")
        client.create_tweet(text=tweet)
    except Exception as e:
        logger.error(f"Error posting tweet: {e}")


if __name__ == "__main__":
    post_tweet()
