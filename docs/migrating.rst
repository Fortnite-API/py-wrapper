.. _migrating:

Migrating
=========

The change from Version 2.x.x of the library (dubbed as "Version 2" from here on out) to Version 3 is a major change.
Version 3 of the library has been rebuilt from the ground up to be more intuitive, more consistent, and more powerful. 

Don't worry though, we've got you covered. This document will help you migrate your code from the old version of the FortniteAPI Python
wrapper to the new version, and in doing so, help you understand the changes that have been made.

The documentation is key to understanding the changes that have been made. As you get reworking your code, you must work
hand in hand with the documentation to ensure a smooth transition. 

*Any objects not touched upon in a specific section of this document are mentioned in* :ref:`the Additional Objects section <migrating-additional-objects>` *at the bottom.*

Client 
------
Before we dive into the specifics of the changes, it's important to understand the general changes that have been made 
to the client. The client is your main interface between your code and the Fortnite API. It is the single, most important
object in this library. In Version 2, the client held all available endpoints in specific ``namespaces``. For example,

.. outdated-code-block:: python3
    :since: v2.6.6

    client = fortnite_api.FortniteAPI(api_key='', run_async=False)

    # All cosmetics endpoints are available under "client.cosmetics"
    client.cosmetics.fetch()

    # All playlist endpoints are available under "client.playlist"
    client.playlist.fetch_all()

The namespaces approach created obtuse code that was difficult to maintain, type-hint, and understand.

In Version 3, however, the client now holds all available endpoints as direct methods.
So for example, after creating an instance of the client, you simply call the methods directly on the client itself: 

.. code-block:: python3

    # "with" discussed later, don't worry about it for now
    with fortnite_api.SyncClient() as client:
        # Method to fetch all cosmetics
        client.fetch_cosmetics_all()

        # Method to fetch all playlists
        client.fetch_playlists()

Notice the ``with`` statement? We'll touch on that in :ref:`creating-the-client`. 

The biggest key takeaway here is that
the client now holds all available endpoints as direct methods. This makes the library more intuitive to use, and easier to maintain.

Async and Sync Specific Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In Version 2, you could specify whether you wanted to use the client in an async or sync manner by passing a 
``run_async`` parameter to the client. In Version 3, the :class:`fortnite_api.Client` client only has async
functions. Don't worry though, all synchronous functionality has been extended into the 
:class:`fortnite_api.SyncClient` class with exactly the same interface as its async counterpart.

.. _creating-the-client:

Creating the Client
~~~~~~~~~~~~~~~~~~~
In Version 3, you choose which instance of client to use based on whether you want to use async methods
or sync methods. Now, creating an instance of the client should be done as follows:

Async client
^^^^^^^^^^^^
To create an async client, you use the :class:`fortnite_api.Client` class. This class is used to make async requests to the Fortnite API.

.. code-block:: python3

    import asyncio

    async def main():
        async with fortnite_api.Client(api_key='') as client:
            ... 
    
    asyncio.run(main())

Sync client
^^^^^^^^^^^
To create a sync client, you use the :class:`fortnite_api.SyncClient` class. This class is used to make synchronous requests to the Fortnite API.

.. code-block:: python3

    with fortnite_api.SyncClient(api_key='') as client:
        ...

.. _client-context-managers:

Client Context Managers
~~~~~~~~~~~~~~~~~~~~~~~
Both clients in Version 3 are run with context managers. This transition boasts many benefits, most notably,

- Ensures that the HTTP session is closed properly when the context manager is exited, regardless of an exception being raised,
- Makes the client more intuitive to use, and
- Removes redundant boilerplate code.

Thus, when creating and using an instance of the client, it is recommended that you use the built in context managers and include all your API requests within the context manager. This ensures that the session is closed properly when you're done with it.

.. code-block:: python3

    async with fortnite_api.Client(api_key='') as client: # Session created
        print('Client session is open for requests.')
        ... # Some operations with the client
        
    print('Session is closed automatically.')

.. code-block:: python3

    with fortnite_api.SyncClient(api_key='') as client: # Session created
        print('Client session is open for requests.')
        ... # Some operations with the client

    print('Session is closed automatically.')

