Migrating
=========

The change from Version 2.x.x of the library (dubbed as "Version 2" from here on out) to Version 3 is a major change. But don't worry, we've got 
you covered. This document will help you migrate your code from the old version of the FortniteAPI Python
wrapper to the new version, and in doing so, help you understand the changes that have been made.

The documentation is key to understanding the changes that have been made. It's highly recommended that, after
reading this, you skim through all the methods on the :class:`fortnite_api.FortniteAPI` and :class:`fortnite_api.SyncFortniteAPI` classes to understand the changes that have been made.

Client 
------
Before we dive into the specifics of the changes, it's important to understand the general changes that have been made 
to the client. The client is your main interface between your code and the Fortnite API. It is the single, most important
object in this library. In Version 2, the client was a class that held all different types of endpoints as attributes.

.. outdated-code-block:: python3
    :since: v2.6.6

    from fortnite_api import FortniteAPI

    client = FortniteAPI(api_key='', run_async=False)
    client.cosmetics.fetch()
    client.playlist.fetch_all()

This is no longer the case in Version 3. In Version 3, the client is a class that holds all different types of endpoints as methods. Keep this in mind as you read through the changes that have been made. Version 3 of the library has been
rebuilt from the ground up to be more intuitive, more consistent, and more powerful.

Great, let's dive into how creating a client has changed.

Async and Sync Specific Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In Version 2, you could specify whether you wanted to use the client in an async or sync manner by passing a 
``run_async`` parameter to the client. In Version 3, the :class:`fortnite_api.FortniteAPI` client only has async
functions. Don't worry though, all synchronous functionality has been extended into the 
:class:`fortnite_api.SyncFortniteAPI` class with exactly the same interface as its async counterpart.

Creating the client
~~~~~~~~~~~~~~~~~~~
In Version 3, you choose which instance of client to use based on whether you want to use async methods
or sync methods. Now, creating an instance of the client should be done as follows:

Async Client
^^^^^^^^^^^^
To create an async client, you use the :class:`fortnite_api.FortniteAPI` class. This class is used to make async requests to the Fortnite API.

.. code-block:: python3

    from fortnite_api import FortniteAPI
    import asyncio

    async def main():
        async with FortniteAPI(api_key='') as client:
            ... 
    
    asyncio.run(main())

Sync client
^^^^^^^^^^^
To create a sync client, you use the :class:`fortnite_api.SyncFortniteAPI` class. This class is used to make synchronous requests to the Fortnite API.

.. code-block:: python3

    from fortnite_api import SyncFortniteAPI

    with SyncFortniteAPI(api_key='') as client:
        ...

Client context managers
~~~~~~~~~~~~~~~~~~~~~~~
Both clients in Version 3 are run with context managers. Running ``async with``/``with`` ensures that the 
HTTP session is closed properly when the context manager is exited, it's a good practice to use them.

Although it is recommended you use the built in context managers, it is not strictly required. 
You are completely free to use both clients without the context manager if you choose. In that case, however, 
you are in the driver's seat, and must be in charge of managing the HTTP session. Thus, it's your 
responsibility to pass it to the client and close it when you're done with it.

Async client without context manager
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When using the async client without the context manager, you must pass the session to the client and close it yourself.

.. code-block:: python3

    from fortnite_api import FortniteAPI
    import asyncio

    async def main():
        session = aiohttp.ClientSession()
        client = FortniteAPI(api_key='', session=session)    
        ...
        
        await session.close()

    asyncio.run(main())

Sync client without context manager
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When using the sync client without the context manager, you must pass the session to the client and close it yourself.

.. code-block:: python3

    from fortnite_api import SyncFortniteAPI
    import requests

    session = requests.Session()
    client = SyncFortniteAPI(api_key='', session=session)    
    ...

    session.close()

Client parameters
~~~~~~~~~~~~~~~~~
In Version 3, the parameters that can be passed to a client have been given a refresh. Let's walk through the changes
that have been made for both the async and sync clients, what they mean, and how they affect you.

Although all these parameters are documented on their respective client classes, we're going to reiterate 
and elaborate on them here to help you understand the important changes that have been made.

