import logging
import datetime
import requests
import json

logger = logging.getLogger(__name__)
logging.basicConfig(filename="exec.log", encoding="utf-8", level=logging.DEBUG)
api_url = "http://ergast.com/api/f1/"

current_year = datetime.datetime.now().year

logger.info(f"Current year is {current_year}")
logger.info("Requesting for API to send the data")

response = requests.get(f"{api_url}{current_year}.json")
logger.info("Request was successful")

races = response.json()["MRData"]["RaceTable"]["Races"]

race_objects = []

for race in races:
    logger.info(f"Processing {race['raceName']}")
    race_objects.append(race)

with open('data.json', 'w', encoding='utf-8') as f:
    logger.info("Writing data to file")
    json.dump(race_objects, f, ensure_ascii=False, indent=4)

logger.info("Data written to file")
logger.info("Process completed")