from pprint import pprint
import json

from fastapi import (
    FastAPI,
    Response,
    status,
    HTTPException,
    Depends,
    APIRouter,
    Query,
    Path,
    Depends,
)
from psycopg_pool import ConnectionPool

import src.app.database.database as db

import src.app.teams.dependencies as dependencies
import src.app.teams.schemas as schemas


router = APIRouter()


def get_all_teams_data(team_ids: list, pool_conn: ConnectionPool):
    metadata = {
        "teams_table": "teams_info",
        "players_table": "rosters",
        "stats_table": "teams_stats",
        "ranks_table": "teams_ranks",
        "id_type": "team_id",
        "stats": "stats",
        "ranks": "ranks",
    }
    response = []
    for team_id in team_ids:
        team_data = select_teams_by_ids_function(
            pool_conn, metadata["teams_table"], metadata["id_type"], team_id
        )[0]
        team_data["players"] = select_players_by_ids_function(
            pool_conn, metadata["players_table"], metadata["id_type"], team_id
        )
        team_data["stats"] = select_teamstatsranks_by_teamid_function(
            pool_conn,
            metadata["stats_table"],
            metadata["id_type"],
            team_id,
            metadata["stats"],
        )
        team_data["ranks"] = select_teamstatsranks_by_teamid_function(
            pool_conn,
            metadata["ranks_table"],
            metadata["id_type"],
            team_id,
            metadata["ranks"],
        )
        response.append(team_data)
    return response


@router.get(
    path="/teams",
    response_model=schemas.Teams,
    status_code=status.HTTP_200_OK,
)
def teams_data(
    team_data: schemas.Teams = Depends(dependencies.valid_all_team_data),
):
    return team_data


@router.get(
    path="/teams/ids",
    response_model=dict[str, list[schemas.TeamsIds]],
    status_code=status.HTTP_200_OK,
)
def all_team_ids(
    team_ids: dict[str, list[schemas.TeamsIds]] = Depends(dependencies.valid_team_ids),
):
    return team_ids


@router.get(
    path="/teams/{team_id}",
    response_model=schemas.Teams,
    status_code=status.HTTP_200_OK,
)
def team_data_id(
    team_id: int,
    team_data: schemas.Teams = Depends(dependencies.valid_team_id_data),
):
    return team_data


@router.get(
    "/teams/{team_id}/players",
    response_model=schemas.Teams,
    status_code=status.HTTP_200_OK,
)
def teams_id_players_data(
    team_id: int,
    season: int = None,
    teams_data: schemas.Teams = Depends(dependencies.valid_team_id_data),
    players_data: schemas.PlayersRequest = Depends(dependencies.valid_players_data),
    players_season_data: schemas.PlayersRequest = Depends(
        dependencies.valid_season_players_data
    ),
):
    response = {"teams": teams_data["teams"]}
    if season:
        response["teams"][0]["players"] = players_season_data["players"]
    else:
        response["teams"][0]["players"] = players_data["players"]
    return response


@router.get(
    "/teams/{team_id}/stats",
    response_model=schemas.Teams,
    status_code=status.HTTP_200_OK,
)
def teams_id_stats_data(
    team_id: int,
    season: int = None,
    teams_data: schemas.Teams = Depends(dependencies.valid_team_id_data),
    stats_data: schemas.StatsRequest = Depends(dependencies.valid_stats_data),
    stats_season_data: schemas.StatsRequest = Depends(
        dependencies.valid_season_stats_data
    ),
):
    response = {"teams": teams_data["teams"]}
    if season:
        response["teams"][0]["stats"] = stats_season_data["stats"]
    else:
        response["teams"][0]["stats"] = stats_data["stats"]
    return response


@router.get(
    "/teams/{team_id}/ranks",
    response_model=schemas.Teams,
    status_code=status.HTTP_200_OK,
)
def teams_id_ranks_data(
    team_id: int,
    season: int = None,
    teams_data: schemas.Teams = Depends(dependencies.valid_team_id_data),
    ranks_data: schemas.RanksRequest = Depends(dependencies.valid_ranks_data),
    ranks_season_data: schemas.RanksRequest = Depends(
        dependencies.valid_season_ranks_data
    ),
):
    response = {"teams": teams_data["teams"]}
    if season:
        response["teams"][0]["ranks"] = ranks_season_data["ranks"]
    else:
        response["teams"][0]["ranks"] = ranks_data["ranks"]
    return response


# @app.get("/teams/{team_id}/links")
# @app.get("/teams/{team_id}/schedule")
# @app.get("/teams/{team_id}/history")
