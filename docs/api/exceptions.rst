.. currentmodule:: fortnite_api

Exceptions
===========

.. _api-exception-hierarchy:

Exception Hierarchy
-------------------

.. exception_hierarchy::
    - :exc:`~fortnite_api.FortniteAPIException`
        - :exc:`~fortnite_api.HTTPException`
            - :exc:`~fortnite_api.NotFound`
            - :exc:`~fortnite_api.Forbidden`
            - :exc:`~fortnite_api.ServiceUnavailable`
            - :exc:`~fortnite_api.RateLimited`
            - :exc:`~fortnite_api.Unauthorized`
        - :exc:`~fortnite_api.BetaAccessNotEnabled`
        - :exc:`~fortnite_api.BetaUnknownException`

Exception Classes
-----------------

.. autoclass:: FortniteAPIException
    :members:

.. autoclass:: HTTPException
    :members:

.. autoclass:: NotFound
    :members:

.. autoclass:: Forbidden
    :members:

.. autoclass:: ServiceUnavailable
    :members:

.. autoclass:: RateLimited
    :members:

.. autoclass:: Unauthorized
    :members:

.. autoclass:: BetaAccessNotEnabled
    :members:

.. autoclass:: BetaUnknownException
    :members: