.. currentmodule:: fortnite_api

.. _response_flags:

Response Flags
==============

The Fortnite-API uses response flags to indicate if some optional fields are present in an API response. These flags
are optional, meaning that you can choose not to include them in the response. 

By default, any response flags are not enabled on the :class:`~fortnite_api.Client` and :class:`~fortnite_api.SyncClient` class. To enable them, you can set the
``response_flags`` parameter in the constructor.

Using the Response Flags Class
------------------------------
The :class:`~fortnite_api.ResponseFlags` class provides a set of flags that you can enable or disable and set in the client.
This class is a subclass of the built-in :class:`~py.enum.IntFlag`, and thus, supports bitwise operations.

To consider how to use response flags, let's consider the following example:

.. code-block:: python3

    from enum import IntFlag, auto

    class Color(IntFlag):
        RED = auto()
        GREEN = auto()
        BLUE = auto()

Here, we have defined a class titled ``Color`` as a subclass of :class:`~py.enum.IntFlag`. This class has three fields: ``RED``, ``GREEN``, and ``BLUE``. Each field is an instance of the :class:`~py.enum.auto` class, which automatically assigns a unique value to each field.

To enable the ``RED`` and ``GREEN`` flags, you can use the bitwise OR operator:

.. code-block:: python3

    flags = Color.RED | Color.GREEN

The value of ``flags`` will be the bitwise OR of the values of ``Color.RED`` and ``Color.GREEN``. In this case, the value of ``flags`` will be ``3``.

To check if a flag is enabled, you can use the bitwise AND operator:

.. code-block:: python3

    if flags & Color.RED:
        print("RED is enabled")

The value of ``flags & Color.RED`` will be the bitwise AND of the values of ``flags`` and ``Color.RED``. If the result is non-zero, the flag is enabled. Otherwise, the flag is disabled.

This same concept applies to the response flags. For more information on bit manipulation, see this article on `Bitwise Operators <https://www.geeksforgeeks.org/python-bitwise-operators/>`_.

Response Flags Class Fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~

These are several fields on the :class:`~fortnite_api.ResponseFlags` class.

- :attr:`~fortnite_api.ResponseFlags.INCLUDE_NOTHING`: Disables all response flags. This is the default value on the client.
- :attr:`~fortnite_api.ResponseFlags.INCLUDE_PATHS`: Enables the ``path`` field of a response to be present. By default, the path to a Fortnite cosmetic is not included in the response.
- :attr:`~fortnite_api.ResponseFlags.INCLUDE_GAMEPLAY_TAGS`: Enables the ``gameplay_tags`` field of a response to be present. By default, the gameplay tags of a Fortnite cosmetic are not included in the response and will simply be an empty list.
- :attr:`~fortnite_api.ResponseFlags.INCLUDE_SHOP_HISTORY`: Enables the ``shop_history`` field of a response to be present. By default, the shop history of a Fortnite cosmetic is not included in the response and will simply be an empty list.

To enable response flags, you can use the bitwise OR operator to combine the flags you want to enable, or use the :meth:`~fortnite_api.ResponseFlags.all` method to enable everything.

.. hint::

    Every attribute that requires a specific response flag to be set in this documentation will have a note indicating 
    which response flag is required to be set on the client class. If the response flag is not set, the attribute will
    not have an expected value.

Setting Response Flags
----------------------

Setting response flags on the client is simple. You can set the ``response_flags`` parameter in the constructor to enable the flags you want to include in the response. Consider the following example:

.. code-block:: python3

    import fortnite_api

    # NOTE: Shorthand import for readability. Doing this 
    # is optional and not required.
    from fortnite_api import ResponseFlags

    async def main():
        response_flags = ResponseFlags.INCLUDE_PATHS | ResponseFlags.INCLUDE_GAMEPLAY_TAGS
        async with fortnite_api.Client(response_flags=response_flags) as client:
            # (1) Fetch the Renegade Raider
            cosmetic = await client.fetch_cosmetic_br('CID_028_Athena_Commando_F') 
            
            # (2) Print the path and gameplay tags
            print(cosmetic.path)
            >>> 'Athena/Items/Cosmetics/Characters/CID_028_Athena_Commando_F'
            print(cosmetic.gameplay_tags)
            >>> ['Cosmetics.Source.Season1', ...]

            # (3) Print the shop history. Note this will ALWAYS be 
            # an EMPTY LIST because the shop history response flag has not
            # been set on the client class.
            print(cosmetic.shop_history)
            >>> []

We see that the ``path`` and ``gameplay_tags`` fields are present in the response, while the ``shop_history`` field is not. This is because the ``INCLUDE_PATHS`` and ``INCLUDE_GAMEPLAY_TAGS`` flags are enabled, while the ``INCLUDE_SHOP_HISTORY`` flag is not.

Now, let's enable all response flags using the :meth:`~fortnite_api.ResponseFlags.all` method:

.. code-block:: python3

    import fortnite_api

    async def main():
        response_flags = fortnite_api.ResponseFlags.all()
        async with fortnite_api.Client(response_flags=response_flags) as client:
            # (1) Fetch the Renegade Raider
            cosmetic = await client.fetch_cosmetic_br('CID_028_Athena_Commando_F') 
            
            # (2) Print the path, gameplay tags, and shop history
            print(cosmetic.path)
            >>> 'Athena/Items/Cosmetics/Characters/CID_028_Athena_Commando_F'
            print(cosmetic.gameplay_tags)
            >>> ['Cosmetics.Source.Season1', ...]
            print(cosmetic.shop_history)
            >>> ['2021-09-01T00:00:00Z', ...]

We can see now that all fields are present in the response. This is because all response flags are enabled.
