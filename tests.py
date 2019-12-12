import asyncio

import fortnite_api

api_key = 'ac54ca08e4715a72da4ee30eaf9086ef0c89bcbe32e7cc23fd3dee0c1ec82e32'


def sync_test():
    fn = fortnite_api.FortniteAPI(api_key)
    print(fn.shop.fetch())
    print([[i.name, i.type.value] for i in fn.cosmetics.search_all(name='Drift')])
    print(fn.cosmetics.search_first(name='Drift').id)
    print(fn.creator_code.search_first('EasyFnStats').user.name)


async def async_test():
    fn = fortnite_api.FortniteAPI(api_key, run_async=True)
    print(await fn.shop.fetch())
    print([[i.name, i.type.value] for i in (await fn.cosmetics.search_all(name='Drift'))])
    print((await fn.cosmetics.search_first(name='Drift')).id)
    print((await fn.creator_code.search_first('EasyFnStats')).user.name)

if __name__ == '__main__':
    print('------ Sync Tests ------')
    sync_test()
    loop = asyncio.get_event_loop()
    print('------ Async Tests ------')
    loop.run_until_complete(async_test())
