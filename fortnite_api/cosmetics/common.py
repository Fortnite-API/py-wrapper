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
from typing import Any, Generic, TypeVar

from ..abc import DictT, Hashable, ReconstructAble
from ..asset import Asset
from ..enums import CosmeticRarity, CosmeticType, try_enum
from ..http import HTTPClientT
from ..images import Images
from ..utils import get_with_fallback, parse_time, simple_repr

CosmeticT = TypeVar("CosmeticT", bound="Cosmetic[Any, Any]")

__all__: tuple[str, ...] = (
    "Cosmetic",
    "CosmeticTypeInfo",
    "CosmeticRarityInfo",
    "CosmeticSeriesInfo",
    "CosmeticImages",
    "CosmeticT",
)


class Cosmetic(Generic[DictT, HTTPClientT], Hashable, ReconstructAble[DictT, HTTPClientT]):
    """
    .. attributetable:: fortnite_api.Cosmetic

    Represents a base cosmetic. Every cosmetic type inherits from this class and adds additional attributes.
    View documentation for the specific cosmetic type for more information.

    This class inherits from :class:`~fortnite_api.Hashable` and :class:`~fortnite_api.ReconstructAble`.

    - :class:`fortnite_api.CosmeticBr`
    - :class:`fortnite_api.CosmeticCar`
    - :class:`fortnite_api.CosmeticInstrument`
    - :class:`fortnite_api.CosmeticLegoKit`
    - :class:`fortnite_api.CosmeticTrack`
    - :class:`fortnite_api.VariantLego`
    - :class:`fortnite_api.VariantBean`

    Attributes
    ----------
    id: :class:`str`
        The ID of the cosmetic.
    added: :class:`datetime.datetime`
        When the cosmetic was added.
    """

    __slots__: tuple[str, ...] = ("id", "added")

    def __init__(
        self,
        *,
        data: DictT,
        http: HTTPClientT,
    ) -> None:
        super().__init__(data=data, http=http)

        self.id: str = data["id"]
        self.added: datetime = parse_time(data["added"])