Although it is recommended you use the built in context managers, there may be a situation in which it is not possible. Don't worry, you are free to use both clients without the context manager if you choose. In that case, however, 
you are in the driver's seat, and must be in charge of managing the HTTP session, ie. close the session when you're done with it.

Async client without context manager
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When using the async client without the context manager, you must pass the session to the client and close it yourself.

.. code-block:: python3

    import asyncio

    async def main():
        session = aiohttp.ClientSession()
        client = fortnite_api.Client(api_key='', session=session)    
        ...
        
        await session.close()

    asyncio.run(main())

Sync client without context manager
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When using the sync client without the context manager, you must pass the session to the client and close it yourself.

.. code-block:: python3

    import requests

    session = requests.Session()
    client = fortnite_api.SyncClient(api_key='', session=session)    
    ...

    session.close()

Client Parameters
~~~~~~~~~~~~~~~~~
In Version 3, the parameters that can be passed to a client have been given a refresh. Let's walk through the changes
that have been made for both the async and sync clients, what they mean, and how they affect you. Note that all the 
parameters, except for the ``session`` parameter, are the same on both clients. We'll discuss the ``session`` parameter
separately for both clients in the next section.

.. list-table::
    :header-rows: 1

    *   - Parameter
        - Description
    *   - ``api_key``
        - The API key to use for requests to the Fortnite API. This is not a required parameter for most endpoints however, it is required to use any stats endpoints. This is the same as in Version 2. 
    *   - ``default_language``
        - The client now boasts a default language parameter. For many endpoints in the Fortnite API, you can specify a language parameter to denote the language you want the response to be in. This parameter allows you to set a default language for all requests made by the client, for endpoints that support it, so that you don't have to specify it every time you make a request. The default language is :attr:`~fortnite_api.GameLanguage.ENGLISH` (``en``). 
    *   - ``session``
        - The session parameter accepts an HTTP session into the client. By default this is an optional parameter. This parameter comes in useful if you want to manage a session yourself. In that case, it is a required parameter. This is different in the :class:`fortnite_api.Client` and :class:`fortnite_api.SyncClient` - so what is the difference? Below will discuss the differences between the two clients' initialization parameters.
    *   - ``beta``
        - Denotes if the client has the permissions to access beta endpoints (always prefixed with ``beta_fetch_x``). This is a new parameter that is set to ``False`` by default. If you want to access beta endpoints, you must set this parameter to ``True``.
    *   - ``response_flags``
        - Denotes the response flags that the client should attach to its requests to the Fortnite API. This is a new parameter that is set to :attr:`~fortnite_api.ResponseFlags.INCLUDE_NOTHING` by default. It is **highly recommended** you read through the :ref:`response flags section <response_flags>` to understand how to use this parameter effectively, which flags are available, and where they affect the responses from the Fortnite API.

See the documentation for these parameters in :class:`fortnite_api.Client` and :class:`fortnite_api.SyncClient`.

Async client specific initialization parameter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Denotes the only parameter difference between the async and sync clients.

.. list-table::
    :header-rows: 1

    *   - Parameter
        - Description

    *   - ``session``
        - The session parameter is a new parameter that allows you to pass a :class:`aiohttp.ClientSession` to the client. By default this is an optional parameter. This parameter comes in useful if you want to manage a session yourself. In that case, it is a required parameter.

See the documentation for these parameters in :class:`fortnite_api.Client`.

Sync client specific initialization parameter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Denotes the only parameter difference between the sync and async clients.

.. list-table::
    :header-rows: 1

    *   - Parameter
        - Description
    *   - ``session``
        - The session parameter is a new parameter that allows you to pass a :class:`requests.Session` to the client. By default this is an optional parameter. This parameter comes in useful if you want to manage a session yourself. In that case, it is a required parameter.

See the documentation for these parameters in :class:`fortnite_api.SyncClient`.

End of Client Introduction
~~~~~~~~~~~~~~~~~~~~~~~~~~
Welcome to the end of the introduction to the new Version 3 changes. You now have a solid understanding of the changes that have been made to the client, and how to create and use the client. The next sections will dive into the specifics of the changes that have been made to the library. Below is more of the "nitty gritty" of the changes that have been made, and choose to focus more on method renaming, object renaming, new objects, and any other small details that differ from Version 2 of the library.  

