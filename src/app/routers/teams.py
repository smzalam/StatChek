from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .db_api_mediation_functions import *
from .database.db_connect import get_pool
from .schemas import *
from pprint import pprint


router = APIRouter()
pool_conn = get_pool()


def get_all_teams_data(team_ids: list):
    table = {
        "teams_table": "teams_info",
        "players_table": "rosters",
        "stats_table": "teams_stats",
        "ranks_table": "teams_ranks",
    }
    response = []
    for team_id in team_ids:
        team_data = select_teams_by_ids_function(
            pool_conn, table["teams_table"], "team_id", team_id
        )[0]
        team_data["players"] = select_players_by_ids_function(
            pool_conn, table["players_table"], "team_id", team_id
        )
        team_data["stats"] = select_teamstatsranks_by_teamid_function(
            pool_conn, table["stats_table"], "team_id", team_id, "stats"
        )
        team_data["ranks"] = select_teamstatsranks_by_teamid_function(
            pool_conn, table["ranks_table"], "team_id", team_id, "ranks"
        )
        response.append(team_data)
    return response


@router.get("/teams", response_model=Teams)
def teams_data(all: bool = False):
    if all:
        table = "teams"
        team_ids_request = select_all_function(pool_conn, table)
        team_ids = []
        for team_id in team_ids_request:
            team_ids.append(team_id["team_id"])
        teams_data = get_all_teams_data(team_ids)
        response = {"teams": teams_data}
        return response
    else:
        table = "teams_info"
        teams_data = select_all_function(pool_conn, table)
        response = {"teams": teams_data}
        return response


@router.get("/teams/{team_id}", response_model=Teams)
def teams_data_id(team_id: int = 0, show_ids: bool = False):
    if show_ids:
        table = "teams"
        teams_data = select_all_function(pool_conn, table)
        response = {"teams": teams_data}
        return response
    else:
        table = "teams_info"
        teams_data = select_teams_by_ids_function(pool_conn, table, "team_id", team_id)
        response = {"teams": teams_data}
        return response


@router.get("/teams/{team_id}/players", response_model=Teams)
def teams_id_players_data(team_id: int, season: int = None):
    table = {"teams_table": "teams_info", "players_table": "rosters"}
    teams_data = select_teams_by_ids_function(
        pool_conn, table["teams_table"], "team_id", team_id
    )[0]
    if not season:
        teams_data["players"] = select_players_by_ids_function(
            pool_conn, table["players_table"], "team_id", team_id
        )
        response = {"teams": [teams_data]}
    else:
        teams_data["players"] = select_players_by_teamid_season_function(
            pool_conn, table["players_table"], team_id, season
        )
        response = {"season": season, "teams": [teams_data]}

    return response


@router.get("/teams/{team_id}/stats", response_model=Teams)
def teams_id_stats_data(team_id: int, season: int = None):
    table = {"teams_table": "teams_info", "stats_table": "teams_stats"}
    teams_data = select_teams_by_ids_function(
        pool_conn, table["teams_table"], "team_id", team_id
    )[0]
    if season:
        teams_data["stats"] = select_teamstatsranks_by_teamid_season_function(
            pool_conn, table["stats_table"], team_id, season, "stats"
        )
        response = {"season": season, "teams": [teams_data]}
    else:
        teams_data["stats"] = select_teamstatsranks_by_teamid_function(
            pool_conn, table["stats_table"], "team_id", team_id, "stats"
        )
        response = {"teams": [teams_data]}

    return response


@router.get("/teams/{team_id}/ranks", response_model=Teams)
def teams_id_ranks_data(team_id: int, season: int = None):
    table = {"teams_table": "teams_info", "ranks_table": "teams_ranks"}
    teams_data = select_teams_by_ids_function(
        pool_conn, table["teams_table"], "team_id", team_id
    )[0]
    if season:
        teams_data["ranks"] = select_teamstatsranks_by_teamid_season_function(
            pool_conn, table["ranks_table"], team_id, season, "ranks"
        )
        response = {"season": season, "teams": [teams_data]}
    else:
        teams_data["ranks"] = select_teamstatsranks_by_teamid_function(
            pool_conn, table["ranks_table"], "team_id", team_id, "ranks"
        )
        response = {"teams": [teams_data]}

    return response


# @app.get("/teams/{team_id}/links")
# @app.get("/teams/{team_id}/schedule")
# @app.get("/teams/{team_id}/history")
