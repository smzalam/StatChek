import requests, aiohttp
import asyncio
import pandas as pd
from asgiref import sync
from datetime import date

# analyzing lines from when auston matthew ws drafted (2016) so making list of years from 2016 - current year
year = date.today().year
years = [2016 + x for x in range(year - 2015)]

api_urls = {
    "base_url": "https://statsapi.web.nhl.com",
    "team": "/api/v1/teams/10",
    "rosters": "/api/v1/teams/10?expand=team.roster&season={season}",
    "players": "/api/v1/people/{id}",
}


def async_aiohttp_get_all(urls):
    """
    performs asynchronous get requests
    """

    async def get_all(urls):
        async with aiohttp.ClientSession(urls["base_url"]) as session:

            async def fetch(url):
                async with session.get(url) as response:
                    return await response.json()

            # async def export_to_csv(data, title):
            #     df = pd.DataFrame(data)
            #     df.to_csv(title, index=False)

            async def get_team_data(urls):
                data = await fetch(urls["team"])
                df = pd.json_normalize(data["teams"][0], max_level=1)
                title = "teamFranchiseDetails.csv"
                df.to_csv(title, index=False)

            async def get_team_data(urls):
                data = await fetch(urls["team"])
                df = pd.json_normalize(data["teams"][0], max_level=1)
                title = "teamFranchiseDetails"
                df.to_csv(title, index=False)

            async def get_team_data(urls):
                data = await fetch(urls["team"])
                df = pd.json_normalize(data["teams"][0], max_level=1)
                title = "teamFranchiseDetails"
                df.to_csv(title, index=False)

            async def get_team_data(urls):
                data = await fetch(urls["team"])
                df = pd.json_normalize(data["teams"][0], max_level=1)
                title = "teamFranchiseDetails"
                df.to_csv(title, index=False)

            await get_team_data(urls)
            # return await asyncio.gather(*[fetch(url) for url in urls])

    return sync.async_to_sync(get_all)(urls)


async_aiohttp_get_all(api_urls)