Async client
^^^^^^^^^^^^
.. list-table::
    :header-rows: 1

    *   - Parameter
        - Description
    *   - ``api_key``
        - The API key to use for requests to the Fortnite API. This is not a required parameter for most endpoints however, it is required to use any stats endpoints. This is the same as in Version 2. 
    *   - ``default_language``
        - The client now boasts a default language parameter. For many endpoints in the Fortnite API, you can specify a language parameter to denote the language you want the response to be in. This parameter allows you to set a default language for all requests made by the client, for endpoints that support it, so that you don't have to specify it every time you make a request. The default language is :attr:`~fortnite_api.GameLanguage.ENGLISH` (``en``). 
    *   - ``session``
        - The session parameter is a new parameter that allows you to pass a :class:`aiohttp.ClientSession` to the client. By default this is an optional parameter. This parameter comes in useful if you want to manage a session yourself. In that case, it is a required parameter.
    *   - ``beta``
        - Denotes if the client has the permissions to access beta endpoints (always prefixed with ``beta_fetch_x``). This is a new parameter that is set to ``False`` by default. If you want to access beta endpoints, you must set this parameter to ``True``.
    *   - ``optimization_flags``
        - This is a new parameter that allows you to toggle certain optimizations on or off. This parameter is not required, and defaults to :meth:`~fortnite_api.OptimizationFlags.default` if not given. 

See the documentation for these parameters in :class:`fortnite_api.FortniteAPI`.

Sync client
^^^^^^^^^^^
.. list-table::
    :header-rows: 1

    *   - Parameter
        - Description
    *   - ``api_key``
        - The API key to use for requests to the Fortnite API. This is not a required parameter for most endpoints however, it is required to use any stats endpoints. This is the same as in Version 2. 
    *   - ``default_language``
        - The client now boasts a default language parameter. For many endpoints in the Fortnite API, you can specify a language parameter to denote the language you want the response to be in. This parameter allows you to set a default language for all requests made by the client, for endpoints that support it, so that you don't have to specify it every time you make a request. The default language is :attr:`~fortnite_api.GameLanguage.ENGLISH` (``en``). 
    *   - ``session``
        - The session parameter is a new parameter that allows you to pass a :class:`requests.Session` to the client. By default this is an optional parameter. This parameter comes in useful if you want to manage a session yourself. In that case, it is a required parameter.
    *   - ``beta``
        - Denotes if the client has the permissions to access beta endpoints (always prefixed with ``beta_fetch_x``). This is a new parameter that is set to ``False`` by default. If you want to access beta endpoints, you must set this parameter to ``True``.
    *   - ``optimization_flags``
        - This is a new parameter that allows you to toggle certain optimizations on or off. This parameter is not required, and defaults to :meth:`~fortnite_api.OptimizationFlags.default` if not given. 

See the documentation for these parameters in :class:`fortnite_api.SyncFortniteAPI`.

Cosmetics
---------

Cosmetic objects
~~~~~~~~~~~~~~~~
The naming convention for cosmetic objects have been refactored. Anything related to cosmetics
has been prefixed with ``CosmeticX``. A complete mapping of this change is as follows:

.. list-table:: 
    :header-rows: 1

    *   - Old Name
        - New Name
    *   - ``Cosmetic`` 
        - :class:`fortnite_api.Cosmetic`
    *   - ``BrCosmetic``
        - :class:`fortnite_api.CosmeticBr`
    *   - ``BrCosmeticVariant``
        - :class:`fortnite_api.CosmeticBrVariant`
    *   - ``BrCosmeticVariantOption``
        - :class:`fortnite_api.CosmeticBrVariantOption`
    *   - ``CarCosmetic``
        - :class:`fortnite_api.CosmeticCar`
    *   - ``InstrumentCosmetic``
        - :class:`fortnite_api.CosmeticInstrument`
    *   - ``LegoKitCosmetic``
        - :class:`fortnite_api.CosmeticLegoKit`
    *   - ``LegoCosmeticVariant``
        - :class:`fortnite_api.CosmeticLego`
    *   - ``JamTrack``
        - :class:`fortnite_api.CosmeticTrack`
    *   - ``CosmeticImage``
        - Does not exist anymore. The closest replacement is :class:`fortnite_api.Asset`, which is discussed more below.

Additionally, many new Cosmetic related objects have been added to the library. These include:

