"""
This example introduces you to the basic usage of the Client in a synchronous context.
It familiarizes you with the SyncClient and how to use it to fetch data from the Fortnite API.

Any asynchronous code in this example directory can be converted to synchronous code simply
by changing the client definition and removing all async/await keywords. The library ensures
that the interfaces are the same for both synchronous and asynchronous contexts.
"""

import fortnite_api


def main():
    # The main way you interact with the API is through the main client.
    # This client uses an requests Session for its HTTP requests, so
    # it's recommended to use the client with an async context manager.
    with fortnite_api.SyncClient(api_key='YOUR_API_KEY') as client:

        # The client has many methods to get cosmetics, news,
        # and other data from the API. Every method that fetches
        # data from the API is an API call, so you may want to keep
        # these calls limited to only when you need them.
        cosmetics = client.fetch_cosmetics_all()

        # In this case, fetch_cosmetics_all returns an instance of "fortnite_api.CosmeticsAll"

        assert isinstance(cosmetics, fortnite_api.CosmeticsAll)

        # We can iterate through the BR (battle royale) cosmetics and print out all their IDS.
        for cosmetic in cosmetics.br:
            print(cosmetic.id)

    # After the context manager, our client is closed and the
    # session is closed. If you choose to use the client without
    # the context manager, you must be sure to close the session yourself.


main()
