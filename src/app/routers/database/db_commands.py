from pprint import pprint


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
