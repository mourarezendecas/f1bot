import datetime
import requests
import json

api_url = "http://ergast.com/api/f1/"

current_year = datetime.datetime.now().year

print(f"Current year is {current_year}")
print("Requesting for API to send the data")

response = requests.get(f"{api_url}{current_year}.json")
print("Request was successful")

races = response.json()["MRData"]["RaceTable"]["Races"]

race_objects = []

for race in races:
    print(f"Processing {race['raceName']}")
    race_objects.append(race)

with open("resources/races.json", 'w') as f:
    print("Writing data to file")
    json_string = json.dumps(race_objects)
    f.write(json_string)

print("Data written to file")
print("Process completed")