import asyncio

import fortnite_api

api_key = ''


def sync_test():
    fn = fortnite_api.FortniteAPI()
    print(fn.shop.fetch(combined=True))
    print([[i.name, i.type.value] for i in fn.cosmetics.search_all(name='Drift')])
    print(fn.cosmetics.search_first(name='Drift').id)
    print(fn.creator_code.search_first('GetOnMyLvl').user.name)
    print(fn.news.fetch())
    print(fn.aes.fetch())
    print(fn.stats.fetch_by_name('Luc1412'))


async def async_test():
    fn = fortnite_api.FortniteAPI(run_async=True)
    print(await fn.shop.fetch(combined=True))
    print([[i.name, i.type.value] for i in (await fn.cosmetics.search_all(unseen_for=800))])
    print((await fn.cosmetics.search_first(name='Drift')).id)
    print((await fn.creator_code.search_first('GetOnMyLvl')).user.name)
    print(await fn.news.fetch())
    print(await fn.aes.fetch())
    print(await fn.stats.fetch_by_name('Luc1412'))


if __name__ == '__main__':
    print('------ Sync Tests ------')
    sync_test()
    loop = asyncio.get_event_loop()
    print('------ Async Tests ------')
    loop.run_until_complete(async_test())
