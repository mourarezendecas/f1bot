import tweepy
import os
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(filename="exec.log", encoding="utf-8", level=logging.DEBUG)
json_file_path = "../gp-list/resources/races.json"
current_data = datetime.now()


def read_data():
    logger.info("Reading data from file")
    json_file = open(json_file_path)
    return json.load(json_file)

races = read_data()

incoming_races = []

for race in races:
    print(race["raceName"])
    print(race["FirstPractice"]["date"])
    race_date = datetime.strptime(race["FirstPractice"]["date"], "%Y-%m-%d").date()
    if current_data.date() < race_date:
        print("Incoming race")

#client = tweepy.Client(
#    consumer_key=os.getenv('CONSUMER_KEY'),
#    consumer_secret=os.getenv('CONSUMER_SECRET'),
#    access_token=os.getenv('ACCESS_TOKEN'),
#    access_token_secret=os.getenv('ACCESS_TOKEN_SECRET')
#)