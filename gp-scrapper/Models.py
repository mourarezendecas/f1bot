from datetime import date
from dataclasses import dataclass
from typing import Optional

@dataclass
class Location:
    city: str
    country: str

@dataclass
class Circuit:
    circuit_name: str
    location: Location

@dataclass
class FirstPractice:
    date: date
    time: str

@dataclass
class SecondPractice:
    date: date
    time: str

@dataclass
class ThirdPractice:
    date: date
    time: str

@dataclass
class Qualifying:
    date: date
    time: str

@dataclass
class Sprint:
    date: date
    time: str

@dataclass
class SprintQualifying:
    date: date
    time: str

@dataclass
class Race:
    season: int
    round: int
    race_name: str
    date: date
    first_practice: FirstPractice
    qualifying: Qualifying
    circuit: Circuit
    sprint: Optional[Sprint] = None
    sprint_qualifying: Optional[SprintQualifying] = None
    second_practice: Optional[SecondPractice] = None
    third_practice: Optional[ThirdPractice] = None