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
from .asset import Asset
from .enums import CosmeticCompatibleMode, ProductTag
from .http import HTTPClientT
from .utils import get_with_fallback

__all__: tuple[str, ...] = (
    "RenderImage",
    "MaterialInstanceImages",
    "MaterialInstanceColors",
    "MaterialInstance",
    "NewDisplayAsset",
)


class RenderImage(ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.RenderImage

    Represents a render image for a shop entry. A render image is an image
    used to visually represent a cosmetic item in the shop. This class inherits
    from :class:`~fortnite_api.ReconstructAble`.

    .. versionchanged:: v3.1.0
        Renamed from ``ShopEntryRenderImage`` to a more generic ``RenderImage``
        to reflect its usage across the API.

    Attributes
    ----------
    product_tag: :class:`fortnite_api.ProductTag`
        The product tag of the render image.
    file_name: :class:`str`
        The internal file name of the rendered image. Refers to the name within the game files and **not** the :attr`image`. An example of this is ``T-Featured-Pickaxes-SleepyTimePickaxe``.
    image: :class:`fortnite_api.Asset`
        The image of the render image.
    """

    __slots__: tuple[str, ...] = ("product_tag", "file_name", "image")

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.product_tag: ProductTag = ProductTag._from_str(data["productTag"])
        self.file_name: str = data["fileName"]
        self.image: Asset[HTTPClientT] = Asset(url=data["image"], http=http)


class MaterialInstanceImages(dict[str, Asset[HTTPClientT]]):
    """
    .. attributetable:: fortnite_api.MaterialInstanceImages

    Represents some images of a Material instance, as they are rendered in game. Although this class
    has concrete attributes, the API generates the keys dynamically. The most common keys are exposed as attributes, and all
    other keys are available through dictionary operations.

    This class inherits from :class:`dict`, and thus, supports all the operations that a normal
    dictionary does, such as indexing, iteration, etc.

    .. versionchanged:: v3.1.0
        Moved from the now-deleted ``fortnite_api.material`` to ``fortnite_api.new_display_asset``.

    Attributes
    ----------
    offer_image: Optional[:class:`fortnite_api.Asset`]
        The offer image of the Material instance. This is the image that is shown in the item shop.
        Can be ``None`` if there is no offer image for the Material instance.
    background: Optional[:class:`fortnite_api.Asset`]
        The background of the Material instance. This is the background gradient
        of the material instance. Can be ``None`` if there is no background
        for the Material instance.
    """

    __slots__: tuple[str, ...] = ("offer_image", "background")

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        _offer_image = data.get("OfferImage")
        self.offer_image: Optional[Asset[HTTPClientT]] = _offer_image and Asset(url=_offer_image, http=http)

        _background = data.get("Background", None)
        self.background: Optional[Asset[HTTPClientT]] = _background and Asset(url=_background, http=http)

        # Transform all remaining keys into assets, and pass this along to the dict constructor
        super().__init__({key: Asset(url=value, http=http) for key, value in data.items()})


class MaterialInstanceColors(dict[str, str]):
    """
    .. attributetable:: fortnite_api.MaterialInstanceColors

    Represents some metadata about the colors of a Material instance. Although the keys are dynamically generated in the API, the most common keys are exposed as attributes.

    This class inherits from :class:`dict`, and thus, supports all the operations that a normal dictionary does, such as indexing, iteration, etc.

    .. versionchanged:: v3.1.0
        Moved from the now-deleted ``fortnite_api.material`` to ``fortnite_api.new_display_asset``.

    Attributes
    ----------
    background_color_a: Optional[:class:`str`]
        The first background color of the Material instance, if any.
    background_color_b: Optional[:class:`str`]
        The second background color of the Material instance, if any.
    fall_off_color: Optional[:class:`str`]
        The fall off color of the Material instance, if any.
    """

    __slots__: tuple[str, ...] = (
        "background_color_a",
        "background_color_b",
        "fall_off_color",
    )

    def __init__(self, *, data: dict[str, Any]) -> None:
        self.background_color_a: Optional[str] = data.get("Background_Color_A")
        self.background_color_b: Optional[str] = data.get("Background_Color_B")
        self.fall_off_color: Optional[str] = data.get("FallOff_Color")
        super().__init__(data)


class MaterialInstance(Hashable, ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.MaterialInstance

    Material instancing is a way to create a parent Material that you can
    use as a base to make a wide variety of different looking children (Material instances).

    Fortnite takes advantage of this concept for its cosmetics. This allows developers to create a single
    cosmetic and then create many different versions of it using Material instances. This is used
    across not just skins but also extended onto lego cosmetic variants as well.

    This class represents a Material instance, which is said to be a child of a bigger parent Material.

    This class inherits from :class:`~fortnite_api.Hashable` and :class:`~fortnite_api.ReconstructAble`.

    .. versionchanged:: v3.1.0
        Moved from the now-deleted ``fortnite_api.material`` to ``fortnite_api.new_display_asset``.

    Attributes
    ----------
    id: :class:`str`
        The ID of the Material instance.
    primary_mode: :class:`fortnite_api.CosmeticCompatibleMode`
        The primary mode of the Material instance. This denotes what the cosmetic material instance is compatible with.
    product_tag: :class:`fortnite_api.ProductTag`
        The product tag of the Material instance.
    images: :class:`fortnite_api.MaterialInstanceImages`
        Represents some images of the Material instance, as they are rendered in game.
    colors: Optional[:class:`fortnite_api.MaterialInstanceColors`]
        Holds some metadata about the colors of the Material instance, such
        as the background color A and B, if it exists.
    scalings: :class:`dict`
        Some information about the scalings of the Material instance. This is a low level Unreal Engine 5
        information dump that is not commonly used, but is available for those who need it. It can
        contain information about the material background, density, zoom, streak multipliers, and spotlights.
    flags: :class:`dict`
        Any flags on the material instance.

        .. warning::

            This is always an empty dict, as there are no flags used at this time.
    """

    __slots__: tuple[str, ...] = (
        "id",
        "primary_mode",
        "product_tag",
        "images",
        "colors",
        "scalings",
        "flags",
    )

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.id: str = data["id"]
        self.primary_mode: CosmeticCompatibleMode = CosmeticCompatibleMode._from_str(data["primaryMode"])
        self.product_tag: ProductTag = ProductTag._from_str(data["productTag"])

        self.images: MaterialInstanceImages[HTTPClientT] = MaterialInstanceImages(data=data["images"], http=http)

        _colors = data.get("colors")
        self.colors: Optional[MaterialInstanceColors] = _colors and MaterialInstanceColors(data=_colors)
        self.scalings: dict[str, Any] = get_with_fallback(data, "scalings", dict)

        self.flags: dict[str, Any] = get_with_fallback(data, "flags", dict)  # This is always None at this time.


class NewDisplayAsset(Hashable, ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.NewDisplayAsset

    Represents a new display asset for a shop entry. A display asset is an asset that is
    used to visually represent a cosmetic item in the shop. This class inherits
    from :class:`~fortnite_api.ReconstructAble` and :class:`~fortnite_api.Hashable`.

    Attributes
    ----------
    id: :class:`str`
        The ID of the display asset.
    cosmetic_id: Optional[:class:`str`]
        The ID of the cosmetic item associated with the display asset, if any.
    material_instances: List[:class:`fortnite_api.MaterialInstance`]
        A list of material instances used by the display asset.
    render_images: List[:class:`fortnite_api.RenderImage`]
        A list of render images used by the display asset.

    .. versionchanged:: v3.1.0
        Renamed from ``ShopEntryNewDisplayAsset`` to a more generic ``NewDisplayAsset``
        to better reflect its usage across the API.
    """

    __slots__: tuple[str, ...] = ("id", "cosmetic_id", "material_instances", "render_images")

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.id: str = data["id"]
        self.cosmetic_id: Optional[str] = data.get("cosmeticId")
        self.material_instances: list[MaterialInstance[HTTPClientT]] = [
            MaterialInstance(data=instance, http=http)
            for instance in get_with_fallback(data, "materialInstances", list)
        ]
        self.render_images: list[RenderImage[HTTPClientT]] = [
            RenderImage(data=instance, http=http) for instance in get_with_fallback(data, "renderImages", list)
        ]