It is recommended to read through the entire document to get a full understanding of the changes that have been made. However, if you are looking for a specific section, you can use the table of contents below to navigate to that section.

Cosmetics
---------
One of the biggest elements of the library, Fortnite Cosmetics. These endpoints, classes, and 
methods have been refactored to be more consistent, more intuitive, and more powerful. Let's dive into the specifics of the changes that have been made.

Cosmetic Objects
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
    *   - ``LegoCosmetic``
        - :class:`fortnite_api.VariantLego`
    *   - ``JamTrack``
        - :class:`fortnite_api.CosmeticTrack`
    *   - ``CosmeticImage``
        - Does not exist anymore. The closest replacement is :class:`fortnite_api.Asset`, which is discussed more below.

Additionally, many new Cosmetic related objects have been added to the library. These include:

- :class:`fortnite_api.CosmeticBrIntroduction`
- :class:`fortnite_api.CosmeticRarity`
- :class:`fortnite_api.CosmeticBrSet`
- :class:`fortnite_api.CosmeticType`
- :class:`fortnite_api.CosmeticTrackDifficulty`
- :class:`fortnite_api.CosmeticImages`
- :class:`fortnite_api.CosmeticSeriesInfo`
- :class:`fortnite_api.CosmeticRarityInfo`
- :class:`fortnite_api.CosmeticTypeInfo`
- :class:`fortnite_api.CosmeticCompatibleMode`
- :class:`fortnite_api.VariantBean`

This may seem like a lot, but don't worry, the documentation has got you covered! As you get working with methods to fetch this data, a lot of these objects will be second hand to you.

Fetching Cosmetics
~~~~~~~~~~~~~~~~~~~
Version 2 previously held all cosmetic endpoints under the ``client.cosmetics`` namespace. 
In Version 3, this is not the case. Instead, all cosmetic endpoints, as well as all endpoints, are now methods of 
the client itself. This means that to fetch cosmetics, you no longer do:

.. outdated-code-block:: python3
    :since: v2.6.6

    cosmetics = await client.cosmetics.fetch()
    print(cosmetics)
    >>> [<fortnite_api.Cosmetic ...>, ...]

But rather, you do:

.. code-block:: python3
    :name: version-3-fetching-cosmetics

    cosmetics = await client.fetch_cosmetics_all()
    print(cosmetics)
    >>> <fortnite_api.CosmeticsAll ...>

This change has been made to ensure a consistent naming convention between all types of endpoints,
and to make the library more intuitive to use. 

Fetching cosmetics method changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A complete mapping of the old methods and their new counterparts
are as follows:

.. list-table:: 
    :header-rows: 1

    *   - Old Method
        - New Method
    *   - ``client.cosmetics.fetch()`` 
        - :meth:`fortnite_api.Client.fetch_cosmetics_all`
    *   - ``client.cosmetics.fetch_br()``
        - :meth:`fortnite_api.Client.fetch_cosmetics_br`
    *   - ``client.cosmetics.fetch_cars()``
        - :meth:`fortnite_api.Client.fetch_cosmetics_cars`
    *   - ``client.cosmetics.fetch_instruments()``
        - :meth:`fortnite_api.Client.fetch_cosmetics_instruments`
    *   - ``client.cosmetics.fetch_lego_kits()``
        - :meth:`fortnite_api.Client.fetch_cosmetics_lego_kits`
    *   - ``client.cosmetics.fetch_jam_tracks()``
        - :meth:`fortnite_api.Client.fetch_cosmetics_tracks`
    *   - ``client.cosmetics.fetch_lego_variants()``
        - :meth:`fortnite_api.Client.fetch_variants_lego`
    *   - ``client.cosmetics.fetch_all_new()``
        - :meth:`fortnite_api.Client.fetch_cosmetics_new`
    *   - ``client.cosmetics.fetch_new_br()``
        - This method has been depreciated. Use :meth:`fortnite_api.Client.fetch_cosmetics_new` instead.
    *   - ``client.cosmetics.search_all()``
        - :meth:`fortnite_api.Client.search_br_cosmetics`
    *   - ``client.cosmetics.search_first()``
        - :meth:`fortnite_api.Client.search_br_cosmetics`

