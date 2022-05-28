import requests
from pprint import pprint as print

from ..fortnite_api import FortniteAPI


def main():
    session = requests.Session()
    client = FortniteAPI(session=session)

    cosmetics = client.fetch_cosmetics()
    print(cosmetics[0].id)

    shop = client.fetch_br_shop()
    print(shop.raw_data)

    cosmetic = client.fetch_cosmetic('CID_461_Athena_Commando_M_DriftSummer')
    print(cosmetic.raw_data)

    cosmetics = client.search_cosmetic(multiple=True, id='CID_298_Athena_Commando_F_IceMaiden')
    print([e.raw_data for e in cosmetics])

    aes = client.fetch_aes()
    print(aes.raw_data)

    banners = client.fetch_banners()
    print(len(banners))

    banner_colors = client.fetch_banner_colors()
    print(len(banner_colors))

    code = client.fetch_creator_code('Ninja')
    print(code.raw_data)

    fortnite_map = client.fetch_map()
    print(fortnite_map.raw_data)

    user = client.fetch_br_stats('Luc1412')
    print(user)
