.. currentmodule:: fortnite_api

API Reference
=============

Clients
-------
.. autoclass:: fortnite_api.FortniteAPI
    :members:


.. autoclass:: fortnite_api.SyncFortniteAPI
    :members:

Base Classes
------------

.. autoclass:: fortnite_api.abc.IdComparable
    :members:

.. autoclass:: fortnite_api.abc.Hashable
    :members:


Objects
-------

.. autoclass:: fortnite_api.account.Account
    :members:

.. autoclass:: fortnite_api.aes.Aes
    :members:

.. autoclass:: fortnite_api.aes.Version
    :members:

.. autoclass:: fortnite_api.aes.DynamicKey
    :members:

.. autoclass:: fortnite_api.all.CosmeticsAll
    :members:

.. autoclass:: fortnite_api.asset.Asset
    :members:

.. autoclass:: fortnite_api.banner.Banner
    :members:

.. autoclass:: fortnite_api.banner.BannerColor
    :members:

.. autoclass:: fortnite_api.banner.BannerColour
    :members:

.. autoclass:: fortnite_api.creator_code.CreatorCode
    :members:


Enumerations
------------

.. class:: KeyFormat

    Represents a return format type for the AES endpoint.

    .. attribute:: HEX

        Return the AES keys in hexadecimal format.
    
    .. attribute:: BASE64
        
        Return the AES keys in base64 format.

.. class:: GameLanguage

    Represents a language that Fortnite supports. This can be used to change the return language of many API calls.

    
    .. attribute:: ARABIC

        Arabic language.
    
    .. attribute:: GERMAN
            
        German language.
    
    .. attribute:: ENGLISH

        English language.
    
    .. attribute:: SPANISH

        Spanish language.
    
    .. attribute:: SPANISH_LATIN 

        Latin Spanish language.
    
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

    .. attribute:: PORTUGUESE

        Portuguese language.
    
    .. attribute:: RUSSIAN

        Russian language.
    
    .. attribute:: TURKISH

        Turkish language.
    
    .. attribute:: CHINESE_SIMPLIFIED

        Simplified Chinese language.
    
    .. attribute:: CHINESE_TRADITIONAL

        Traditional Chinese language.


.. class:: MatchMethod

    Represents a string matching method for some search methods in the API.

    .. attribute:: FULL

        Match the full string.
    
    .. attribute:: CONTAINS

        Match the string if it contains part or all of the search string.
    
    .. attribute:: STARTS

        Match the string if it starts with the search string.
    
    .. attribute:: ENDS

        Match the string if it ends with the search string.

.. class:: CosmeticType
    
    Represents a type of a cosmetic in Fortnite.

    .. attribute:: BR

        A type of a :class:`fortnite_api.cosmetic.CosmeticBr` cosmetic. 
    
    .. attribute:: TRACKS

        The type of a :class:`fortnite_api.cosmetic.CosmeticTrack` cosmetic.
    
    .. attribute:: INSTRUMENTS

        The type of a :class:`fortnite_api.cosmetic.CosmeticInstrument` cosmetic.
    
    .. attribute:: CARS

        The type of a :class:`fortnite_api.cosmetic.CosmeticCar` cosmetic.
    
    .. attribute:: LEGO

        The type of a :class:`fortnite_api.cosmetic.CosmeticLego` cosmetic.

    .. attribute:: LEGO_KITS

        The type of a :class:`fortnite_api.cosmetic.CosmeticLegoKit` cosmetic.


.. class:: CosmeticBrRarity

    Represents a rarity of a :class:`fortnite_api.cosmetic.CosmeticBr` cosmetic.

    .. attribute:: FROZEN
    .. attribute:: LAVA
    .. attribute:: LEGENDARY
    .. attribute:: GAMING_LEGENDS
    .. attribute:: DARK
    .. attribute:: STARWARS
    .. attribute:: MARVEL
    .. attribute:: DC
    .. attribute:: ICON_SERIES
    .. attribute:: SHADOW
    .. attribute:: SLURP
    .. attribute:: EPIC
    .. attribute:: LAMBORGHINI
    .. attribute:: RARE
    .. attribute:: UNCOMMON
    .. attribute:: COMMON
    .. attribute:: MYTHIC