Of course, the same applies to the SyncClient client. The methods are the same, but they are synchronous and 
under the :class:`fortnite_api.SyncClient` client instead.


Playlists
---------
Playlist Objects
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

- :class:`fortnite_api.PlaylistImages`: This object represents the images of a playlist, if available. In Version 2, this information used to be wrapped in the :class:`fortnite_api.Playlist` object itself, but this has been separated.

Fetching Playlists
~~~~~~~~~~~~~~~~~~
In Version 2, all playlist endpoints were contained under the ``client.playlist`` namespace. 
In Version 3, this is not the case. Rather, the playlist endpoints are now methods of the client itself.
Previously, you could fetch the playlists using,

.. outdated-code-block:: python3
    :since: v2.6.6

    playlists = await client.playlist.fetch_all()
    print(playlists)
    >>> [<fortnite_api.Playlist ...>, ...]

This approach, however, is no longer valid in Version 3. Instead, you should use direct methods on the client.

.. code-block:: python3
    :name: version-3-fetching-playlists

    playlists = await client.fetch_playlists()
    print(playlists)
    >>> [<fortnite_api.Playlist ...>, ...]

Playlist method changes
^^^^^^^^^^^^^^^^^^^^^^^
A complete mapping of the old methods and their new counterparts are as follows:

.. list-table::
    :header-rows: 1

    *   - Old Method
        - New Method
    *   - ``client.playlist.fetch_all()``
        - :meth:`fortnite_api.Client.fetch_playlists`
    *   - ``client.playlist.fetch_by_id()``
        - :meth:`fortnite_api.Client.fetch_playlist`

Of course, the same applies to the SyncClient client. The methods are the same, but they are synchronous and
under the :class:`fortnite_api.SyncClient` client instead.

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
        - :class:`fortnite_api.NewDisplayAsset`
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

    shop = await client.shop.fetch_all()
    print(shop)
    >>> <fortnite_api.Shop ...>

This approach, however, is no longer valid in Version 3. Instead, you should use direct methods on the client. 

.. code-block:: python3

    shop = await client.fetch_shop()
    print(shop)
    >>> <fortnite_api.Shop ...>

Shop method changes
^^^^^^^^^^^^^^^^^^^
A complete mapping of the old methods and their new counterparts are as follows:

.. list-table::
    :header-rows: 1

    *   - Old Method
        - New Method
    *   - ``client.shop.fetch_all()``
        - :meth:`fortnite_api.Client.fetch_shop`
    *   - ``client.shop.fetch_br()``
        - Depreciated.
    *   - ``client.shop.fetch()``
        - Depreciated. ``client.shop.fetch()`` was an alias to ``fetch_br``, which has been depreciated.

Of course, the same applies to the SyncClient client. The methods are the same, but they are synchronous and
under the :class:`fortnite_api.SyncClient` client instead.


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

- :class:`fortnite_api.Version`: Represents a version of a build in Fortnite. Holds the major and minor version of the build of Fortnite.

Fetching Aes Data
~~~~~~~~~~~~~~~~~
In Version 3, the AES data is no longer fetched using the ``client.aes`` namespace. Previously, you could fetch the AES data using,

.. outdated-code-block:: python3
    :since: v2.6.6

    aes = await client.aes.fetch()
    print(aes)
    >>> <fortnite_api.AES ...>

This approach, however, is no longer valid in Version 3. Instead, you should use direct methods on the client.

.. code-block:: python3

    aes = await client.fetch_aes()
    print(aes)
    >>> <fortnite_api.Aes ...>

AES method changes
^^^^^^^^^^^^^^^^^^
A complete mapping of the old methods and their new counterparts are as follows:

.. list-table::
    :header-rows: 1

    *   - Old Method
        - New Method
    *   - ``client.aes.fetch()``
        - :meth:`fortnite_api.Client.fetch_aes`

Of course, the same applies to the SyncClient client. The methods are the same, but they are synchronous and
under the :class:`fortnite_api.SyncClient` client instead.

