from pydantic import BaseModel


class DivisionsRequest(BaseModel):
    id: int
    name: str
    abbreviation: str
    link: str
    active: bool
    conference_id: int


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


class ConferencesRequest(BaseModel):
    id: int
    name: str
    link: str
    abbreviation: str
    active: bool
    divisions: list[DivisionsRequest] | None = None
    teams: list[TeamsRequest] | None = None


class Conferences(BaseModel):
    conferences: list[ConferencesRequest]
