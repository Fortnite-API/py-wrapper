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

from typing import Any, Optional

from .abc import Hashable, ReconstructAble
from .http import HTTPClientT
from .images import Images
from .utils import simple_repr

__all__: tuple[str, ...] = (
    "Banner",
    "BannerColor",
)


@simple_repr
class Banner(Hashable, ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.Banner

    Represents a banner within the Fortnite game.

    This inherits from :class:`~fortnite_api.Hashable` and :class:`~fortnite_api.ReconstructAble`.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

    Examples
    --------
    .. code-block:: python3
        :caption: Fetch all banners in Fortnite.

        # (1) Fetch all the banners using the client
        banners = await client.fetch_banners()

        # (2) Walk through each banner
        for banner in banners:
            # (3) Print out their metadata
            print(banner.id, banner.name, banner.description)

    .. code-block:: python3
        :caption: Fetch the images of all the banners in Fortnite.

        # (1) Fetch all the banners using the client
        banners = await client.fetch_banners()

        # (2) Walk through each banner
        for banner in banners:
            # (3) Print out the image URL of the banner
            print(banner.images.icon.url)

    Attributes
    ----------
    id: :class:`str`
        The id of the banner.
    name: Optional[:class:`str`]
        The name of the banner. Can be ``None`` if the banner is not named or
        no information is provided by the API.
    description: :class:`str`
        The description of the banner.
    category: Optional[:class:`str`]
        The category the banner belongs to. Can be ``None`` if this banner
        does not belong to any category.
    full_usage_rights: :class:`bool`
        Denotes if the banner is full usage rights from Epic Games.
    dev_name: :class:`str`
        The developer name of the banner, this is used internally by the
        Epic Games team.
    images: :class:`fortnite_api.Images`
        Preview images of the banner.
    """

    __slots__: tuple[str, ...] = (
        "id",
        "name",
        "description",
        "category",
        "full_usage_rights",
        "dev_name",
        "images",
    )

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.id: str = data["id"]
        self.name: str = data["name"]
        self.dev_name: str = data["devName"]
        self.description: str = data["description"]
        self.category: Optional[str] = data.get("category")
        self.full_usage_rights: bool = data["fullUsageRights"]

        self.images: Images[HTTPClientT] = Images(data=data, http=http)


@simple_repr
class BannerColor(Hashable, ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.BannerColor

    Represents a color of a :class:`fortnite_api.Banner`.

    This inherits from :class:`~fortnite_api.Hashable` and :class:`~fortnite_api.ReconstructAble`.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

    Attributes
    ----------
    id: :class:`str`
        The id of the color.
    color: :class:`str`
        The color of the banner.
    category: :class:`str`
        The category of the banner.
    sub_category_group: :class:`int`
        The sub category group of the banner.
    """

    __slots__: tuple[str, ...] = ("id", "color", "category", "sub_category_group")

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)
        self.id: str = data["id"]

        self.color: str = data["color"]

        self.category: str = data["category"]
        self.sub_category_group: int = data["subCategoryGroup"]  # TODO: Convert this to enum?
