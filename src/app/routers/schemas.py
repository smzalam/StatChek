from pydantic import BaseModel, EmailStr
from datetime import datetime


class RanksRequest(BaseModel):
    team_id: int
    season: int
    games_won: str
    games_lost: str
    games_lost_ot: str
    points: str
    points_pct: str
    goals_per_game: str
    goals_against_per_game: str
    ev_gga_ratio: str
    powerplay_pct: str
    powerplay_goals: str
    powerplay_goals_against: str
    powerplay_opportunities: str
    penaltykill_pct: str
    shots_per_game: str
    shots_allowed: str
    win_when_score_first: str
    win_when_opp_score_first: str
    win_when_leading_first_per: str
    win_when_leading_second_per: str
    win_when_outshooting_opp: str
    win_when_opp_outshooting: str
    faceoffs_taken: str
    faceoffs_won: str
    faceoffs_lost: str
    faceoff_win_pct: str
    shooting_pct: str
    save_pct: str


class StatsRequest(BaseModel):
    team_id: int
    season: int
    games_played: int
    games_won: int
    games_lost: int
    games_lost_ot: int
    points: int
    points_pct: float
    goals_per_game: float
    goals_against_per_game: float
    ev_gga_ratio: float
    powerplay_pct: float
    powerplay_goals: float
    powerplay_goals_against: float
    powerplay_opportunities: float
    penaltykill_pct: float
    shots_per_game: float
    shots_allowed: float
    win_when_score_first: float
    win_when_opp_score_first: float
    win_when_leading_first_per: float
    win_when_leading_second_per: float
    win_when_outshooting_opp: float
    win_when_opp_outshooting: float
    faceoffs_taken: float
    faceoffs_won: float
    faceoffs_lost: float
    faceoff_win_pct: float
    shooting_pct: float
    save_pct: float


class PlayersRequest(BaseModel):
    team_id: int
    season: int
    player_id: int
    full_name: str
    first_name: str
    last_name: str
    jersey_number: int
    position: str
    position_code: str


class TeamsIds(BaseModel):
    id: int
    team_id: int
    name: str


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
    players: list[PlayersRequest] | str = "Not Requested"
    stats: list[StatsRequest] | str = "Not Requested"
    ranks: list[RanksRequest] | str = "Not Requested"


class DivisionsRequest(BaseModel):
    id: int
    name: str
    abbreviation: str
    link: str
    active: bool
    conference_id: int
    teams: list[TeamsRequest] | str = "Not Requested"


class ConferencesRequest(BaseModel):
    id: int
    name: str
    link: str
    abbreviation: str
    active: bool
    divisions: list[DivisionsRequest] | str = "Not Requested"
    teams: list[TeamsRequest] | str = "Not Requested"


class Conferences(BaseModel):
    conferences: list[ConferencesRequest]


class Divisions(BaseModel):
    divisions: list[DivisionsRequest]


class Teams(BaseModel):
    season: int | str = "all"
    teams: list[TeamsRequest | TeamsIds]


class Players(BaseModel):
    player_id: int
    players: list[PlayersRequest]


class UserCreate(BaseModel):
    user_id: str | None = None
    email: EmailStr
    password: str


class UserRequest(BaseModel):
    user_id: str
    email: EmailStr
    created_at: datetime


class User(BaseModel):
    users: list[UserRequest]
