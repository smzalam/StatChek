import requests, aiohttp, asyncio
import os.path
import pandas as pd
from asgiref import sync
from datetime import date

# analyzing lines from when auston matthew was drafted (2016) so making list of years from 2016 - current year
year = date.today().year
years = [2016 + x for x in range(year - 2015)]

# URLs from where to fulfill the HTTP requests
api_urls = {
    "base_url": "https://statsapi.web.nhl.com",
    "team": "/api/v1/teams/10",
    "team_stats": "/api/v1/teams/10/stats?season={season}",
    "rosters": "/api/v1/teams/10/roster?season={season}",
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

            async def get_team_data(urls):
                """
                gets data about the specified team
                outputs data to csv file
                """

                data = await fetch(urls["team"])
                df = pd.json_normalize(data["teams"][0], max_level=1)
                title = "./scraped_csv/team_details/teamFranchiseDetails.csv"
                df.to_csv(title, index=False)
                print(f"File `teamFranchiseDetails.csv` created.")

            async def get_team_stats(urls, years):
                """
                gets stats of the specified team for each year specified
                outputs data to csv file
                """

                for year in years:
                    fields = {"season": f"{year}{year+1}"}
                    data = await fetch((urls["team_stats"]).format(**fields))
                    df = pd.json_normalize(
                        data["stats"], record_path=["splits"], meta=[]
                    )
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
                for year in years:
                    fields = {"season": f"{year}{year+1}"}
                    data = await fetch((urls["rosters"]).format(**fields))
                    df = pd.json_normalize(data["roster"], max_level=1)

                    player_ids = df["person.id"].tolist()
                    for player_id in player_ids:
                        await asyncio.gather(
                            get_players_data(urls, player_id),
                            get_player_stats_seasonal(
                                urls, player_id, fields["season"]
                            ),
                        )

                    title = (
                        f"./scraped_csv/team_rosters/{fields['season']}_team_roster.csv"
                    )
                    df.to_csv(title, index=False)
                    print(f"File `{fields['season']}_team_roster.csv` created.")

            await asyncio.gather(
                get_team_data(urls),
                get_team_stats(urls, years),
                get_team_rosters(urls, years),
            )

    return sync.async_to_sync(get_all)(urls, years)


async_aiohttp_get_all(api_urls, years)
