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

from .utils import simple_repr

from .abc import Hashable
from .http import HTTPClientT
from .images import Images

__all__: Tuple[str, ...] = (
    'Banner',
    'BannerColor',
)


@simple_repr
class Banner(Hashable, Generic[HTTPClientT]):
    """
    .. attributetable:: fortnite_api.Banner

    Represents a banner within the Fortnite game. This inherits from :class:`~fortnite_api.Hashable`.

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
        The category the banner belongs to.
    full_usage_rights: :class:`bool`
        Denotes if the banner is full usage rights from Epic Games.
    dev_name: :class:`str`
        The developer name of the banner, this is used internally by the
        Epic Games team.
    images: :class:`fortnite_api.Images`
        Preview images of the banner.
    raw_data: :class:`dict`
        The raw data of the banner that was used to create this object.
        This can be used for recreating the object without re-fetching the API.
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


@simple_repr
class BannerColor(Hashable):
    """
    .. attributetable:: fortnite_api.BannerColor

    Represents a color of a :class:`fortnite_api.Banner`. This inherits from :class:`~fortnite_api.Hashable`.

    Attributes
    ----------
    id: :class:`str`
        The id of the color.
    color: :class:`str`
        The color of the banner.
    colour: :class:`str`
        An alias to :attr:`~color`.
    category: :class:`str`
        The category of the banner.
    sub_category_group: :class:`int`
        The sub category group of the banner.
    raw_data: :class:`dict`
        The raw data of the banner color. This can be used for recreating the object
        without re-fetching the API.
    """

    __slots__: Tuple[str, ...] = ('id', 'color', 'category', 'sub_category_group', 'raw_data')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.id: str = data['id']

        self.color: str = data['color']
        self.colour = self.color

        self.category: str = data['category']
        self.sub_category_group: int = data['subCategoryGroup']  # TODO: Convert this to enum?
        self.raw_data = data
