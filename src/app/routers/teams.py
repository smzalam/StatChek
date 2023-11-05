from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .db_api_mediation_functions import *
from .database.db_connect import get_pool
from pprint import pprint


router = APIRouter()
pool_conn = get_pool()


@router.get("/teams")
def teams_data():
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
        stats_data = select_teamstatsranks_by_teamid_season_function(
            pool_conn, table["ranks_table"], team_id, season, "ranks"
        )
        response = {"team": team_data, "season": season, "ranks": stats_data}
    else:
        stats_data = select_teamstatsranks_by_teamid_function(
            pool_conn, table["ranks_table"], "team_id", team_id, "ranks"
        )
        response = {"team": team_data, "ranks": stats_data}

    return response


# @app.get("/teams/{team_id}/links")
# @app.get("/teams/{team_id}/schedule")
# @app.get("/teams/{team_id}/history")
