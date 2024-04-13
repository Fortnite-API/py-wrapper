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

from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar

from ..abc import Hashable
from ..asset import Asset
from ..enums import CosmeticBrType
from ..http import HTTPClientT
from ..images import Images
from ..utils import get_with_fallback, parse_time

CosmeticT = TypeVar('CosmeticT', bound='Cosmetic[Any]')

__all__: Tuple[str, ...] = (
    'Cosmetic',
    'CosmeticTypeInfo',
    'CosmeticRarity',
    'CosmeticSeries',
    'CosmeticImages',
    'CosmeticT',
)


class Cosmetic(Hashable, Generic[HTTPClientT]):
    """Represents a cosmetic. Every cosmetic type inherits from this class.

    Attributes
    ----------
    id: :class:`str`
        The ID of the cosmetic.
    added: :class:`datetime.datetime`
        When the cosmetic was added.
    raw_data: :class:`dict`
        The raw data of the cosmetic.
    """

    __slots__: Tuple[str, ...] = ('id', 'added', 'raw_data')

    def __init__(
        self,
        *,
        data: Dict[str, Any],
        http: HTTPClientT,
    ) -> None:
        self._http: HTTPClientT = http

        self.id: str = data['id']
        self.added: datetime = parse_time(data['added'])
        self.raw_data: Dict[str, Any] = data


class CosmeticTypeInfo:
    """Represents a cosmetic type.

    Attributes
    ----------
    value: :class:`fortnite_api.CosmeticBrType`
        The value of the cosmetic type.
    display_value: :class:`str`
        The display value of the cosmetic type. This is the value that is displayed to the user.
    backend_value: :class:`str`
        The internal marker of the cosmetic type.
    """

    __slots__: Tuple[str, ...] = ('value', 'display_value', 'backend_value')

    def __init__(self, *, data: Dict[str, Any]) -> None:
        self.value: CosmeticBrType = CosmeticBrType(data['value'])
        self.display_value: str = data['displayValue']
        self.backend_value: str = data['backendValue']


class CosmeticRarity:
    """Represents a cosmetic rarity.

    Attributes
    ----------
    value: :class:`str`
        The value of the cosmetic rarity.
    display_value: :class:`str`
        The display value of the cosmetic rarity. This is the value that is displayed to the user.
    backend_value: :class:`str`
        The internal marker of the cosmetic rarity.
    """

    __slots__: Tuple[str, ...] = ('value', 'display_value', 'backend_value')

    def __init__(self, *, data: Dict[str, Any]) -> None:
        self.value: str = data['value']
        self.display_value: str = data['displayValue']
        self.backend_value: str = data['backendValue']


class CosmeticSeries(Generic[HTTPClientT]):
    """Represents the series of a cosmetic.

    Attributes
    ----------
    value: :class:`str`
        The value of the cosmetic series.
    backend_value: :class:`str`
        The internal marker of the cosmetic series.
    image: Optional[:class:`fortnite_api.Asset`]
        The image of the cosmetic series. Will be ``None`` if the cosmetic series has no image.
    colors: List[:class:`str`]
        A list of colors that are associated with the cosmetic series.
    """

    __slots__: Tuple[str, ...] = ('value', 'backend_value', 'image', 'colors')

    def __init__(
        self,
        *,
        data: Dict[str, Any],
        http: HTTPClientT,
    ) -> None:
        self.value: str = data['value']
        self.backend_value: str = data['backendValue']

        image = data.get('image')
        self.image: Optional[Asset[HTTPClientT]] = image and Asset(http=http, url=image)

        self.colors: List[str] = get_with_fallback(data, 'colors', list)


class CosmeticImages(Images[HTTPClientT]):
    """Represents the images of a cosmetic.

    This inherits from :class:`fortnite_api.Images`.

    Attributes
    ----------
    featured: Optional[:class:`fortnite_api.Asset`]
        The featured image of the cosmetic, if available.
    lego: Optional[:class:`fortnite_api.Asset`]
        The LEGO image of the cosmetic, if available.
    other: Dict[:class:`str`, :class:`fortnite_api.Asset`]
        A mapping other images to their respective asset.
    """

    __slots__: Tuple[str, ...] = ('featured', 'lego', 'other')

    def __init__(
        self,
        *,
        data: Dict[str, Any],
        http: HTTPClientT,
    ) -> None:
        super().__init__(data=data, http=http)

        featured = data.get('featured')
        self.featured: Optional[Asset[HTTPClientT]] = featured and Asset(http=http, url=featured)

        lego = data.get('lego')
        self.lego: Optional[Asset[HTTPClientT]] = lego and Asset(http=http, url=lego)

        # Mapping of str to Asset. In testing all I have found is "background" in this mapping.
        other: Dict[str, str] = get_with_fallback(data, 'other', dict)
        self.other: Dict[str, Asset[HTTPClientT]] = {key: Asset(http=http, url=value) for key, value in other.items()}
