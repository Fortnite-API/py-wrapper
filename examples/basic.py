# This example introduces you to the basic usage of the FortniteAPI client in an asynchronous context.
# It will familiarize you with the client and how to use it to fetch data from the Fortnite API.

import asyncio

import fortnite_api


async def main():
    # The main way you interact with the API is through the main client.
    # This client uses an aiohttp ClientSession for its HTTP requests, so
    # it's recommended to use the client with an async context manager.
    async with fortnite_api.FortniteAPI(api_key='YOUR_API_KEY') as client:

        # The client has many methods to get cosmetics, news,
        # and other data from the API. Every method that fetches
        # data from the API is a coroutine, so you must await the result.
        cosmetics = await client.fetch_cosmetics_all()

        # In this case, fetch_cosmetics_all returns an instance of "fortnite_api.CosmeticsAll"

        assert isinstance(cosmetics, fortnite_api.CosmeticsAll)

        # We can iterate through the BR (battle royale) cosmetics and print out all their IDS.
        for cosmetic in cosmetics.br:
            print(cosmetic.id)

    # After the context manager, our client is closed and the
    # session is closed. If you choose to use the client without
    # the context manager, you must be sure to close the session yourself.


asyncio.run(main())
