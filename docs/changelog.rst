.. currentmodule:: fortnite_api

.. _changelog:

Changelog
=========

.. _vp3p1p0:

v3.1.0
-------
This version introduces new data for shop-related objects, reflecting the updated shop layouts and the Fortnite webshop. Additionally, it includes functions that were omitted in version 3.0.0 and addresses a design decision that results in a breaking change.

Breaking Changes
~~~~~~~~~~~~~~~~
- ``ShopEntryNewDisplayAsset`` has been renamed to :class:`fortnite_api.NewDisplayAsset`.
- ``Banner.colour`` has been removed as it was merely an alias for :attr:`fortnite_api.Banner.color`.

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
- Fetching specific game mode news when no news is available now raises :class:`fortnite_api.NotFound` instead of :class:`fortnite_api.ServiceUnavailable`, thanks to proper handling from Fortnite-API.com. Documentation has been updated accordingly.
- Fixed an issue where ``type`` and ``time_window`` parameters were not respected when fetching stats.
- :attr:`fortnite_api.Playlist.images` now returns ``None`` when no images are available, instead of an empty dict.
- Ensured all datetime objects include timezone information to avoid returning naive datetime objects in rare cases.

Miscellaneous
~~~~~~~~~~~~~
- Improved documentation for attributes that require specific response flags to be set.


.. _vp3p0p0:

v3.0.0
-------
For help on Migrating to Version 3 from Version 2, and a complete list of all the new features, see the :ref:`Migration guide <migrating>`.