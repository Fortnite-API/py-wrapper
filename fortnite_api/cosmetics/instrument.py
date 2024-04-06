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
from typing import Any, Dict, Optional, List

from ..utils import get_with_fallback, parse_time

from ..http import HTTPClientT
from .common import Cosmetic, CosmeticImages, CosmeticRarity, CosmeticSeries, CosmeticType


class CosmeticInstrument(Cosmetic[HTTPClientT]):
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