- :class:`fortnite_api.CosmeticBrIntroduction`
- :class:`fortnite_api.CosmeticBrRarity`
- :class:`fortnite_api.CosmeticBrSet`
- :class:`fortnite_api.CosmeticBrType`
- :class:`fortnite_api.CosmeticTrackDifficulty`
- :class:`fortnite_api.CosmeticLegoImages`
- :class:`fortnite_api.CosmeticImages`
- :class:`fortnite_api.CosmeticSeries`
- :class:`fortnite_api.CosmeticRarity`
- :class:`fortnite_api.CosmeticTypeInfo`
- :clasS:`fortnite_api.CosmeticCompatibleMode`

As the amount of Fortnite cosmetics grows overtime, this ensures a consistent naming 
convention between all cosmetic objects.

Fetching Cosmetics
~~~~~~~~~~~~~~~~~~~
Version 2 previously held all cosmetic endpoints under the ``client.cosmetics`` namespace. 
In Version 3, this is not the case. Instead, all cosmetic endpoints, as well as all endpoints, are now methods of 
the client itself. This means that to fetch cosmetics, you no longer need to do:

.. outdated-code-block:: python3
    :since: v2.6.6

    cosmetics = await client.cosmetics.fetch()
    reveal_type(cosmetics)
    >>> List[fortnite_api.Cosmetic]

But rather, you do:

.. code-block:: python3
    :name: version-3-fetching-cosmetics

    cosmetics = await client.fetch_cosmetics_all()
    reveal_type(cosmetics)
    >>> fortnite_api.CosmeticsAll

This change has been made to ensure a consistent naming convention between all types of endpoints,
and to make the library more intuitive to use. 

Fetching Cosmetics Method Changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A complete mapping of the old methods and their new counterparts
are as follows:

.. list-table:: 
    :header-rows: 1

    *   - Old Method
        - New Method
    *   - ``client.cosmetics.fetch()`` 
        - :meth:`fortnite_api.FortniteAPI.fetch_cosmetics_all`
    *   - ``client.cosmetics.fetch_br()``
        - :meth:`fortnite_api.FortniteAPI.fetch_cosmetics_br`
    *   - ``client.cosmetics.fetch_cars()``
        - :meth:`fortnite_api.FortniteAPI.fetch_cosmetics_cars`
    *   - ``client.cosmetics.fetch_instruments()``
        - :meth:`fortnite_api.FortniteAPI.fetch_cosmetics_instruments`
    *   - ``client.cosmetics.fetch_lego_kits()``
        - :meth:`fortnite_api.FortniteAPI.fetch_cosmetics_lego_kits`
    *   - ``client.cosmetics.fetch_jam_tracks()``
        - :meth:`fortnite_api.FortniteAPI.fetch_cosmetics_tracks`
    *   - ``client.cosmetics.fetch_lego_variants()``
        - :meth:`fortnite_api.FortniteAPI.fetch_cosmetics_lego`
    *   - ``client.cosmetics.fetch_all_new()``
        - :meth:`fortnite_api.FortniteAPI.fetch_cosmetics_new`
    *   - ``client.cosmetics.fetch_new_br()``
        - :meth:`fortnite_api.FortniteAPI.fetch_cosmetics_br_new`
    *   - ``client.cosmetics.search_all``
        - :meth:`fortnite_api.FortniteAPI.search_br_cosmetics`
    *   - ``client.cosmetics.search_first``
        - :meth:`fortnite_api.FortniteAPI.search_br_cosmetics`

Of course, the same applies to the SyncFortniteAPI client. The methods are the same, but they are synchronous and 
under the :class:`fortnite_api.SyncFortniteAPI` client instead.


Playlists
---------
Playlist objects
~~~~~~~~~~~~~~~~
In Version 3, playlist objects remain mostly the same as they were in Version 2. A mapping of the old playlist 
objects to the new playlist objects is as follows:

.. list-table::
    :header-rows: 1

    *   - Old Name
        - New Name
    *   - ``Playlist``
        - :class:`fortnite_api.Playlist`


Additionally, a new playlist object has been added to the library:

- :class:`fortnite_api.PlaylistImages`: This object represents the images of a playlist, if available. In Version 2, this information used to be wrapped in the :class:`fortnite_api.Playlist` object itself, however, it has been separated into its own object in Version 3.

Fetching Playlists
~~~~~~~~~~~~~~~~~~

In Version 2, all playlist endpoints were contained under the ``client.playlist`` namespace. 
In Version 3, this is not the case. Rather, the playlist endpoints are now methods of the client itself.
Previously, you could fetch the playlists using,

