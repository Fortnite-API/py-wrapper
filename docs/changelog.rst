.. currentmodule:: fortnite_api

.. _changelog:

Changelog
=========

.. _vp3p2p0:

v3.2.0
-------

Breaking Changes
~~~~~~~~~~~~~~~~
- ``CreatorCode.status`` and ``CreatorCode.disabled`` have been removed, since they where never returned by this endpoint. Disabled creator codes always raise :class:`fortnite_api.NotFound` when trying to fetch them.
- ``CreatorCode.verified`` has been removed, since it isn't used within the affiliate system. It always returns ``False``.

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