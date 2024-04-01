import requests
from pprint import pprint as print

import fortnite_api


def test_sync_client():
    session = requests.Session()
    client = fortnite_api.SyncFortniteAPI(session=session)

    cosmetics = client.fetch_cosmetics()
    print(cosmetics[0].id)

    shop = client.fetch_br_shop()
    print(shop)

    cosmetic = client.fetch_cosmetic('CID_461_Athena_Commando_M_DriftSummer')
    print(cosmetic)

    cosmetics = client.search_cosmetic(multiple=True, id='CID_298_Athena_Commando_F_IceMaiden')
    print(cosmetics)

    aes = client.fetch_aes()
    print(aes)

    banners = client.fetch_banners()
    print(len(banners))

    banner_colors = client.fetch_banner_colors()
    print(len(banner_colors))

    code = client.fetch_creator_code('Ninja')
    print(code)

    fortnite_map = client.fetch_map()
    print(fortnite_map)
