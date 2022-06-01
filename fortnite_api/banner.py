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

import math
from typing import Any, Dict, Optional, Tuple

__all__: Tuple[str, ...] = ('Banner', 'BannerColor', 'BrBannerImage')


class Banner:
    """A representation of a banner given to the :class:`FortniteAPI` client
    as a response. This represents a banner within the Fortnite game.

    Attributes
    ----------
    id: :class:`str`
        The id of the banner.
    name: Optional[:class:`str`]
        The name of the banner. Can be ``None`` if the banner is not named or
        no information is provided by the API.
    description: :class:`str`
        The description of the banner.
    category: :class:`str`
        The category of the banner.
    full_usage_rights: :class:`bool`
        Denotes if the banner is full usage rights from Epic Games.
    dev_name: :class:`str`
        The developer name of the banner, this is used internally by the
        Epic Games team.
    """

    __slots__: Tuple[str, ...] = (
        'id',
        'name',
        'description',
        'category',
        'full_usage_rights',
        'dev_name',
        'small_icon',
        'icon',
        'raw_data',
    )

    def __init__(self, data: Dict[str, Any]) -> None:
        self.id: str = data['id']
        self.name: Optional[str] = data.get('str')
        self.description: str = data['category']
        self.category: str = data['category']
        self.full_usage_rights = data['fullUsageRights']
        self.dev_name: str = data['devName']

        images: Dict[str, Any] = data['images']
        self.small_icon: Optional[BrBannerImage] = BrBannerImage(smi) if (smi := images.get('smallIcon')) else None
        self.icon: Optional[BrBannerImage] = BrBannerImage(i) if (i := images.get('icon')) else None
        self.raw_data: Dict[str, Any] = data


class BannerColor:

    __slots__: Tuple[str, ...] = ('id', 'color', 'category', 'sub_category_group', 'raw_data')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.id = data.get('id')
        self.color = data.get('color')
        self.category = data.get('category')
        self.sub_category_group = data.get('subCategoryGroup')
        self.raw_data = data


class BrBannerImage:
    """Represents a Battle Royale cosmetic image.

    Attributes
    -----------
    url: :class:`str`
        The hash of the image.
    """

    __slots__: Tuple[str, ...] = ('url',)

    def __init__(self, url: str) -> None:
        self.url = url

    def url_as(self, size: int) -> str:
        if size < 0 or type(math.sqrt(size)) is float:
            raise TypeError('Size must be a power of 2.')

        url_without_type = self.url.replace('.png', '')
        return f'{url_without_type}_{size}.png'

    def __str__(self):
        return self.url