News 
----
News Objects 
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

    news = await client.news.fetch()
    print(news)
    >>> <fortnite_api.News ...>

However, this approach is no longer valid in Version 3. Instead, you should use direct methods on the client.

.. code-block:: python3

    news = await client.fetch_news()
    print(news)
    >>> <fortnite_api.News ...>

News method changes
^^^^^^^^^^^^^^^^^^^
A complete mapping of the old methods and their new counterparts are as follows:

.. list-table::
    :header-rows: 1

    *   - Old Method
        - New Method
    *   - ``client.news.fetch()``
        - :meth:`fortnite_api.Client.fetch_news`
    *   - ``client.news.fetch_by_type()``
        - Fetching by type has been depreciated. Rather, use these two methods: :meth:`fortnite_api.Client.fetch_news_br`, and :meth:`fortnite_api.Client.fetch_news_stw`. Note that fetching creative news has been depreciated.


Of course, the same applies to the SyncClient client. The methods are the same, but they are synchronous and
under the :class:`fortnite_api.SyncClient` client instead.

Creator Code 
------------
Creator Code Objects 
~~~~~~~~~~~~~~~~~~~~
The Creator Code objects are the same in Version 3 as they were in Version 2. A mapping of the old Creator Code objects to the new Creator Code objects is as follows:

.. list-table::
    :header-rows: 1

    *   - Old Name
        - New Name
    *   - ``CreatorCode``
        - :class:`fortnite_api.CreatorCode`


Fetching Creator Code Data
~~~~~~~~~~~~~~~~~~~~~~~~~~
In Version 2, the creator code data was fetched using the ``client.creator_code`` namespace. Previously, you could fetch the creator code data using,

.. outdated-code-block:: python3
    :since: v2.6.6

    creator_code = await client.creator_code.fetch('username')
    print(creator_code)
    >>> <fortnite_api.CreatorCode ...>

However, this approach is no longer valid in Version 3. Instead, you should use direct methods on the client.

.. code-block:: python3

    creator_code = await client.fetch_creator_code(name='username')
    print(creator_code)
    >>> <fortnite_api.CreatorCode ...>

Creator Code Method Changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^
A complete mapping of the old methods and their new counterparts are as follows:

.. list-table::
    :header-rows: 1

    *   - Old Method
        - New Method
    *   - ``client.creator_code.fetch()``
        - :meth:`fortnite_api.Client.fetch_creator_code`
    *   - ``client.creator_code.exists()``
        - Removed, try to fetch the creator code and handle not found exceptions manually.
    *   - ``client.creator_code.search_first()``
        - Depreciated, search creator code endpoints do not work anymore.
    *   - ``client.creator_code.search_all()``
        - Depreciated, search creator code endpoints do not work anymore.

Of course, the same applies to the SyncClient client. The methods are the same, but they are synchronous and
under the :class:`fortnite_api.SyncClient` client instead.

In Version 2, the ``client.creator_code.exists()`` method worked by fetching the creator code and returning ``False`` if :class:`~fortnite_api.NotFound` was raised. This method has been removed in Version 3. If you need similar functionality, you should fetch the creator code and handle the exception if it was not found. For example,

.. code-block:: python3

    try:
        creator_code = await client.fetch_creator_code(name='username')
    except fortnite_api.NotFound:
        print('Creator code not found')
    else:
        print(creator_code)

For more information on exceptions, they are all listed in the :ref:`exceptions section <migrating-exceptions>`.

BR Stats
--------
BR Stat Objects 
~~~~~~~~~~~~~~~~
The objects for BR stats remain the same in Version 3 as they were in Version 2. A mapping of the old BR stat objects to the new BR stat objects is as follows:

.. list-table::
    :header-rows: 1

    *   - Old Name
        - New Name
    *   - ``BrPlayerStats``
        - :class:`fortnite_api.BrPlayerStats`
    *   - ``BrBattlePass``
        - :class:`fortnite_api.BrBattlePass`
    *   - ``BrInputs``
        - :class:`fortnite_api.BrInputs`
    *   - ``BrInputStats``
        - :class:`fortnite_api.BrInputStats`. Note that ``trios`` stats have been depreciated.
    *   - ``BrGameModeStats``
        - :class:`fortnite_api.BrGameModeStats`