@simple_repr
class CosmeticTypeInfo(ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.CosmeticTypeInfo

    A class that holds cosmetic type information passed from the API for
    a given :class:`~fortnite_api.Cosmetic`.

    This class inherits from :class:`~fortnite_api.ReconstructAble`.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

    Attributes
    ----------
    value: :class:`fortnite_api.CosmeticType`
        The value of the cosmetic type.
    raw_value: :class:`str`
        The raw value of the cosmetic type. This value is used to construct the
        :attr:`value` attribute, but, is exposed through this attribute due to how
        commonly it is used.
    display_value: :class:`str`
        The display value of the cosmetic type. This is the value that is displayed to the user.
    backend_value: :class:`str`
        The internal marker of the cosmetic type.
    """

    __slots__: tuple[str, ...] = (
        "value",
        "raw_value",
        "display_value",
        "backend_value",
    )

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.value: CosmeticType = try_enum(CosmeticType, data["value"])
        self.raw_value: str = data["value"]

        self.display_value: str = data["displayValue"]
        self.backend_value: str = data["backendValue"]


@simple_repr
class CosmeticRarityInfo(ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.CosmeticRarityInfo

    Represents a cosmetic rarity. This class is used to hold information about the rarity of a cosmetic.

    This class inherits from :class:`~fortnite_api.ReconstructAble`.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

    Attributes
    ----------
    value: :class:`fortnite_api.CosmeticRarity`
        The rarity of the cosmetic.
    display_value: :class:`str`
        The display value of the cosmetic rarity. This is the value that is displayed to the user.
    backend_value: :class:`str`
        The internal marker of the cosmetic rarity.
    """

    __slots__: tuple[str, ...] = ("value", "display_value", "backend_value")

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.value: CosmeticRarity = try_enum(CosmeticRarity, data["value"])
        self.display_value: str = data["displayValue"]
        self.backend_value: str = data["backendValue"]


@simple_repr
class CosmeticSeriesInfo(ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.CosmeticSeriesInfo

    Represents information about the series a :class:`~fortnite_api.Cosmetic` belongs to.
    This class inherits from :class:`~fortnite_api.ReconstructAble`.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

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

    __slots__: tuple[str, ...] = ("value", "backend_value", "image", "colors")

    def __init__(
        self,
        *,
        data: dict[str, Any],
        http: HTTPClientT,
    ) -> None:
        super().__init__(data=data, http=http)

        self.value: str = data["value"]
        self.backend_value: str = data["backendValue"]

        image = data.get("image")
        self.image: Asset[HTTPClientT] | None = image and Asset(http=http, url=image)

        self.colors: list[str] = get_with_fallback(data, "colors", list)


@simple_repr
class CosmeticImages(Images[HTTPClientT]):
    """
    .. attributetable:: fortnite_api.CosmeticImages

    Represents the images of a cosmetic.

    This inherits from :class:`fortnite_api.Images`.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

    Attributes
    ----------
    featured: Optional[:class:`fortnite_api.Asset`]
        The featured image of the cosmetic, if available. Typically available off of :class:`fortnite_api.CosmeticBr` objects.
    lego: Optional[:class:`fortnite_api.Asset`]
        The LEGO image of the cosmetic, if available. Typically available off of :class:`fortnite_api.CosmeticBr` objects.
    bean: Optional[:class:`fortnite_api.Asset`]
        The bean image of the cosmetic, if available. Typically available off of :class:`fortnite_api.CosmeticBr` objects.
    small: Optional[:class:`fortnite_api.Asset`]
        The small image of the cosmetic. Typically available off of :class:`fortnite_api.CosmeticInstrument`,
        :class:`fortnite_api.CosmeticCar`, :class:`fortnite_api.CosmeticLegoKit`,
        and :class:`fortnite_api.VariantLego` objects.
    large: Optional[:class:`fortnite_api.Asset`]
        The large image of the cosmetic. Typically available off of :class:`fortnite_api.CosmeticInstrument`,
        :class:`fortnite_api.CosmeticCar`, :class:`fortnite_api.CosmeticLegoKit`,
        and :class:`fortnite_api.VariantLego` objects.
    wide: Optional[:class:`fortnite_api.Asset`]
        The wide image of the cosmetic. Typically available off of :class:`fortnite_api.VariantLego` objects.
    """

    __slots__: tuple[str, ...] = (
        "featured",
        "lego",
        "bean",
        "_other",
        "_http",
        "small",
        "large",
        "wide",
    )

    def __init__(
        self,
        *,
        data: dict[str, Any],
        http: HTTPClientT,
    ) -> None:
        super().__init__(data=data, http=http)

        featured = data.get("featured")
        self.featured: Asset[HTTPClientT] | None = featured and Asset(http=http, url=featured)

        lego = data.get("lego")
        self.lego: Asset[HTTPClientT] | None = lego and Asset(http=http, url=lego)

        bean = data.get("bean")
        self.bean: Asset[HTTPClientT] | None = bean and Asset(http=http, url=bean)

        small = data.get("small")
        self.small: Asset[HTTPClientT] | None = small and Asset(http=http, url=small)

        large = data.get("large")
        self.large: Asset[HTTPClientT] | None = large and Asset(http=http, url=large)

        wide = data.get("wide")
        self.wide: Asset[HTTPClientT] | None = wide and Asset(http=http, url=wide)

        self._other: dict[str, str] = get_with_fallback(data, "other", dict)
        self._http: HTTPClientT = http

    @property
    def background(self) -> Asset[HTTPClientT] | None:
        """
        Optional[:class:`~fortnite_api.Asset`]: The background image of the cosmetic, if available.
        """
        url = self._other.get("background")
        if not url:
            return

        return Asset(http=self._http, url=url)

    @property
    def coverart(self) -> Asset[HTTPClientT] | None:
        """
        Optional[:class:`~fortnite_api.Asset`]: The cover art image of the cosmetic, if available.
        """
        url = self._other.get("coverart")
        if not url:
            return

        return Asset(http=self._http, url=url)

    @property
    def decal(self) -> Asset[HTTPClientT] | None:
        """
        Optional[:class:`~fortnite_api.Asset`]: The decal image of the cosmetic, if available.
        """
        url = self._other.get("decal")
        if not url:
            return

        return Asset(http=self._http, url=url)