.. class:: CosmeticBrType

    Represents a type of a :class:`fortnite_api.cosmetic.CosmeticBr` cosmetic.

    .. attribute:: OUTFIT
    .. attribute:: BACKPACK
    .. attribute:: PET
    .. attribute:: PET_CARRIER
    .. attribute:: PICKAXE
    .. attribute:: GLIDER
    .. attribute:: CONTRAIL
    .. attribute:: AURA
    .. attribute:: EMOTE
    .. attribute:: EMOJI
    .. attribute:: SPRAY
    .. attribute:: TOY
    .. attribute:: WRAP
    .. attribute:: BANNER
    .. attribute:: MUSIC
    .. attribute:: LOADING_SCREEN
    .. attribute:: GUITAR
    .. attribute:: BASS
    .. attribute:: DRUMS
    .. attribute:: MICROPHONE
    .. attribute:: KEYTAR
    .. attribute:: CAR_BODY
    .. attribute:: DECAL
    .. attribute:: WHEELS
    .. attribute:: TRAIL
    .. attribute:: BOOST
    .. attribute:: JAM_TRACK
    .. attribute:: LEGO_BUILD
    .. attribute:: LEGO_DECOR_BUNDLE
    .. attribute:: SHOUT


.. class:: AccountType

    Represents the type of a :class:`fortnite_api.account.Account`.

    .. attribute:: EPIC

        An Epic Games account.
    
    .. attribute:: PSN
            
        An PSN, Play Station Network, account.

    .. attribute:: XBL

        An XBL, Xbox Live, account.


.. class:: TimeWindow

    Represents a time window for statistics in the API.

    .. attribute:: SEASON

        Denotes that the results should only be for the current season.
    
    .. attribute:: LIFETIME

        Denotes that the results should be for the lifetime of an account.
    

.. class:: StatsImageType

    Represents the type of image that should be returned from the stats image endpoint.

    .. attribute:: ALL

        Return an image that has statistics for all input types.

    .. attribute:: KEYBOARD_MOUSE

        Return an image that has statistics for only keyboard and mouse input types.

    .. attribute:: GAMEPAD

        Return an image that has statistics for only gamepad (controller) input types.

    .. attribute:: TOUCH

        Return an image that has statistics for only touch input types.
    
    .. attribute:: NONE

        No image should be returned.


.. class:: CreatorCodeStatus

    Represents the status of a creator code.

    .. attribute:: ACTIVE

        The creator code is active.
    
    .. attribute:: DISABLED

        The creator code is disabled.


.. class:: TileSize

    Represents the given size of a tile in the item shop.

    .. attribute:: SMALL

        A small sized tile.

    .. attribute:: NORMAL

        A normal sized title.

    .. attribute:: DOUBLE_WIDE

        A double wide sized tile.
    
    .. attribute:: TRIPLE_WIDE

        A triple wide sized tile.


.. class:: CosmeticCompatibleMode

    A class that represents the compatibility of a cosmetic material instance with other modes.

    .. attribute:: BATTLE_ROYALE

        The material instance is compatible with Battle Royale.

    .. attribute:: LEGO

        The material instance is compatible with LEGO.

    .. attribute:: ROCKET_RACING

        The material instance is compatible with Rocket Racing.

    .. attribute:: FESTIVAL

        The material instance is compatible with Festival.


.. class:: BannerIntensity

    Denotes the intensity of a :class:`fortnite_api.ShopEntryBanner`.

    .. attribute:: LOW

        Low intensity.

    .. attribute:: MEDIUM

        Medium intensity.
    
    .. attribute:: HIGH

        High intensity.