Fetching BR Stats
~~~~~~~~~~~~~~~~~~
In Version 2, the BR stats data was fetched using the ``client.stats`` namespace. Previously, you could fetch the BR stats data using,

.. outdated-code-block:: python3
    :since: v2.6.6

    stats = await client.stats.fetch_by_name('username')
    print(stats)
    >>> <fortnite_api.BrPlayerStats ...>

However, this approach is no longer valid in Version 3. Instead, you should use direct methods on the client.

.. code-block:: python3

    stats = await client.fetch_br_stats('username')
    print(stats)
    >>> <fortnite_api.BrPlayerStats ...>

BR Stats method changes
^^^^^^^^^^^^^^^^^^^^^^^^
A complete mapping of the old methods and their new counterparts are as follows:

.. list-table::
    :header-rows: 1

    *   - Old Method
        - New Method
    *   - ``client.stats.fetch_by_name()``
        - Moved to :meth:`fortnite_api.Client.fetch_br_stats` with a ``name`` parameter.
    *   - ``client.stats.fetch_by_id()``
        - Moved to the :meth:`fortnite_api.Client.fetch_br_stats` with a ``account_id`` parameter.

Of course, the same applies to the SyncClient client. The methods are the same, but they are synchronous and 
under the :class:`fortnite_api.SyncClient` client instead.

Banners 
-------
Banner Objects 
~~~~~~~~~~~~~~
A majority of the Banner objects in Version 3 are the same as they were in Version 2. A mapping of the old Banner objects to the new Banner objects is as follows:

.. list-table::
    :header-rows: 1

    *   - Old Name
        - New Name
    *   - ``Banner``
        - :class:`fortnite_api.Banner`
    *   - ``BannerColor``
        - :class:`fortnite_api.BannerColor`
    *   - ``BrBannerImage``
        - Depreciated, moved to :class:`fortnite_api.Images`. More on this below.

Fetching Banners
~~~~~~~~~~~~~~~~
Previously in Version 2, the banners were fetched using the ``client.banner`` namespace. Thus, you could fetch the banners using,

.. outdated-code-block:: python3
    :since: v2.6.6

    banners = await client.banner.fetch()
    print(banners)
    >>> [<fortnite_api.Banner ...>, ...]

    colors = await client.banner.fetch_colors()
    print(colors)
    >>> [<fortnite_api.BannerColor ...>, ...]

However, this approach is no longer valid in Version 3. Instead, you should use direct methods on the client.

.. code-block:: python3

    banners = await client.fetch_banners()
    print(banners)
    >>> [<fortnite_api.Banner ...>, ...]

    colors = await client.fetch_banner_colors()
    print(colors)
    >>> [<fortnite_api.BannerColor ...>, ...]

Banner method changes
^^^^^^^^^^^^^^^^^^^^^^
A complete mapping of the old methods and their new counterparts are as follows:

.. list-table::
    :header-rows: 1

    *   - Old Method
        - New Method
    *   - ``client.banner.fetch()``
        - :meth:`fortnite_api.Client.fetch_banners`
    *   - ``client.banner.fetch_colors()``
        - :meth:`fortnite_api.Client.fetch_banner_colors`

Of course, the same applies to the SyncClient client. The methods are the same, but they are synchronous and 
under the :class:`fortnite_api.SyncClient` client instead.

Map 
----
Map Objects 
~~~~~~~~~~~
The Map Objects have received a facelift in Version 3. A mapping of the old Map objects to the new Map objects is as follows:

.. list-table::
    :header-rows: 1

    *   - Old Name
        - New Name
    *   - ``Map``
        - :class:`fortnite_api.Map`
    *   - ``POI``
        - :class:`fortnite_api.POI`
    *   - ``POILocation``
        - :class:`fortnite_api.POILocation`
    
There is a new object relating to maps. This is,

- :class:`fortnite_api.MapImages`: Represents the image representation of the map. This is what you see when you open the map in game. It holds both a blank image and one that has the :class:`~fortnite_api.POI` locations named on it.

Fetching Maps
~~~~~~~~~~~~~~
In Version 2, the maps were fetched using the ``client.map`` namespace. For example,

