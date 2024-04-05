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

from typing import Any, Dict, Generic, Tuple

from .abc import Hashable
from .http import HTTPClientT
from .images import Images

__all__: Tuple[str, ...] = ('Banner', 'BannerColor')


class Banner(Hashable, Generic[HTTPClientT]):
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
        'icon',
    images: :class:`Images`
        The images of the banner.
    """

    __slots__: Tuple[str, ...] = (
        'id',
        'name',
        'description',
        'category',
        'full_usage_rights',
        'dev_name',
        'images',
        'raw_data',
    )

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.id: str = data['id']
        self.name: str = data['name']
        self.dev_name: str = data['devName']
        self.description: str = data['category']
        self.category: str = data['category']
        self.full_usage_rights: bool = data['fullUsageRights']

        self.images: Images[HTTPClientT] = Images(data=data, http=http)
        self.raw_data: Dict[str, Any] = data


class BannerColor(Hashable):
    __slots__: Tuple[str, ...] = ('id', 'color', 'category', 'sub_category_group', 'raw_data')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.id: str = data['id']
        self.color: str = data['color']
        self.category: str = data['category']
        self.sub_category_group: int = data['subCategoryGroup']  # TODO: Convert this to enum
        self.raw_data = data
