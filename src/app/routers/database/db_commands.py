from pprint import pprint


"""SELECT COMMANDS"""

select_column_names = """
                SELECT column_name
                FROM information_schema.columns 
                WHERE table_schema = 'public'
                AND table_name = %s
                ORDER BY ordinal_position;
"""

select_all_records = """
                SELECT * FROM {table};
"""

select_conference_by_id = """
                            SELECT * 
                            FROM conferences
                            WHERE id = %s
"""

select_division_by_id = """
                            SELECT * 
                            FROM divisions
                            WHERE {table} = %s
"""

select_teams_by_id = """
                            SELECT * 
                            FROM teams_info
                            WHERE {table} = %s
"""

select_teamstats_by_id = """
                            SELECT *
                            FROM teams_stats
                            WHERE {table} = %s
"""

select_teamstats_by_id_season = """
                            SELECT *
                            FROM teams_stats
                            WHERE team_id = (%s)
                            AND season = (%s)
"""

select_teamranks_by_id = """
                            SELECT *
                            FROM teams_ranks
                            WHERE {table} = %s
"""

select_teamranks_by_id_season = """
                            SELECT *
                            FROM teams_ranks
                            WHERE team_id = (%s)
                            AND season = (%s)
"""

select_players_by_id = """
                            SELECT * 
                            FROM rosters
                            WHERE {table} = %s
"""

select_players_by_teamid_season = """
                            SELECT *
                            FROM rosters
                            WHERE team_id = (%s)
                            AND season = (%s)
"""

select_user_details_id = """
                    SELECT user_id, email
                    FROM users
                    WHERE {table} = %s
"""

"""INSERT COMMANDS"""

insert_new_user = """
                    INSERT INTO users(user_id, email, password)
                    VALUES (%s, %s, %s)
 """
