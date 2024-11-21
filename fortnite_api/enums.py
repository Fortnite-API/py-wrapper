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
from typing import Tuple, Type

from typing_extensions import Self

__all__: Tuple[str, ...] = (
    'KeyFormat',
    'GameLanguage',
    'MatchMethod',
    'CosmeticCategory',
    'CosmeticRarity',
    'CosmeticType',
    'AccountType',
    'TimeWindow',
    'StatsImageType',
    'CreatorCodeStatus',
    'CosmeticCompatibleMode',
    'BannerIntensity',
    'CustomGender',
    'ProductTag',
)


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
    PORTUGUESE_BRASIL
        Portuguese (Brasil) language.
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


class CosmeticCategory(enum.Enum):
    """Represents the internal names for the types of a cosmetics in Fortnite.

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
        Type of a :class:`fortnite_api.VariantLego` cosmetic variant.
    LEGO_KITS
        Type of a :class:`fortnite_api.CosmeticLegoKit` cosmetic.
    BEANS
        Type of a :class:`fortnite_api.VariantBean` cosmetic variant.
    """

    BR = "br"
    TRACKS = "tracks"
    INSTRUMENTS = "instruments"
    CARS = "cars"
    LEGO = "lego"
    LEGO_KITS = "legokits"
    BEANS = "beans"


class CosmeticRarity(enum.Enum):
    """Represents a rarity of a :class:`~fortnite_api.Cosmetic` object.

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


class CosmeticType(enum.Enum):
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
    ALL
        The material instance is compatible with all modes.
    """

    BATTLE_ROYALE = 'battleroyale'
    LEGO = 'juno'
    ROCKET_RACING = 'delmar'
    FESTIVAL = 'sparks'
    ALL = 'max'

    @classmethod
    def _from_str(cls: Type[Self], string: str) -> Self:
        # The Epic Games API uses both "CosmeticCompatibleMode" and "CosmeticCompatibleModeLegacy" enums
        # with the same values, so we need to handle both.
        # To easily handle this, we'll remove the "ECosmeticCompatibleMode::" or "ECosmeticCompatibleModeLegacy::" prefix.
        # and then convert it to the enum.
        trimmed = string.split('::')[-1]
        return cls(trimmed.lower())


class BannerIntensity(enum.Enum):
    """Denotes the intensity of a :class:`fortnite_api.ShopEntryBanner`.

    Attributes
    ----------
    LOW
        Low intensity.
    HIGH
        High intensity.
    """

    LOW = 'Low'
    HIGH = 'High'


class CustomGender(enum.Enum):
    """Denotes the gender of a character in Fortnite.

    At the moment, this is only used on the :class:`fortnite_api.VariantBean` class.

    Attributes
    ----------
    FEMALE
        A female character.
    MALE
        A male character.
    """

    FEMALE = 'EFortCustomGender::Female'
    MALE = 'EFortCustomGender::Male'


class ProductTag(enum.Enum):
    """A class that represents the tag of a product.

    Attributes
    ----------
    BATTLE_ROYALE
        The product is for Battle Royale.
    LEGO
        The product is for LEGO.
    ROCKET_RACING
        The product is for Rocket Racing.
    FESTIVAL
        The product is for Festival.
    ALL
        The product is for all modes.
    """

    BATTLE_ROYALE = 'br'
    LEGO = 'juno'
    ROCKET_RACING = 'delmar'
    FESTIVAL = 'sparks'
    ALL = 'max'

    @classmethod
    def _from_str(cls: Type[Self], string: str) -> Self:
        # The Epic Games API "Product" enums contains both lower case and capitalized values, so we need to handle both.
        # To easily handle this, we'll remove the "Product." prefix and convert it to lowercase.
        trimmed = string.split('.')[-1]
        return cls(trimmed.lower())