.. outdated-code-block:: python3
    :since: v2.6.6

    fortnite_map = await client.map.fetch()
    print(fortnite_map)
    >>> <fortnite_api.Map ...>

In Version 3, this approach is no longer valid. Instead, you should use direct methods on the client.

.. code-block:: python3

    fortnite_map = await client.fetch_map()
    print(fortnite_map)
    >>> <fortnite_api.Map ...>

Map method changes
^^^^^^^^^^^^^^^^^^
A complete mapping of the old methods and their new counterparts are as follows:

.. list-table::
    :header-rows: 1

    *   - Old Method
        - New Method
    *   - ``client.map.fetch()``
        - :meth:`fortnite_api.Client.fetch_map`

Of course, the same applies to the SyncClient client. The methods are the same, but they are synchronous and 
under the :class:`fortnite_api.SyncClient` client instead.


.. _migrating-exceptions:

Exceptions
----------
Exceptions have been refactored in Version 3. The exception hierarchy has been restructured to make it more intuitive and easier to understand. The exceptions that are raised when an error occurs while fetching data from the Fortnite API are now more descriptive and provide more information about what went wrong.

- :class:`fortnite_api.FortniteAPIException`: The base exception class for all exceptions raised by the library. This is a subclass of :class:`Exception`.

- :class:`fortnite_api.HTTPException`: A subclass of :class:`fortnite_api.FortniteAPIException` that is raised when an error occurs while making an HTTP request to the Fortnite API. All HTTP errors are subclasses of this exception.

- :class:`fortnite_api.NotFound`: A subclass of :class:`fortnite_api.HTTPException` that is raised when the requested resource is not found. This is raised when a 404 status code is returned by the Fortnite API.

- :class:`fortnite_api.Forbidden`: A subclass of :class:`fortnite_api.HTTPException` that is raised when the client does not have permission to access the requested resource. This is raised when a 403 status code is returned by the Fortnite API.

- :class:`fortnite_api.ServiceUnavailable`: A subclass of :class:`fortnite_api.HTTPException` that is raised when the Fortnite API is unavailable. This is raised when a 503 status code is returned by the Fortnite API. Ideally your program should globally handle this exception in the event of a service outage.

- :class:`fortnite_api.RateLimited`: A subclass of :class:`fortnite_api.HTTPException` that is raised when the client has been rate limited by the Fortnite API. This is raised when a 429 status code is returned by the Fortnite API. Typical endpoints do not have rate limits, however, stats endpoints do.

- :class:`fortnite_api.Unauthorized`: A subclass of :class:`fortnite_api.HTTPException` that is raised when the client is not authorized to access the requested resource. This will be raised when the client attempts to request to stat endpoints without an api key set. This is raised when a 401 status code is returned by the Fortnite API.

- :class:`fortnite_api.BetaAccessNotEnabled`: A subclass of :class:`fortnite_api.FortniteAPIException` raised when a client attempts to call a beta method without the :attr:`~fortnite_api.Client.beta` flag enabled on the client.

- :class:`fortnite_api.BetaUnknownException`: A special subclass of :class:`fortnite_api.FortniteAPIException` that wraps an exception that occurred while calling or processing a beta endpoint. This will contain the original exception that was raised.


Datetime Objects
----------------
All datetime objects in the library have been refactored to be timezone aware to UTC. This means that all datetime objects returned by the library will be timezone aware to UTC. This is a breaking change from Version 2, where datetime objects were naive. This change was made to ensure that all datetime objects are consistent and timezone aware.

.. code-block:: python3

    cosmetics = await client.fetch_cosmetics_br()
    assert cosmetics[0].added_at.tzinfo == datetime.timezone.utc

.. _migrating-additional-objects:

Additional Objects
------------------
The library has been extended with new objects that were not present in Version 2. You may run into these as you
work with the library and upgrade from Version 2. Every object not already mentioned in this guide is discussed below:

- :class:`fortnite_api.IdComparable`: A mixin class that allows objects to be compared by their ID. This is used across many objects in the library. This implements the ``__eq__`` and ``__ne__`` methods. Any class that has an ID inherits from this class.

