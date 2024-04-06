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

from typing import Any, Dict, List, Optional

from ..asset import Asset
from ..http import HTTPClientT
from ..utils import get_with_fallback
from .common import Cosmetic, CosmeticImages


class CosmeticLegoImages(CosmeticImages[HTTPClientT]):
    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        _wide = data.get('wide')
        self.wide: Optional[Asset[HTTPClientT]] = _wide and Asset(http=http, url=_wide)


class CosmeticLego(Cosmetic[HTTPClientT]):
    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.cosmetic_id: str = data['cosmeticId']
        self.sound_library_tags: List[str] = get_with_fallback(data, 'soundLibraryTags', list)

        _images = data.get('images')
        self.images: Optional[CosmeticLegoImages[HTTPClientT]] = _images and CosmeticLegoImages(data=_images, http=http)
        self.path: Optional[str] = data.get('path')
