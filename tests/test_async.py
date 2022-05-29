import pytest
import aiohttp
from pprint import pprint as print

import fortnite_api

@pytest.mark.asyncio
async def test_async_client():
    session = aiohttp.ClientSession()
    async with fortnite_api.AsyncFortniteAPI(session=session) as client:

        cosmetics = await client.fetch_cosmetics()
        print(cosmetics[0].id)

        shop = await client.fetch_br_shop()
        print(shop)

        cosmetic = await client.fetch_cosmetic('CID_461_Athena_Commando_M_DriftSummer')
        print(cosmetic)

        cosmetics = await client.search_cosmetic(multiple=True, id='CID_298_Athena_Commando_F_IceMaiden')
        print(cosmetics)

        aes = await client.fetch_aes()
        print(aes)

        banners = await client.fetch_banners()
        print(len(banners))

        banner_colors = await client.fetch_banner_colors()
        print(len(banner_colors))

        code = await client.fetch_creator_code('Ninja')
        print(code)

        fortnite_map = await client.fetch_map()
        print(fortnite_map)