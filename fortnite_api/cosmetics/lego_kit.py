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

from typing import Any, Dict, List, Optional, Tuple

from ..http import HTTPClientT
from ..utils import get_with_fallback, parse_time, simple_repr
from .common import Cosmetic, CosmeticImages, CosmeticSeriesInfo, CosmeticTypeInfo

__all__: Tuple[str, ...] = ('CosmeticLegoKit',)


@simple_repr
class CosmeticLegoKit(Cosmetic[Dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.CosmeticLegoKit

    Represents a LEGO kit cosmetic in Fortnite.

    This class inherits from :class:`fortnite_api.Cosmetic`.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

    Attributes
    ----------
    name: :class:`str`
        The name of the LEGO kit.
    type: Optional[:class:`fortnite_api.CosmeticTypeInfo`]
        The type of the LEGO kit.
    gameplay_tags: List[:class:`str`]
        The gameplay tags of the LEGO kit.

        .. opt-in:: INCLUDE_GAMEPLAY_TAGS
    images: Optional[:class:`fortnite_api.CosmeticImages`]
        Any LEGO kit images.
    path: Optional[:class:`str`]
        The path of the LEGO kit.

        .. opt-in:: INCLUDE_PATHS
    shop_history: List[:class:`datetime.datetime`]
        The shop history of the LEGO kit.

        .. opt-in:: INCLUDE_SHOP_HISTORY
    """

    __slots__: Tuple[str, ...] = ('name', 'type', 'gameplay_tags', 'images', 'path', 'shop_history')

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.name: str = data['name']

        _type = data.get('type')
        self.type: Optional[CosmeticTypeInfo[HTTPClientT]] = _type and CosmeticTypeInfo(data=_type, http=http)

        _series = data.get('series')
        self.series: Optional[CosmeticSeriesInfo[HTTPClientT]] = _series and CosmeticSeriesInfo(data=_series, http=http)

        self.gameplay_tags: List[str] = get_with_fallback(data, 'gameplayTags', list)

        _images = data.get('images')
        self.images: Optional[CosmeticImages[HTTPClientT]] = _images and CosmeticImages(data=_images, http=http)

        self.path: Optional[str] = data.get('path')
        self.shop_history = [parse_time(time) for time in get_with_fallback(data, 'shopHistory', list)]
