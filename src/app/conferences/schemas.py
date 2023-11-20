from pydantic import BaseModel, EmailStr
from datetime import datetime


"""API DATA SCHEMAS"""

"""TEAMS SCHEMAS"""


class TeamsRequest(BaseModel):
    id: int
    team_id: int
    name: str
    abbreviation: str
    location: str
    inaugaration_year: int
    url: str
    venue: str
    division_id: int
    conference_id: int


class Teams(BaseModel):
    season: int | str = "all"
    teams: list[TeamsRequest]


"""DIVISIONS SCHEMAS"""


class DivisionsRequest(BaseModel):
    division_id: int
    name: str
    abbreviation: str
    link: str
    active: bool
    conference_id: int


class Divisions(BaseModel):
    divisions: list[DivisionsRequest]


"""CONFERENCE SCHEMAS"""


class ConferenceIds(BaseModel):
    conference_id: int
    name: str


class ConferencesRequest(BaseModel):
    conference_id: int
    name: str
    link: str
    abbreviation: str
    active: bool
    divisions: list[DivisionsRequest] | str = "Not Requested"
    teams: list[TeamsRequest] | str = "Not Requested"


class Conferences(BaseModel):
    conferences: list[ConferencesRequest]
