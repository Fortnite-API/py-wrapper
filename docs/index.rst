Welcome to Fortnite-API Python Documentation
============================================

Welcome! This is the official documentation for the Fortnite-API Python library. This library allows you to interact with the Fortnite API using Python. You can use this library to get information about Fortnite players, cosmetics, shops, and more.

.. _installation:

Installation
------------
To install the Fortnite-API Python library, you can use pip. Run the following command in your terminal:

.. note::

   Note that Python 3.9 and greater is required to use this library.

.. code-block:: bash

   # Linux/macOS
   python3 -m pip install fortnite-api

   # Windows
   py -3 -m pip install fortnite-api


To install the latest development version of the library, you can use the following command:

.. code-block:: bash

   git clone https://github.com/Fortnite-API/py-wrapper
   cd py-wrapper
   python3 -m pip install .

Optional Dependencies
---------------------

- `speed`: An optional dependency that installs `orjson <https://github.com/ijl/orjson>`_ for faster JSON serialization and deserialization.

.. code-block:: bash

   # Linux/macOS
   python3 -m pip install fortnite-api[speed]

   # Windows
   py -3 -m pip install fortnite-api[speed]

API Key
-------

For most endpoints, you do not need an API key. However, some endpoints, such as fetching statistics, require an API key. To use these endpoints, you need to set the `api_key` parameter in the constructor.

.. code-block:: python3

   import asyncio
   import fortnite_api

   async def main():
      async with fortnite_api.Client(api_key="your_api_key"):
         stats = await client.fetch_br_stats(name='some_username')
         print(stats)

   if __name__ == "__main__":
      asyncio.run(main())

Generating an API Key
---------------------

You can generate an API key on `the dashboard <https://dash.fortnite-api.com/account>`_ by logging in with your Discord account.

View Documentation
------------------
The entirety of the public API is documented here. If you're looking for a specific method, class, or module, the search bar at the top right is your friend.

If you're not sure where to start, check out the :class:`fortnite_api.Client` class for a list of all available methods you can use to interact with the API.

.. toctree::
   :maxdepth: 3

   api/index

Migrating From Version 2
-------------------------

If you're migrating from version 2 of the Fortnite-API Python library, you can find a complete guide on how to do so here. This guide will help you understand the changes that were made in version 3 and how to update your code to work with the new version.

.. toctree::
   :maxdepth: 3

   migrating

Changelog
---------

The changelog contains a list of all changes made to the Fortnite-API Python library. This includes new features, bug fixes, and other changes that have been made to the library. The changelog is updated with each new release of the library.

.. toctree::
   :maxdepth: 3

   changelog


Additional Resources
--------------------

.. toctree::
   :maxdepth: 2

   response_flags