.. outdated-code-block:: python3
    :since: v2.6.6
    
    import fortnite_api

    client = fortnite_api.FortniteAPI(api_key='', run_async=False)
    playlists = client.playlist.fetch_all()
    reveal_type(playlists)
    >>> List[fortnite_api.Playlist]

This approach, however, is no longer valid in Version 3. Instead, you should use direct methods on the client.

.. code-block:: python3
    :name: version-3-fetching-playlists

    playlists = await client.fetch_playlists()
    reveal_type(playlists)
    >>> List[fortnite_api.Playlist]

Playlist Method Changes
^^^^^^^^^^^^^^^^^^^^^^^
A complete mapping of the old methods and their new counterparts are as follows:

.. list-table::
    :header-rows: 1

    *   - Old Method
        - New Method
    *   - ``client.playlist.fetch_all()``
        - :meth:`fortnite_api.FortniteAPI.fetch_playlists`
    *   - ``client.playlist.fetch_by_id()``
        - :meth:`fortnite_api.FortniteAPI.fetch_playlist`

Of course, the same applies to the SyncFortniteAPI client. The methods are the same, but they are synchronous and
under the :class:`fortnite_api.SyncFortniteAPI` client instead.

Shop
----
Shop Objects
~~~~~~~~~~~~
Although the names of shop objects have changed, a majority of the shop functionality remains the same. A mapping of the old 
shop objects to the new shop objects is as follows:

.. list-table::
    :header-rows: 1

    *   - Old Name
        - New Name
    *   - ``Shop``
        - :class:`fortnite_api.Shop`
    *   - ``ShopEntry``
        - :class:`fortnite_api.ShopEntry`
    *   - ``ShopBundle``
        - :class:`fortnite_api.ShopEntryBundle`
    *   - ``ShopBanner``
        - :class:`fortnite_api.ShopEntryBanner`
    *   - ``ShopLayout``
        - :class:`fortnite_api.ShopEntryLayout`
    *   - ``ShopNewDisplayAsset``
        - :class:`fortnite_api.ShopEntryNewDisplayAsset`
    *   - ``ShopMaterialInstance``
        - Depreciated, moved to a more generic :class:`fortnite_api.MaterialInstance` class for the material instance endpoints. More on this later.
    *   - ``ShopMaterialInstanceImages``
        - Depreciated, moved to more generic :class:`fortnite_api.MaterialInstanceImages` class for material instances. More on this later.
    *   - ``BrShop``
        - Depreciated.
    *   - ``BrShopSection``
        - Depreciated.
    *   - ``BrShopEntry``
        - Depreciated.
    *   - ``BrShopBundle``
        - Depreciated.
    *   - ``BrShopBanner``
        - Depreciated.
    *   - ``BrShopSectionNew``
        - Depreciated.
    *   - ``BrShopLayout``
        - Depreciated.
    *   - ``BrShopNewDisplayAsset``
        - Depreciated.
    *   - ``BrShopMaterialInstance``
        - Depreciated.
    
As you can see, the `BrShop` objects have been depreciated in Version 3. This is because that endpoint has been depreciated. The current implementation shows the shop as a whole, rather than specifically for Battle Royale.

Fetching Shop Data
~~~~~~~~~~~~~~~~~~
In Version 3, the shop data is longer fetched using the ``client.shop`` namespace. Previously, you could fetch the shop data using,

.. outdated-code-block:: python3
    :since: v2.6.6

    import fortnite_api

    client = fortnite_api.FortniteAPI(api_key='', run_async=False)
    shop = client.shop.fetch_all()

This approach, however, is no longer valid in Version 3. Instead, you should use direct methods on the client. 

Shop Method Changes
^^^^^^^^^^^^^^^^^^^
A complete mapping of the old methods and their new counterparts are as follows:

.. list-table::
    :header-rows: 1

    *   - Old Method
        - New Method
    *   - ``client.shop.fetch_all()``
        - :meth:`fortnite_api.FortniteAPI.fetch_shop`
    *   - ``client.shop.fetch_br()``
        - Depreciated.
    *   - ``client.shop.fetch()``
        - Depreciated. ``client.shop.fetch()`` was an alias to ``fetch_br``, which has been depreciated.

