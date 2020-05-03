.. currentmodule:: fortnite_api

API Reference
===============

The following section outlines the API of fortnite-api

Version Related Info
---------------------

.. data:: __version__

    A string representation of the version. e.g. ``'1.0.0'``. This is based
    off of :pep:`440`.

FortniteAPI
-----------

.. autoclass:: FortniteAPI
    :members:

.. _fortnite-api-enums:

Enumerations
-------------
The API provides some enumerations for certain types of strings to avoid the API
from being stringly typed in case the strings change in the future.

All enumerations are subclasses of an internal class which mimics the behaviour
of :class:`enum.Enum`.

.. class:: GameLanguage

    Specifies the language of the output.

    .. attribute:: ARABIC

        Arabic language.
    .. attribute:: GERMAN

        German language.
    .. attribute:: ENGLISH

        English language. This is used as default value.
    .. attribute:: SPANISH

        Spanish language.
    .. attribute:: SPANISH_LATIN

        Spanish (Latin) language.
    .. attribute:: FRENCH

        French language.
    .. attribute:: ITALIAN

        Italian language.
    .. attribute:: JAPANESE

        Japanese language.
    .. attribute:: KOREAN

        Korean language.
    .. attribute:: POLISH

        Polish language.
    .. attribute:: PORTUGUESE_BRASIL

        Portuguese (Brasil) language.
    .. attribute:: RUSSIAN

        Russian language.
    .. attribute:: TURKISH

        Turkish language.
    .. attribute:: CHINESE_SIMPLIFIED

        Chinese (simplified) language.
    .. attribute:: CHINESE_TRADITIONAL

        Chinese (traditional) language.

.. class:: MatchMethod

    Specifies the search match method.

    .. attribute:: FULL

        The desired result must match the searched word.
    .. attribute:: CONTAINS

        The desired result must contain the searched word.
    .. attribute:: STARTS

        The desired result must start with the searched word.
    .. attribute:: ENDS

        The desired result must end with the searched word.

.. class:: BrCosmeticRarity

    Specifies the Rarity of a Battle Royale cosmetic.

    .. attribute:: FROZEN

        Frozen rarity.
    .. attribute:: LAVA

        Lava rarity.
    .. attribute:: LEGENDARY

        Legendary rarity.
    .. attribute:: DARK

        Dark rarity.
    .. attribute:: STARWARS

        Starwars rarity.
    .. attribute:: MARVEL

        Marvel rarity.
    .. attribute:: DC

        DC rarity.
    .. attribute:: ICON_SERIES

        Icon Series rarity.
    .. attribute:: SHADOW

        Shadow rarity.
    .. attribute:: EPIC

        Epic rarity.
    .. attribute:: RARE

        Rare rarity.
    .. attribute:: UNCOMMON

        Uncommon rarity.
    .. attribute:: COMMON

        Common rarity.

.. class:: BrCosmeticType

    Specifies the type of a Battle Royale cosmetic.

    .. attribute:: BANNER

        A banner.
    .. attribute:: BACKPACK

        A backpack.
    .. attribute:: CONTRAIL

        A contrail.
    .. attribute:: OUTFIT

        A outfit.
    .. attribute:: EMOTE

        A emote.
    .. attribute:: EMOJI

        A emoji.
    .. attribute:: GLIDER

        A glider.
    .. attribute:: WRAP

        A wrap.
    .. attribute:: LOADING_SCREEN

        A loading screen.
    .. attribute:: MUSIC

        A music pack.
    .. attribute:: PET

        A pet.
    .. attribute:: PICKAXE

        A pick axe.
    .. attribute:: SPRAY

        A pray.
    .. attribute:: TOY

        A toy.

.. class:: NewsType

    Specifies the type of ingame news.

    .. attribute:: BATTLE_ROYALE

        Battle Royale.
    .. attribute:: SAVE_THE_WORLD

        Save The World.
    .. attribute:: CREATIVE

        Creative.

Endpoints
---------

Cosmetics
~~~~~~~~~

.. autoclass:: SyncCosmeticsEndpoints()
    :members:
    :inherited-members:

.. autoclass:: AsyncCosmeticsEndpoints()
    :members:
    :inherited-members:

CreatorCode
~~~~~~~~~~~

.. autoclass:: SyncCreatorCodeEndpoints()
    :members:
    :inherited-members:

.. autoclass:: AsyncCreatorCodeEndpoints()
    :members:
    :inherited-members:

News
~~~~

.. autoclass:: SyncNewsEndpoints()
    :members:
    :inherited-members:

.. autoclass:: AsyncNewsEndpoints()
    :members:
    :inherited-members:

Shop
~~~~

.. autoclass:: SyncShopEndpoints()
    :members:
    :inherited-members:

.. autoclass:: AsyncShopEndpoints()
    :members:
    :inherited-members:


.. _discord_api_models:

FortniteAPI Models
------------------

Cosmetics
~~~~~~~~~
All Cosmetic Models.

BrCosmetic
^^^^^^^^^^
.. autoclass:: BrCosmetic()
    :members:
    :inherited-members:

BRCosmeticImage
^^^^^^^^^^^^^^^
.. autoclass:: BrCosmeticImage()
    :members:
    :inherited-members:

BrCosmeticVariant
^^^^^^^^^^^^^^^^^
.. autoclass:: BrCosmeticVariant()
    :members:
    :inherited-members:

BrCosmeticVariantOption
^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: BrCosmeticVariantOption()
    :members:
    :inherited-members:

CreatorCode
~~~~~~~~~~~
All Creator Code Models.

CreatorCode
^^^^^^^^^^^
.. autoclass:: CreatorCode()
    :members:
    :inherited-members:

News
~~~~
All News Models.

News
^^^^
.. autoclass:: News()
    :members:
    :inherited-members:

GameModeNews
^^^^^^^^^^^^
.. autoclass:: GameModeNews()
    :members:
    :inherited-members:

NewsEntry
^^^^^^^^^
.. autoclass:: NewsEntry()
    :members:
    :inherited-members:

Shop
~~~~
All Shop Models.

BrShop
^^^^^^
.. autoclass:: BrShop()
    :members:
    :inherited-members:

BrShopEntry
^^^^^^^^^^^
.. autoclass:: BrShopEntry()
    :members:
    :inherited-members:

User
~~~~
All User Models.

User
^^^^
.. autoclass:: User()
    :members:
    :inherited-members:




