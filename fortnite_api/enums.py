"""
MIT License

Copyright (c) 2019-present Luc1412
Portions of this code are Copyright (c) 2015-present Rapptz

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

import types
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Iterator, List, Mapping, NamedTuple, Tuple, Type, TypeVar

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
    'CosmeticCompatibleMode',
    'BannerIntensity',
    'CustomGender',
    'ProductTag',
)


E = TypeVar('E', bound='Enum')
OldValue = NewValue = Any


class _EnumValue(NamedTuple):
    name: str
    value: Any


def _create_value_cls(name: str, comparable: bool) -> Type[_EnumValue]:
    cls = _EnumValue
    cls.__repr__ = lambda self: f'<{name}.{self.name}: {self.value!r}>'
    cls.__str__ = lambda self: f'{name}.{self.name}'
    if comparable:
        cls.__le__ = lambda self, other: isinstance(other, self.__class__) and self.value <= other.value
        cls.__ge__ = lambda self, other: isinstance(other, self.__class__) and self.value >= other.value
        cls.__lt__ = lambda self, other: isinstance(other, self.__class__) and self.value < other.value
        cls.__gt__ = lambda self, other: isinstance(other, self.__class__) and self.value > other.value

    return cls


def _is_descriptor(obj: Type[object]) -> bool:
    return hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__')


class EnumMeta(type):
    if TYPE_CHECKING:
        _enum_member_names_: ClassVar[List[str]]
        _enum_member_map_: ClassVar[Dict[str, Any]]
        _enum_value_map_: ClassVar[Dict[Any, Any]]

    def __new__(
        cls,
        name: str,
        bases: Tuple[type, ...],
        attrs: Dict[str, Any],
        *,
        comparable: bool = False,
    ) -> EnumMeta:
        value_mapping: Dict[OldValue, NewValue] = {}
        member_mapping: Dict[str, NewValue] = {}
        member_names: List[str] = []

        value_cls = _create_value_cls(name, comparable)
        for key, value in list(attrs.items()):
            is_descriptor = _is_descriptor(value)
            if key[0] == '_' and not is_descriptor:
                continue

            # Special case classmethod to just pass through
            if isinstance(value, classmethod):
                continue

            if is_descriptor:
                setattr(value_cls, key, value)
                del attrs[key]
                continue

            try:
                new_value = value_mapping[value]
            except KeyError:
                new_value = value_cls(name=key, value=value)
                value_mapping[value] = new_value
                member_names.append(key)

            member_mapping[key] = new_value
            attrs[key] = new_value

        attrs['_enum_value_map_'] = value_mapping
        attrs['_enum_member_map_'] = member_mapping
        attrs['_enum_member_names_'] = member_names
        attrs['_enum_value_cls_'] = value_cls
        actual_cls = super().__new__(cls, name, bases, attrs)
        value_cls._actual_enum_cls_ = actual_cls  # type: ignore # Runtime attribute isn't understood
        return actual_cls

    def __iter__(cls) -> Iterator[Any]:
        return (cls._enum_member_map_[name] for name in cls._enum_member_names_)

    def __reversed__(cls) -> Iterator[Any]:
        return (cls._enum_member_map_[name] for name in reversed(cls._enum_member_names_))

    def __len__(cls) -> int:
        return len(cls._enum_member_names_)

    def __repr__(cls) -> str:
        return f'<enum {cls.__name__}>'

    @property
    def __members__(cls) -> Mapping[str, Any]:
        return types.MappingProxyType(cls._enum_member_map_)

    def __call__(cls, value: str) -> Any:
        try:
            return cls._enum_value_map_[value]
        except (KeyError, TypeError):
            raise ValueError(f"{value!r} is not a valid {cls.__name__}")

    def __getitem__(cls, key: str) -> Any:
        return cls._enum_member_map_[key]

    def __setattr__(cls, name: str, value: Any) -> None:
        raise TypeError('Enums are immutable.')

    def __delattr__(cls, attr: str) -> None:
        raise TypeError('Enums are immutable')

    def __instancecheck__(self, instance: Any) -> bool:
        # isinstance(x, Y)
        # -> __instancecheck__(Y, x)
        try:
            return instance._actual_enum_cls_ is self
        except AttributeError:
            return False


if TYPE_CHECKING:
    from enum import Enum
else:

    class Enum(metaclass=EnumMeta):
        @classmethod
        def try_value(cls, value):
            try:
                return cls._enum_value_map_[value]
            except (KeyError, TypeError):
                return value


class KeyFormat(Enum):
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


class GameLanguage(Enum):
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


class MatchMethod(Enum):
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


class CosmeticCategory(Enum):
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


class CosmeticRarity(Enum):
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


class CosmeticType(Enum):
    """Represents a type of a :class:`fortnite_api.CosmeticBr` cosmetic.

    Attributes
    ----------
    OUTFIT
    BACKPACK
    PET
    PET_CARRIER
    PICKAXE
    SHOES
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
    SHOES = 'shoe'
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


class AccountType(Enum):
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


class TimeWindow(Enum):
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


class StatsImageType(Enum):
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


class CosmeticCompatibleMode(Enum):
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
        return try_enum(cls, trimmed)


class BannerIntensity(Enum):
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


class CustomGender(Enum):
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


class ProductTag(Enum):
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
        return try_enum(cls, trimmed.lower())


def create_unknown_value(cls: Type[E], val: Any) -> E:
    value_cls = cls._enum_value_cls_  # type: ignore # This is narrowed below
    name = f'UNKNOWN_{val}'
    return value_cls(name=name, value=val)


def try_enum(cls: Type[E], val: Any) -> E:
    """A function that tries to turn the value into enum ``cls``.

    If it fails it returns a proxy invalid value instead.
    """

    try:
        return cls._enum_value_map_[val]  # type: ignore # All errors are caught below
    except (KeyError, TypeError, AttributeError):
        return create_unknown_value(cls, val)
