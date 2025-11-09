.. currentmodule:: fortnite_api

.. _changelog:

Changelog
=========

.. _vp3p4p0:

v3.4.0
-------

New Features
~~~~~~~~~~~~
- Added :meth:`fortnite_api.Client.close` and :meth:`fortnite_api.SyncClient.close` methods to close the client's HTTP session when not using a context manager.

.. _vp3p3p0:

v3.3.0
-------

Breaking Changes
~~~~~~~~~~~~~~~~
- Drop support for Python 3.9. The minimum supported Python version is now 3.10.

New Features
~~~~~~~~~~~~
- Added support for :attr:`fortnite_api.CosmeticType.SIDEKICK`.

Bug Fixes
~~~~~~~~~
- Fixed an issue that caused :class:`fortnite_api.Asset.resize` to raise :class:`TypeError` instead of :class:`ValueError` when the given size isn't a power of 2.
- Fixed an issue that caused :class:`fortnite_api.ServiceUnavailable` to be raised with a static message as a fallback for all unhandled http status codes. Instead :class:`fortnite_api.HTTPException` is raised with the proper error message.
- Fixed typing of our internal "Enum-like" classes. They are now typed as a :class:`py:enum.Enum`.

Miscellaneous
~~~~~~~~~~~~~
- Added official support for Python 3.14.

.. _vp3p2p1:

v3.2.1
-------

Bug Fixes
~~~~~~~~~
- Fixed an issue due a change from Epic that causes :class:`fortnite_api.VariantBean` to not have a :class:`fortnite_api.CustomGender`. It now uses :attr:`fortnite_api.CustomGender.UNKNOWN` in such case instead of raising an exception.
- Fixed typo within fallback system for :class:`fortnite_api.TileSize` as ``raise`` keyword was used instead of ``return``.
- Fixed an issue that caused a :class:`KeyError` to be raised when using :meth:`fortnite_api.Client.search_br_cosmetics` or :meth:`fortnite_api.SyncClient.search_br_cosmetics` without ``multiple`` parameter.


.. _vp3p2p0:

v3.2.0
-------
This version introduces support for new Shoes cosmetic type, drops support for Python 3.8, and adds safeguards and future proofing against potential API changes.

Breaking Changes
~~~~~~~~~~~~~~~~
- Drop support for Python 3.8. The minimum supported Python version is now 3.9.
- ``CreatorCode.status`` and ``CreatorCode.disabled`` have been removed, since both returned a static value. Disabled creator codes always raise :class:`fortnite_api.NotFound` when trying to fetch them.
- ``CreatorCode.verified`` has been removed, since it isn't used within the affiliate system. It always returns ``False``.
- All enums now use an internal "Enum-like" class to handle unknown values, instead of the built-in :class:`py:enum.Enum`. This potentially breaks type checks, but does not break core functionality or change the enum interface; you can use them the same.

New Features
~~~~~~~~~~~~
- Added support for :attr:`fortnite_api.CosmeticType.SHOES`.

Documentation
~~~~~~~~~~~~~
- Document :class:`fortnite_api.Forbidden` to be raised by :meth:`fortnite_api.Client.fetch_br_stats` and :meth:`fortnite_api.SyncClient.fetch_br_stats`.

Miscellaneous
~~~~~~~~~~~~~
- Add safeguards against Epic Games' API changing or providing invalid values in API responses.
    - All enums now can handle unknown values via an internally defined "Enum-like" class. If the API returns a value not in the enum, it will be stored as an attribute on the enum object. The interface for using this class is the same as using :class:`py:enum.Enum`.
    - :class:`fortnite_api.TileSize` no longer raises :class:`ValueError` when an unknown value is passed to it. Instead, it now has a fallback value of `-1` for both width and height.


.. _vp3p1p0:

v3.1.0
-------
This version introduces new data for shop-related objects, reflecting the updated shop layouts and the Fortnite webshop. Additionally, it includes functions that were omitted in version v3.0.0 and addresses a design decision that results in a breaking change.

Breaking Changes
~~~~~~~~~~~~~~~~
- ``ShopEntryNewDisplayAsset`` has been renamed to :class:`fortnite_api.NewDisplayAsset`.
- Alias ``BannerColor.colour`` has been removed for consistency. The API does not use aliases, use  :attr:`fortnite_api.BannerColor.color` instead.

New Features
~~~~~~~~~~~~
- Added new object :class:`fortnite_api.ProductTag`.
- Added attribute :attr:`fortnite_api.MaterialInstance.product_tag`.
- Added new object :class:`fortnite_api.ShopEntryOfferTag`.
- Added new object :class:`fortnite_api.ShopEntryColors`.
- Added new object :class:`fortnite_api.RenderImage`.
- Added attribute :attr:`fortnite_api.ShopEntryLayout.rank`.
- Added attribute :attr:`fortnite_api.NewDisplayAsset.render_images`.
- Added attribute :attr:`fortnite_api.ShopEntry.offer_tag`.
- Added attribute :attr:`fortnite_api.ShopEntry.colors`.

Bug Fixes
~~~~~~~~~
- Fixed an issue where ``type`` and ``time_window`` parameters were not respected when fetching stats.
- :attr:`fortnite_api.Playlist.images` now returns ``None`` when no images are available, instead of an empty dict.
- Bug fix for returning naive datetime objects in rare cases. All datetime objects are UTC aware.

Documentation
~~~~~~~~~~~~~
- Added :ref:`response flags <response_flags>` documentation to explain how to use the ``fortnite_api.ResponseFlags`` class, how to enable response flags, which response flags are available, and when you should enable them.
- Added ``opt-in`` directive in the documentation on attributes that require a specific response flag to be set. This ensures users know of the response flags required to access certain attributes when using the API.

Miscellaneous
~~~~~~~~~~~~~
- Previously, fetching specific game mode news raised :class:`fortnite_api.ServiceUnavailable` due to improper handling from Fortnite-API.com. This has been fixed within the API. Now, when no news is available, :class:`fortnite_api.NotFound` is raised instead. This change is also reflected in the documentation.


.. _vp3p0p0:

v3.0.0
-------
For help on Migrating to Version 3 from Version 2, and a complete list of all the new features, see the :ref:`Migration guide <migrating>`.