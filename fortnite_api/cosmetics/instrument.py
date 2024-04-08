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

import datetime
from typing import Any, Dict, List, Optional, Tuple

from ..http import HTTPClientT
from ..utils import get_with_fallback, parse_time
from .common import Cosmetic, CosmeticImages, CosmeticRarity, CosmeticSeries, CosmeticType

__all__: Tuple[str, ...] = ('CosmeticInstrument',)


class CosmeticInstrument(Cosmetic[HTTPClientT]):
    """Represents an instrument cosmetic in Fortnite.

    This class inherits from :class:`Cosmetic`.

    Attributes
    ----------
    name: :class:`str`
        The name of the instrument.
    description: :class:`str`
        The description of the instrument.
    type: Optional[:class:`CosmeticType`]
        The type of the instrument.
    rarity: Optional[:class:`CosmeticRarity`]
        The rarity of the instrument.
    images: Optional[:class:`CosmeticImages`]
        Any instrument images.
    series: Optional[:class:`CosmeticSeries`]
        The series of the instrument.
    gameplay_tags: List[:class:`str`]
        The gameplay tags of the instrument.
    path: Optional[:class:`str`]
        The path of the instrument.
    showcase_video: Optional[:class:`str`]
        The showcase video of the instrument.
    shop_history: List[:class:`datetime.datetime`]
        The shop history of the instrument.
    """

    __slots__: Tuple[str, ...] = (
        'name',
        'description',
        'type',
        'rarity',
        'images',
        'series',
        'gameplay_tags',
        'path',
        'showcase_video',
        'shop_history',
    )

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.name: str = data['name']
        self.description: str = data['description']

        _type = data.get('type')
        self.type: Optional[CosmeticType] = _type and CosmeticType(data=_type)

        _rarity = data.get('rarity')
        self.rarity: Optional[CosmeticRarity] = _rarity and CosmeticRarity(data=_rarity)

        _images = data.get('images')
        self.images: Optional[CosmeticImages[HTTPClientT]] = _images and CosmeticImages(data=_images, http=http)

        _series = data.get('series')
        self.series: Optional[CosmeticSeries[HTTPClientT]] = _series and CosmeticSeries(data=_series, http=self._http)

        self.gameplay_tags: List[str] = get_with_fallback(data, 'gameplayTags', list)
        self.path: Optional[str] = data.get('path')
        self.showcase_video: Optional[str] = data.get('showcaseVideo')

        self.shop_history: List[datetime.datetime] = [
            parse_time(time) for time in get_with_fallback(data, 'shopHistory', list)
        ]
