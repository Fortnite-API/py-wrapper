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
from ..utils import get_with_fallback, parse_time, simple_repr
from .common import Cosmetic, CosmeticImages, CosmeticRarityInfo, CosmeticSeriesInfo, CosmeticTypeInfo

__all__: Tuple[str, ...] = ('CosmeticInstrument',)


@simple_repr
class CosmeticInstrument(Cosmetic[Dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.CosmeticInstrument

    Represents an instrument cosmetic in Fortnite.

    This class inherits from :class:`fortnite_api.Cosmetic`.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

    Attributes
    ----------
    name: :class:`str`
        The name of the instrument.
    description: :class:`str`
        The description of the instrument.
    type: Optional[:class:`fortnite_api.CosmeticTypeInfo`]
        The type of the instrument.
    rarity: Optional[:class:`fortnite_api.CosmeticRarityInfo`]
        The rarity of the instrument.
    images: Optional[:class:`fortnite_api.CosmeticImages`]
        Any instrument images.
    series: Optional[:class:`fortnite_api.CosmeticSeriesInfo`]
        The series of the instrument.
    gameplay_tags: List[:class:`str`]
        The gameplay tags of the instrument.
    path: Optional[:class:`str`]
        The path of the instrument.

        .. opt-in:: INCLUDE_PATHS

    showcase_video_id: Optional[:class:`str`]
        The showcase YouTube video ID of the cosmetic, if available.
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
        'showcase_video_id',
        'shop_history',
    )

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.name: str = data['name']
        self.description: str = data['description']

        _type = data.get('type')
        self.type: Optional[CosmeticTypeInfo[HTTPClientT]] = _type and CosmeticTypeInfo(data=_type, http=http)

        _rarity = data.get('rarity')
        self.rarity: Optional[CosmeticRarityInfo[HTTPClientT]] = _rarity and CosmeticRarityInfo(data=_rarity, http=http)

        _images = data.get('images')
        self.images: Optional[CosmeticImages[HTTPClientT]] = _images and CosmeticImages(data=_images, http=http)

        _series = data.get('series')
        self.series: Optional[CosmeticSeriesInfo[HTTPClientT]] = _series and CosmeticSeriesInfo(
            data=_series, http=self._http
        )

        self.gameplay_tags: List[str] = get_with_fallback(data, 'gameplayTags', list)
        self.path: Optional[str] = data.get('path')
        self.showcase_video_id: Optional[str] = data.get('showcaseVideo')

        self.shop_history: List[datetime.datetime] = [
            parse_time(time) for time in get_with_fallback(data, 'shopHistory', list)
        ]

    @property
    def showcase_video_url(self) -> Optional[str]:
        """Optional[:class:`str`]: The URL of the YouTube showcase video of the cosmetic, if any."""
        _id = self.showcase_video_id
        if not _id:
            return None

        return f"https://www.youtube.com/watch?v={_id}"
