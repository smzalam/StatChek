from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .db_api_mediation_functions import *
from .database.db_connect import get_pool
from .schemas import *
from pprint import pprint
from psycopg_pool import ConnectionPool


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


@router.get("/teams", response_model=Teams)
def teams_data(pool_conn: ConnectionPool = Depends(get_pool), all: bool = False):
    if all:
        metadata = {"table": "teams"}
        team_ids_request = select_all_function(pool_conn, metadata["table"])
        metadata["team_ids"] = [team_id["team_id"] for team_id in team_ids_request]
        # for team_id in team_ids_request:
        #     team_ids.append(team_id["team_id"])
        teams_data = get_all_teams_data(metadata["team_ids"], pool_conn)
        response = {"teams": teams_data}
        return response
    else:
        metadata = {"table": "teams_info"}
        teams_data = select_all_function(pool_conn, metadata["table"])
        response = {"teams": teams_data}
        return response


@router.get("/teams/{team_id}", response_model=Teams)
def teams_data_id(
    pool_conn: ConnectionPool = Depends(get_pool),
    team_id: int = 0,
    show_ids: bool = False,
):
    if show_ids:
        metadata = {"table": "teams"}
        teams_data = select_all_function(pool_conn, metadata["table"])
        response = {"teams": teams_data}
        return response
    else:
        metadata = {"table": "teams_info", "id_type": "team_id"}
        teams_data = select_teams_by_ids_function(
            pool_conn, metadata["table"], metadata["id_type"], team_id
        )
        response = {"teams": teams_data}
        return response


@router.get("/teams/{team_id}/players", response_model=Teams)
def teams_id_players_data(
    team_id: int, pool_conn: ConnectionPool = Depends(get_pool), season: int = None
):
    metadata = {
        "teams_table": "teams_info",
        "players_table": "rosters",
        "id_type": "team_id",
    }
    teams_data = select_teams_by_ids_function(
        pool_conn, metadata["teams_table"], metadata["id_type"], team_id
    )[0]
    if not season:
        teams_data["players"] = select_players_by_ids_function(
            pool_conn, metadata["players_table"], metadata["id_type"], team_id
        )
        response = {"teams": [teams_data]}
    else:
        teams_data["players"] = select_players_by_teamid_season_function(
            pool_conn, metadata["players_table"], team_id, season
        )
        response = {"season": season, "teams": [teams_data]}

    return response


@router.get("/teams/{team_id}/stats", response_model=Teams)
def teams_id_stats_data(
    team_id: int, pool_conn: ConnectionPool = Depends(get_pool), season: int = None
):
    metadata = {
        "teams_table": "teams_info",
        "stats_table": "teams_stats",
        "id_type": "team_id",
        "stats": "stats",
    }
    teams_data = select_teams_by_ids_function(
        pool_conn, metadata["teams_table"], metadata["id_type"], team_id
    )[0]
    if season:
        teams_data["stats"] = select_teamstatsranks_by_teamid_season_function(
            pool_conn, metadata["stats_table"], team_id, season, metadata["stats"]
        )
        response = {"season": season, "teams": [teams_data]}
    else:
        teams_data["stats"] = select_teamstatsranks_by_teamid_function(
            pool_conn, metadata["stats_table"], metadata["id_type"], team_id, "stats"
        )
        response = {"teams": [teams_data]}

    return response


@router.get("/teams/{team_id}/ranks", response_model=Teams)
def teams_id_ranks_data(
    team_id: int, pool_conn: ConnectionPool = Depends(get_pool), season: int = None
):
    metadata = {
        "teams_table": "teams_info",
        "ranks_table": "teams_ranks",
        "id_type": "team_id",
        "ranks": "ranks",
    }
    teams_data = select_teams_by_ids_function(
        pool_conn, metadata["teams_table"], metadata["id_type"], team_id
    )[0]
    if season:
        teams_data["ranks"] = select_teamstatsranks_by_teamid_season_function(
            pool_conn, metadata["ranks_table"], team_id, season, metadata["ranks"]
        )
        response = {"season": season, "teams": [teams_data]}
    else:
        teams_data["ranks"] = select_teamstatsranks_by_teamid_function(
            pool_conn,
            metadata["ranks_table"],
            metadata["id_type"],
            team_id,
            metadata["ranks"],
        )
        response = {"teams": [teams_data]}

    return response


# @app.get("/teams/{team_id}/links")
# @app.get("/teams/{team_id}/schedule")
# @app.get("/teams/{team_id}/history")
