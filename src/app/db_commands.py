from pprint import pprint

conferences: """
                SELECT * FROM conferences;
"""
divisions: """
                SELECT * FROM divisions;
"""
teams: """
                SELECT * FROM teams;
"""
teams_info: """
                SELECT * FROM teams_info;
"""
teams_stats: """
                SELECT * FROM teams_stats;
"""
teams_ranks: """
                SELECT * FROM teams_ranks;
"""
rosters: """
                SELECT * FROM rosters;
"""
players: """
                SELECT * FROM players;
"""
column_names: """
                SELECT column_name
                FROM information_schema.columns 
                WHERE table_schema = 'public'
                AND table_name = %s
                ORDER BY ordinal_position;
"""
