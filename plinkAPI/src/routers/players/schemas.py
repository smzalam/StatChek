from pydantic import BaseModel, EmailStr
from datetime import datetime


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


class Players(BaseModel):
    player_id: int
    players: list[PlayersRequest]
