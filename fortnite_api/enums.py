"""
MIT License

Copyright (c) 2019-present Luc1412

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

import enum


class KeyFormat(enum.Enum):
    """Represents a return format type for the AES endpoint.

    Attributes
    ----------
    HEX
        Return the AES keys in hexadecimal format.
    BASE64
        Return the AES keys in base64 format.
    """

    HEX = 'hex'
    BASE64 = 'base64'


class GameLanguage(enum.Enum):
    """Represents a language that Fortnite supports. This can be
    used to change the return language of many API calls.

    Attributes
    ----------
    ARABIC
        Arabic language.
    GERMAN
        German language.
    ENGLISH
        English language.
    SPANISH
        Spanish language.
    SPANISH_LATIN
        Latin Spanish language.
    FRENCH
        French language.
    ITALIAN
        Italian language.
    JAPANESE
        Japanese language.
    KOREAN
        Korean language.
    POLISH
        Polish language.
    PORTUGUESE
        Portuguese language.
    RUSSIAN
        Russian language.
    TURKISH
        Turkish language.
    CHINESE_SIMPLIFIED
        Simplified Chinese language.
    CHINESE_TRADITIONAL
        Traditional Chinese language.
    """

    ARABIC = 'ar'
    GERMAN = 'de'
    ENGLISH = 'en'
    SPANISH = 'es'
    SPANISH_LATIN = 'es-419'
    FRENCH = 'fr'
    ITALIAN = 'it'
    JAPANESE = 'ja'
    KOREAN = 'ko'
    POLISH = 'pl'
    PORTUGUESE_BRASIL = 'pt-BR'
    RUSSIAN = 'ru'
    TURKISH = 'tr'
    CHINESE_SIMPLIFIED = 'zh-CN'
    CHINESE_TRADITIONAL = 'zh-Hant'


class MatchMethod(enum.Enum):
    """Represents a string matching method for some search methods in the API.

    Attributes
    ----------
    FULL
        Match the full string.
    CONTAINS
        Match if the string contains the search string.
    STARTS
        Match if the string starts with the search string.
    ENDS
        Match if the string ends with the search string.
    """

    FULL = 'full'
    CONTAINS = 'contains'
    STARTS = 'starts'
    ENDS = 'ends'


class CosmeticType(enum.Enum):
    """Represents a type of a cosmetic in Fortnite.

    Attributes
    ----------
    BR
        Type of a :class:`fortnite_api.CosmeticBr` cosmetic.
    TRACKS
        Type of a :class:`fortnite_api.CosmeticTrack` cosmetic.
    INSTRUMENTS
        Type of a :class:`fortnite_api.CosmeticInstrument` cosmetic.
    CARS
        Type of a :class:`fortnite_api.CosmeticCar` cosmetic.
    LEGO
        Type of a :class:`fortnite_api.CosmeticLego` cosmetic.
    LEGO_KITS
        Type of a :class:`fortnite_api.CosmeticLegoKit` cosmetic.
    """

    BR = "br"
    TRACKS = "tracks"
    INSTRUMENTS = "instruments"
    CARS = "cars"
    LEGO = "lego"
    LEGO_KITS = "legokits"


class CosmeticBrRarity(enum.Enum):
    """Represents a rarity of a :class:`fortnite_api.CosmeticBr` cosmetic.

    Attributes
    ----------
    FROZEN
    LAVA
    LEGENDARY
    GAMING_LEGENDS
    DARK
    STARWARS
    MARVEL
    DC
    ICON_SERIES
    SHADOW
    SLURP
    EPIC
    LAMBORGHINI
    RARE
    UNCOMMON
    COMMON
    MYTHIC
    """

    FROZEN = 'frozen'
    LAVA = 'lava'
    LEGENDARY = 'legendary'
    GAMING_LEGENDS = 'gaminglegends'
    DARK = 'dark'
    STARWARS = 'starwars'
    MARVEL = 'marvel'
    DC = 'dc'
    ICON_SERIES = 'icon'
    SHADOW = 'shadow'
    SLURP = 'slurp'
    EPIC = 'epic'
    LAMBORGHINI = 'lamborghini'
    RARE = 'rare'
    UNCOMMON = 'uncommon'
    COMMON = 'common'
    MYTHIC = 'mythic'


class CosmeticBrType(enum.Enum):
    """Represents a type of a :class:`fortnite_api.CosmeticBr` cosmetic.

    Attributes
    ----------
    OUTFIT
    BACKPACK
    PET
    PET_CARRIER
    PICKAXE
    GLIDER
    CONTRAIL
    AURA
    EMOTE
    EMOJI
    SPRAY
    TOY
    WRAP
    BANNER
    MUSIC
    LOADING_SCREEN
    GUITAR
    BASS
    DRUMS
    MICROPHONE
    KEYTAR
    CAR_BODY
    DECAL
    WHEELS
    TRAIL
    BOOST
    JAM_TRACK
    LEGO_BUILD
    LEGO_DECOR_BUNDLE
    SHOUT
    """

    OUTFIT = 'outfit'
    BACKPACK = 'backpack'
    PET = 'pet'
    PET_CARRIER = 'petcarrier'
    PICKAXE = 'pickaxe'
    GLIDER = 'glider'
    CONTRAIL = 'contrail'
    AURA = 'aura'

    EMOTE = 'emote'
    EMOJI = 'emoji'
    SPRAY = 'spray'
    TOY = 'toy'

    WRAP = 'wrap'

    BANNER = 'banner'
    MUSIC = 'music'
    LOADING_SCREEN = 'loadingscreen'

    GUITAR = 'guitar'
    BASS = 'bass'
    DRUMS = 'drum'
    MICROPHONE = 'mic'
    KEYTAR = 'keyboard'

    CAR_BODY = 'body'
    DECAL = 'skin'
    WHEELS = 'wheel'
    TRAIL = 'drifttrail'
    BOOST = 'booster'

    JAM_TRACK = 'track'

    LEGO_BUILD = 'legoset'
    LEGO_DECOR_BUNDLE = 'legoprop'

    SHOUT = 'shout'


class AccountType(enum.Enum):
    """Represents the type of a :class:`fortnite_api.account.Account`.

    Attributes
    ----------
    EPIC
        Epic Games account.
    PSN
        PlayStation Network account.
    XBL
        Xbox Live account.
    """

    EPIC = 'epic'
    PSN = 'psn'
    XBL = 'xbl'


class TimeWindow(enum.Enum):
    """Represents a time window for statistics in the API.

    Attributes
    ----------
    SEASON
        Denotes that the results should only be for the current season.
    LIFETIME
        Denotes that the results should be for the lifetime of an account.
    """

    SEASON = 'season'
    LIFETIME = 'lifetime'


class StatsImageType(enum.Enum):
    """Represents the type of image that should be returned from the stats image endpoint.

    Attributes
    ----------
    ALL
        Return an image that has statistics for all input types.
    KEYBOARD_MOUSE
        Return an image that has statistics for only keyboard and mouse input types.
    GAMEPAD
        Return an image that has statistics for only gamepad (controller) input types.
    TOUCH
        Return an image that has statistics for only touch input types.
    NONE
        No image should be returned.
    """

    ALL = 'all'
    KEYBOARD_MOUSE = 'keyboardMouse'
    GAMEPAD = 'gamepad'
    TOUCH = 'touch'
    NONE = 'none'


class CreatorCodeStatus(enum.Enum):
    """Represents the status of a creator code.

    Attributes
    ----------
    ACTIVE
        The creator code is active.
    DISABLED
        The creator code is disabled.
    """

    ACTIVE = 'active'
    DISABLED = 'disabled'


class CosmeticCompatibleMode(enum.Enum):
    """A class that represents the compatibility of a cosmetic :class:`fortnite_api.MaterialInstance` with other modes.

    Attributes
    ----------
    BATTLE_ROYALE
        The material instance is compatible with Battle Royale.
    LEGO
        The material instance is compatible with LEGO.
    ROCKET_RACING
        The material instance is compatible with Rocket Racing.
    FESTIVAL
        The material instance is compatible with Festival.
    """

    BATTLE_ROYALE = 'ECosmeticCompatibleMode::BattleRoyale'
    LEGO = 'ECosmeticCompatibleMode::Juno'
    ROCKET_RACING = 'ECosmeticCompatibleMode::DelMar'
    FESTIVAL = 'ECosmeticCompatibleMode::Sparks'


class BannerIntensity(enum.Enum):
    """Denotes the intensity of a :class:`fortnite_api.ShopEntryBanner`.

    Attributes
    ----------
    LOW
        Low intensity.
    MEDIUM
        Medium intensity.
    HIGH
        High intensity.
    """

    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
