.. currentmodule:: fortnite_api

.. _clients:

Clients
=======

The client classes are the main way to interact with the Fortnite API. They provide all the methods to get data from the API. It's through them that you are served most every object in this library. 

There are two main clients you can use to interact with the API: the :class:`Client` and the :class:`SyncClient`. The :class:`Client` is the main client and is the one you should use in most cases. It is asynchronous and uses the `aiohttp` library to make requests. The :class:`SyncClient` is a synchronous client that uses the `requests` library to make requests. It is useful if you are working in a synchronous environment or if you don't want to deal with the complexity of asynchronous programming.

Both clients have the same methods and return the same objects. The only difference is that the :class:`Client` has asynchronous methods and the :class:`SyncClient` has synchronous methods.

.. autoclass:: fortnite_api.Client
    :members:

.. autoclass:: fortnite_api.SyncClient
    :members: