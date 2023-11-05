from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .db_api_mediation_functions import *
from .database.db_connect import get_pool
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
        )
        players_data = select_players_by_ids_function(
            pool_conn, table["players_table"], "team_id", team_id
        )
        stats_data = select_teamstatsranks_by_teamid_function(
            pool_conn, table["stats_table"], "team_id", team_id, "stats"
        )
        ranks_data = select_teamstatsranks_by_teamid_function(
            pool_conn, table["ranks_table"], "team_id", team_id, "ranks"
        )
        response.append(
            {
                "team": team_data,
                "players": players_data,
                "stats": stats_data,
                "ranks": ranks_data,
            }
        )
    return response


@router.get("/teams")
def teams_data(all: bool = False):
    if all:
        table = "teams"
        team_ids_request = select_all_function(pool_conn, table)
        team_ids = []
        for team_id in team_ids_request:
            team_ids.append(team_id["team_id"])
        response = get_all_teams_data(team_ids)
        return response
    else:
        table = "teams_info"
        response = select_all_function(pool_conn, table)
        return response


@router.get("/teams/{team_id}")
def teams_data_id(team_id: int = 0, show_ids: bool = False):
    if show_ids:
        table = "teams"
        response = select_all_function(pool_conn, table)
        return response
    else:
        table = "teams_info"
        response = select_teams_by_ids_function(pool_conn, table, "team_id", team_id)
        return response


@router.get("/teams/{team_id}/players")
def teams_id_players_data(team_id: int, season: int = None):
    table = {"teams_table": "teams_info", "players_table": "rosters"}
    teams_data = select_teams_by_ids_function(
        pool_conn, table["teams_table"], "team_id", team_id
    )
    if not season:
        players_data = select_players_by_ids_function(
            pool_conn, table["players_table"], "team_id", team_id
        )
        response = {
            "team": teams_data,
            "players": players_data,
        }
    else:
        players_data = select_players_by_teamid_season_function(
            pool_conn, table["players_table"], team_id, season
        )
        response = {
            "team": teams_data,
            "season": season,
            "players": players_data,
        }

    return response


@router.get("/teams/{team_id}/stats")
def teams_id_stats_data(team_id: int, season: int = None):
    table = {"teams_table": "teams_info", "stats_table": "teams_stats"}
    team_data = select_teams_by_ids_function(
        pool_conn, table["teams_table"], "team_id", team_id
    )
    if season:
        stats_data = select_teamstatsranks_by_teamid_season_function(
            pool_conn, table["stats_table"], team_id, season, "stats"
        )
        response = {"team": team_data, "season": season, "stats": stats_data}
    else:
        stats_data = select_teamstatsranks_by_teamid_function(
            pool_conn, table["stats_table"], "team_id", team_id, "stats"
        )
        response = {"team": team_data, "stats": stats_data}

    return response


@router.get("/teams/{team_id}/ranks")
def teams_id_ranks_data(team_id: int, season: int = None):
    table = {"teams_table": "teams_info", "ranks_table": "teams_ranks"}
    team_data = select_teams_by_ids_function(
        pool_conn, table["teams_table"], "team_id", team_id
    )
    if season:
        ranks_data = select_teamstatsranks_by_teamid_season_function(
            pool_conn, table["ranks_table"], team_id, season, "ranks"
        )
        response = {"team": team_data, "season": season, "ranks": ranks_data}
    else:
        ranks_data = select_teamstatsranks_by_teamid_function(
            pool_conn, table["ranks_table"], "team_id", team_id, "ranks"
        )
        response = {"team": team_data, "ranks": ranks_data}

    return response


# @app.get("/teams/{team_id}/links")
# @app.get("/teams/{team_id}/schedule")
# @app.get("/teams/{team_id}/history")
