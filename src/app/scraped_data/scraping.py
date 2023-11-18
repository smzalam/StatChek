import requests, aiohttp, asyncio
import os
import pandas as pd
from asgiref import sync
from datetime import date

# analyzing lines from when auston matthew was drafted (2016) so making list of years from 2016 - current year
year = date.today().year
years = [2016 + x for x in range(year - 2015)]

# URLs from where to fulfill the HTTP requests
api_urls = {
    "base_url": "https://statsapi.web.nhl.com",
    "conferences": "/api/v1/conferences",
    "divisions": "/api/v1/divisions",
    "teams": "/api/v1/teams",
    "team": "/api/v1/teams/10",
    "team_stats": "/api/v1/teams/{id}/stats?season={season}",
    "rosters": "/api/v1/teams/{id}/roster?season={season}",
    "players": "/api/v1/people/{id}",
    "players_stats_seasonal": "/api/v1/people/{id}/stats?stats=statsSingleSeason&season={season}",
}


def async_aiohttp_get_all(urls, years):
    """
    performs asynchronous get requests
    """

    async def get_all(urls, years):
        async with aiohttp.ClientSession(urls["base_url"]) as session:

            async def fetch(url):
                """
                Gets JSON request from requested url
                """
                async with session.get(url) as response:
                    return await response.json()

            async def get_conferences(urls):
                """
                gets data about all conferences in NHL
                outputs data to csv file
                """

                data = await fetch(urls["conferences"])
                df = pd.json_normalize(data["conferences"], max_level=1)
                title = "./scraped_csv/nhl_details/conferencesAll.csv"
                df.to_csv(title, index=False)
                print(f"File `conferencesAll.csv` created.")

            async def get_divisions(urls):
                """
                gets data about all conferences in NHL
                outputs data to csv file
                """

                data = await fetch(urls["divisions"])
                df = pd.json_normalize(data["divisions"], max_level=1)
                title = "./scraped_csv/nhl_details/divisionsAll.csv"
                df.to_csv(title, index=False)
                print(f"File `divisionsAll.csv` created.")

            async def get_teams_data(urls):
                """
                gets data about all teams in NHL
                outputs data to csv file
                """

                data = await fetch(urls["teams"])
                df = pd.DataFrame()
                for i in range(len(data["teams"])):
                    df_temp = pd.json_normalize(data["teams"][i], max_level=1)
                    df = pd.concat([df, df_temp], ignore_index=True)
                title = "./scraped_csv/team_details/teamAllDetails.csv"
                df.to_csv(title, index=False)
                print(f"File `teamAllDetails.csv` created.")
            
            async def get_team_ids(urls):
                data = await fetch(urls["teams"])
                df = pd.json_normalize(data["teams"], max_level=0)
                return list(df['id'].values)

            async def get_team_stats(urls, years):
                """
                gets stats of the specified team for each year specified
                outputs data to csv file
                """
                team_ids = await get_team_ids(urls)

                for year in years:
                    df = pd.DataFrame()
                    for team_id in team_ids:
                        fields = {"id":f"{team_id}", "season": f"{year}{year+1}"}
                        data = await fetch((urls["team_stats"]).format(**fields))
                        df_temp = pd.json_normalize(
                            data["stats"], record_path=["splits"], meta=[]
                        )
                        try:
                            df_temp.insert(0, column='team_id', value=team_id)
                            df_temp.insert(1, column='season', value=year)
                        except IndexError as e:
                            print(f'{team_ids} insertion skipped due to {e}')
                        df = pd.concat([df, df_temp], ignore_index=True)
                    title = (
                        f"./scraped_csv/team_stats/{fields['season']}_team_stats.csv"
                    )
                    df.to_csv(title, index=False)
                    print(f"File `{fields['season']}_team_stats.csv` created.")

            async def get_players_data(urls, player_ID):
                """
                gets data about player with specified ID
                outputs data to csv file
                """

                fields = {"id": player_ID}
                data = await fetch((urls["players"].format(**fields)))
                df = pd.json_normalize(data["people"], max_level=1)
                title = (
                    f"./scraped_csv/players_details/{fields['id']}_player_details.csv"
                )
                if os.path.isfile(
                    f"./scraped_csv/players_details/{fields['id']}_player_details.csv"
                ):
                    print(f"File `{fields['id']}_player_details.csv` exists.")
                else:
                    df.to_csv(title, index=False)
                    print(f"File `{fields['id']}_player_details.csv` created.")

            async def get_player_stats_seasonal(urls, player_ID, season):
                """
                gets data about player stats
                for player with specified ID
                for the specified season
                outputs data to csv file
                """

                fields = {"id": player_ID, "season": season}
                data = await fetch((urls["players_stats_seasonal"]).format(**fields))
                df = pd.json_normalize(data["stats"][0]["splits"], max_level=1)
                title = f"./scraped_csv/players_stats_seasonal/{fields['id']}_{fields['season']}_stats.csv"
                df.to_csv(title, index=False)
                print(f"File `{fields['id']}_{fields['season']}_stats.csv` created.")

            async def get_team_rosters(urls, years):
                """
                gets data about the specified team's roster for the specified years
                calls functions to get player data and stats for all player on roster for specified year
                outputs data to csv file
                """

                team_ids = await get_team_ids(urls)

                for year in years:
                    df = pd.DataFrame()
                    for team_id in team_ids:
                        try:
                            fields = {"id": f"{team_id}", "season": f"{year}{year+1}"}
                            data = await fetch((urls["rosters"]).format(**fields))
                            df_temp = pd.json_normalize(data["roster"], max_level=1)
                            df_temp.insert(0, column='team_id', value=team_id)
                            df_temp.insert(1, column='season', value=year)
                            df = pd.concat([df, df_temp], ignore_index=True)
                        except KeyError:
                            print(team_id)
                            print(year)
                            print(data)
                        # player_ids = df["person.id"].tolist()
                        # for player_id in player_ids:
                        #     await asyncio.gather(
                        #         get_players_data(urls, player_id),
                        #         get_player_stats_seasonal(
                        #             urls, player_id, fields["season"]
                        #         ),
                        #     )

                    title = (
                        f"./scraped_csv/team_rosters/{fields['season']}_team_roster.csv"
                    )
                    df.to_csv(title, index=False)
                    print(f"File `{fields['season']}_team_roster.csv` created.")

            await asyncio.gather(
                get_conferences(urls),
                get_divisions(urls),
                get_teams_data(urls),
                get_team_stats(urls, years),
                get_team_rosters(urls, years),
            )

    return sync.async_to_sync(get_all)(urls, years)

def scrape_moneypuck_nhl_data():
    seasons = [2012+i for i in range(11)]
    categories = ['skaters', 'goalies', 'teams']
    types = ['regular', 'playoffs']

    for season in seasons:
        os.mkdir(f'../data/NHL/raw/{season}')
        for entry in types:
            for category in categories:
                req = requests.get(
                    f"https://moneypuck.com/moneypuck/playerData/seasonSummary/{season}/{entry}/{category}.csv"
                    )
                url_content = req.content
                with open(f'../data/NHL/raw/{season}/{entry}_{category}.csv', 'wb') as csv_file:
                    csv_file.write(url_content)
                    csv_file.close()

def main():
    action = input('Do I scrape data? Enter Y or N: ')
    if action.upper() == 'Y':
        subaction1 = input('Scrape MoneyPuck or API data? Enter 1 or 2: ')
        if subaction1 == '1':
            scrape_moneypuck_nhl_data()
        elif subaction1 == '2':
            async_aiohttp_get_all(api_urls, years)
    else: 
        print(f'{__file__} has been run!')

if __name__ == "__main__":
    main()