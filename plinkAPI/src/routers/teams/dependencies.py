from psycopg_pool import ConnectionPool
from fastapi import Depends
from pprint import pprint

import src.app.database.database as db
import src.app.database.db_service as db_funcs
import src.app.teams.schemas as schemas
import src.app.teams.constants as constants


def valid_teams_ids_list(
    pool_conn: ConnectionPool = db.get_pool(),
) -> list:
    team_ids = db_funcs.select_all_ids_function(
        directory=constants.CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.TEAMS_INFO_TABLE,
    )

    return team_ids


def valid_team_ids(
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> dict[str, [schemas.TeamsIds]]:
    teams_data = db_funcs.select_all_function(
        directory=constants.CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.TEAMS_INFO_TABLE,
    )
    team_ids = [
        #! CHANGE 'NAME' TO 'TEAM_NAME' FOR TEAMS_INFO TABLE IN DATABASE
        {
            "team_id": team_data_row[constants.TEAM_ID_COLUMN],
            "name": team_data_row[constants.TEAM_NAME_COLUMN],
        }
        for team_data_row in teams_data
    ]
    return {"team_ids": team_ids}


def valid_team_id_data(
    team_id: int,
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.Teams:
    team_data = db_funcs.select_teams_by_ids_function(
        directory=constants.CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.TEAMS_INFO_TABLE,
        id_type=constants.TEAM_ID_COLUMN,
        id_num=team_id,
    )
    if not team_data:
        raise NameError
    return {"teams": team_data}


def valid_all_team_data(
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.Teams:
    team_data = db_funcs.select_all_function(
        directory=constants.CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.TEAMS_INFO_TABLE,
    )

    if not team_data:
        raise NameError

    return {"teams": team_data}


def valid_players_data(
    team_id: int,
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.PlayersRequest:
    players_data = db_funcs.select_players_by_teamid_function(
        directory=constants.CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.PLAYERS_TABLE,
        id_type=constants.TEAM_ID_COLUMN,
        id_num=team_id,
    )

    if not players_data:
        raise NameError
    return {"players": players_data}


def valid_season_players_data(
    team_id: int,
    season: int = None,
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.PlayersRequest:
    if season:
        players_data = db_funcs.select_players_by_teamid_season_function(
            directory=constants.CACHE_DIRECTORY,
            db_conn=pool_conn,
            db_table=constants.PLAYERS_TABLE,
            team_id=team_id,
            season=season,
        )

        if not players_data:
            raise NameError
        return {"players": players_data}
    else:
        return None


def valid_stats_data(
    team_id: int,
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.StatsRequest:
    stats_data = db_funcs.select_teamstatsranks_by_teamid_function(
        directory=constants.CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.STATS_TABLE,
        team_id=team_id,
        detail_type=constants.STATS,
    )

    if not stats_data:
        raise NameError
    return {"stats": stats_data}


def valid_season_stats_data(
    team_id: int,
    season: int = None,
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.StatsRequest:
    if season:
        stats_data = db_funcs.select_teamstatsranks_by_teamid_season_function(
            directory=constants.CACHE_DIRECTORY,
            db_conn=pool_conn,
            db_table=constants.STATS_TABLE,
            team_id=team_id,
            season=season,
            detail_type=constants.STATS,
        )

        if not stats_data:
            raise NameError
        return {"stats": stats_data}
    else:
        return None


def valid_ranks_data(
    team_id: int,
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.RanksRequest:
    ranks_data = db_funcs.select_teamstatsranks_by_teamid_function(
        directory=constants.CACHE_DIRECTORY,
        db_conn=pool_conn,
        db_table=constants.RANKS_TABLE,
        team_id=team_id,
        detail_type=constants.RANKS,
    )

    if not ranks_data:
        raise NameError
    return {"ranks": ranks_data}


def valid_season_ranks_data(
    team_id: int,
    season: int = None,
    pool_conn: ConnectionPool = Depends(db.get_pool),
) -> schemas.RanksRequest:
    if season:
        ranks_data = db_funcs.select_teamstatsranks_by_teamid_season_function(
            directory=constants.CACHE_DIRECTORY,
            db_conn=pool_conn,
            db_table=constants.RANKS_TABLE,
            team_id=team_id,
            season=season,
            detail_type=constants.RANKS,
        )

        if not ranks_data:
            raise NameError
        return {"ranks": ranks_data}
    else:
        return None


# def get_conference_data(
#     conference_id: int,
#     division_data: schemas.Divisions = Depends(valid_division_id_data),
#     teams_data: schemas.Teams = Depends(valid_teams_data),
# ):
#     pass


constants.ALL_TEAM_IDS = valid_teams_ids_list()
print("Updated team ids constant!")
db_funcs.update_cache(constants.CACHE_DIRECTORY)