Of course, the same applies to the SyncFortniteAPI client. The methods are the same, but they are synchronous and
under the :class:`fortnite_api.SyncFortniteAPI` client instead.


Aes
---
Aes Objects
~~~~~~~~~~~
The AES objects remain almost identical to as they were in Version 2. A mapping of the old AES objects to the new AES objects is as follows:

.. list-table::
    :header-rows: 1

    *   - Old Name
        - New Name
    *   - ``AES``
        - :class:`fortnite_api.Aes`
    *   - ``DynamicKey``
        - :class:`fortnite_api.DynamicKey`

Additionally, a new object relating to :class:`~fortnite_api.Aes` information has been added. This is,

- :class:`fortnite_api.Version`: Represents a version of a build in Fortnite. Holds the major and minor version of the build.

Fetching Aes Data
~~~~~~~~~~~~~~~~~
In Version 3, the AES data is no longer fetched using the ``client.aes`` namespace. Previously, you could fetch the AES data using,

.. outdated-code-block:: python3
    :since: v2.6.6

    import fortnite_api

    client = fortnite_api.FortniteAPI(api_key='', run_async=False)
    client.aes.fetch()

This approach, however, is no longer valid in Version 3. Instead, you should use direct methods on the client.

AES Method Changes
^^^^^^^^^^^^^^^^^^
A complete mapping of the old methods and their new counterparts are as follows:

.. list-table::
    :header-rows: 1

    *   - Old Method
        - New Method
    *   - ``client.aes.fetch()``
        - :meth:`fortnite_api.FortniteAPI.fetch_aes`

Of course, the same applies to the SyncFortniteAPI client. The methods are the same, but they are synchronous and
under the :class:`fortnite_api.SyncFortniteAPI` client instead.

So, fetching the AES data in Version 3 can be done as follows:

.. code-block:: python3
    
    client = fortnite_api.SyncFortniteAPI()
    aes = client.fetch_aes()
    reveal_type(aes)
    >>> fortnite_api.Aes

News 
----
News objects 
~~~~~~~~~~~~
News objects remain the same in Version 3, with no significant changes made to them. A mapping of the old news objects to the new news objects is as follows:

.. list-table::
    :header-rows: 1
    *   - Old Name
        - New Name
    *   - ``News``
        - :class:`fortnite_api.News`
    *   - ``GameModeNews``
        - :class:`fortnite_api.GameModeNews`
    *   - ``NewsMotd``
        - :class:`fortnite_api.NewsMotd`
    *   - ``NewsMessage``
        - :class:`fortnite_api.NewsMessage`

Fetching News Data
~~~~~~~~~~~~~~~~~~
In Version 2, the news data was fetched using the ``client.news`` namespace. Previously, you could fetch the news data using,

.. outdated-code-block:: python3
    :since: v2.6.6

    import fortnite_api

    client = fortnite_api.FortniteAPI(api_key='', run_async=False)
    news = client.news.fetch()
    reveal_type(news)
    >>> fortnite_api.News

However, this approach is no longer valid in Version 3. Instead, you should use direct methods on the client.

News Method Changes
^^^^^^^^^^^^^^^^^^
A complete mapping of the old methods and their new counterparts are as follows:

.. list-table::
    :header-rows: 1

    *   - Old Method
        - New Method
    *   - ``client.news.fetch()``
        - :meth:`fortnite_api.FortniteAPI.fetch_news`
    *   - ``client.news.fetch_by_type()``
        - Fetching by type has been depreciated. Rather, use these two methods: :meth:`fortnite_api.FortniteAPI.fetch_news_br`, and :meth:`fortnite_api.FortniteAPI.fetch_news_stw`


Of course, the same applies to the SyncFortniteAPI client. The methods are the same, but they are synchronous and
under the :class:`fortnite_api.SyncFortniteAPI` client instead.

Now, fetching the news data in Version 3 can be done as follows:

.. code-block:: python3

    async with fortnite_api.FortniteAPI(api_key='') as client:
        news = await client.fetch_news()
        reveal_type(news)
        >>> fortnite_api.News


Creator Code 
------------
.. Changes to the creator code endpoint

BR Stats
--------
.. Changes to the BR Stats endpoint

Banners 
-------
.. Changes to the banners endpoint

Map 
----
.. Changes to the map endpoint

Changelog
---------

.. Changelog for each endpoint difference. The general model between how requests used to 