- :class:`fortnite_api.Hashable`: A mixin class that inherits from :class:`fortnite_api.IdComparable` and allows objects to be hashed by their ID. This is used across many objects in the library. This implements the ``__hash__`` method.

- :class:`fortnite_api.ReconstructAble`: A class that marks an object as being able to be reconstructed from a dictionary. This is used across many objects in the library. This implements the :meth:`~fortnite_api.ReconstructAble.from_dict` and :meth:`~fortnite_api.ReconstructAble.to_dict` methods, and allow you to store an object as a dictionary and reconstruct it later. Not every class inherits this, but a majority of them do. If a class does, you will see a note on the documentation for that class.

- :class:`fortnite_api.CosmeticsAll`: A special class returned when fetching all cosmetics in Fortnite. This is used when fetching all cosmetics.

- :class:`fortnite_api.Asset`: Represents any link-like object from the API. This wraps the URL and allows you to fetch the contents of the asset. This is used across many objects in the library.

- :class:`fortnite_api.KeyFormat`: An enum that represents which format to return AES keys in. This is a parameter used when fetching AES data.

- :class:`fortnite_api.GameLanguage`: An enum that holds all possible languages that the Fortnite API supports. This is used when fetching data that can be localized.

- :class:`fortnite_api.MatchMethod`: An enum that denotes which kind of string matching method to use in an endpoint that performs a search operation.

- :class:`fortnite_api.CosmeticCategory`: Represents the type of a Fortnite cosmetic. Such example would be tracks, instruments, cars, etc. This is used when fetching new cosmetics.

- :class:`fortnite_api.AccountType`: An enum that represents the platform of an Epic games account (e.g. PSN, XBL, etc). This is used as a parameter to narrow the search for an account when fetching BR stats by account name.

- :class:`fortnite_api.TimeWindow`: An enum that represents the time window for which to fetch BR stats. This is used as a parameter when fetching BR stats.

- :class:`fortnite_api.StatsImageType`: An enum that represents which type of battle royale statistics image type should be returned from the API when fetching BR stats. This is used as a parameter when fetching BR stats. 

- :class:`fortnite_api.BannerIntensity`: An enum that represents the intensity of a banner color. This is used in the :class:`~fortnite_api.ShopEntryBanner` class to represent the intensity of a banner color.

- :class:`fortnite_api.FortniteAPIException` and all its subclasses found in :ref:`the exception hierarchy <api-exception-hierarchy>`: These are exceptions that are raised when an error occurs while fetching data from the Fortnite API. They are used across the library. For what each of them do, see the :ref:`exception hierarchy <api-exception-hierarchy>`.

- :class:`fortnite_api.Images`: Represents images returned from the API. This is used across all cosmetics objects through the :class:`fortnite_api.CosmeticImages` object, as well as in the :class:`fortnite_api.Banner` object.

- :class:`fortnite_api.MaterialInstance`: Represents a material instance in Fortnite. If you do not know what a material instance is, check the documentation for the object in the library. This is used when fetching material instances manually, or sometimes given in the :class:`~fortnite_api.NewDisplayAsset` object from the shop.

- :class:`fortnite_api.MaterialInstanceImages`: A special class that represents the images of a material instance. It is given from the :class:`~fortnite_api.MaterialInstance` class. 

- :class:`fortnite_api.MaterialInstanceColors`: A class that holds the background gradient color of a material instance. This is commonly used to create a preview for the material instance in the shop. This is served from the :class:`~fortnite_api.MaterialInstance` object.

- :class:`fortnite_api.NewCosmetics`: A class that holds the response from :meth:`~fortnite_api.Client.fetch_cosmetics_new`. This is used when fetching new cosmetics.

- :class:`fortnite_api.NewCosmetic`: A class that holds specific metadata about new cosmetics, such as the last addition date, the hash of the new cosmetics, and the cosmetics type. This is served from :class:`~fortnite_api.NewCosmetics`.

- :class:`fortnite_api.proxies.TransformerListProxy`: An internal class that is used to transform a list of objects into a list of another type of object. This is used internally in the library as an optimization so that objects are only created when they are needed.

- :class:`fortnite_api.TileSize`: Represents the size of a tile in the Fortnite item shop.