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

from typing import Any, Dict, Optional, Tuple

from .abc import Hashable, ReconstructAble
from .asset import Asset
from .enums import CosmeticCompatibleMode
from .http import HTTPClientT
from .utils import get_with_fallback

__all__: Tuple[str, ...] = ('MaterialInstanceImages', 'MaterialInstanceColors', 'MaterialInstance')


class MaterialInstanceImages(Dict[str, Asset[HTTPClientT]]):
    """
    .. attributetable:: fortnite_api.MaterialInstanceImages

    Represents some images of a Material instance, as they are rendered in game. Although this class
    has concrete attributes, the API generates the keys dynamically. The most common keys are exposed as attributes, and all
    other keys are available through dictionary operations.

    This class inherits from :class:`dict`, and thus, supports all the operations that a normal
    dictionary does, such as indexing, iteration, etc.

    Attributes
    ----------
    offer_image: :class:`fortnite_api.Asset`
        The offer image of the Material instance. This is the image that is shown in the item shop.
    background: :class:`fortnite_api.Asset`
        The background of the Material instance. This is the background gradient of the material instance.
    """

    __slots__: Tuple[str, ...] = ('offer_image', 'background', 'texture')

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        # Pop off the keys as we set concrete attributes
        self.offer_image: Asset[HTTPClientT] = Asset(url=data.pop('OfferImage'), http=http)

        _background = data.pop('Background', None)
        self.background: Optional[Asset[HTTPClientT]] = _background and Asset(url=_background, http=http)

        # Transform all remaining keys into assets, and pass this along to the dict constructor
        super().__init__({key: Asset(url=value, http=http) for key, value in data.items()})


class MaterialInstanceColors(Dict[str, str]):
    """
    .. attributetable:: fortnite_api.MaterialInstanceColors

    Represents some metadata about the colors of a Material instance. Although the keys are dynamically generated in the API, the most common keys are exposed as attributes.

    This class inherits from :class:`dict`, and thus, supports all the operations that a normal dictionary does, such as indexing, iteration, etc.

    Attributes
    ----------
    background_color_a: Optional[:class:`str`]
        The first background color of the Material instance, if any.
    background_color_b: Optional[:class:`str`]
        The second background color of the Material instance, if any.
    fall_off_color: Optional[:class:`str`]
        The fall off color of the Material instance, if any.
    """

    __slots__: Tuple[str, ...] = ('background_color_a', 'background_color_b', 'fall_off_color')

    def __init__(self, *, data: Dict[str, Any]) -> None:
        self.background_color_a: Optional[str] = data.get('Background_Color_A')
        self.background_color_b: Optional[str] = data.get('Background_Color_B')
        self.fall_off_color: Optional[str] = data.get('FallOff_Color')
        super().__init__(data)


class MaterialInstance(Hashable, ReconstructAble[Dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.MaterialInstance

    Material instancing is a way to create a parent Material that you can
    use as a base to make a wide variety of different looking children (Material instances).

    Fortnite takes advantage of this concept for its cosmetics. This allows developers to create a single
    cosmetic and then create many different versions of it using Material instances. This is used
    across not just skins but also extended onto lego cosmetic variants as well.

    This class represents a Material instance, which is said to be a child of a bigger parent Material.

    This class inherits from :class:`~fortnite_api.Hashable` and :class:`~fortnite_api.ReconstructAble`.

    Attributes
    ----------
    id: :class:`str`
        The ID of the Material instance.
    primary_mode: :class:`fortnite_api.CosmeticCompatibleMode`
        The primary mode of the Material instance. This denotes what the cosmetic material instance is compatible with.
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

    __slots__: Tuple[str, ...] = ('id', 'primary_mode', 'images', 'colors', 'scalings', 'flags')

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.id: str = data['id']
        self.primary_mode: CosmeticCompatibleMode = CosmeticCompatibleMode._from_str(data['primaryMode'])

        self.images: MaterialInstanceImages[HTTPClientT] = MaterialInstanceImages(data=data['images'], http=http)

        _colors = data.get('colors')
        self.colors: Optional[MaterialInstanceColors] = _colors and MaterialInstanceColors(data=_colors)
        self.scalings: Dict[str, Any] = get_with_fallback(data, 'scalings', dict)

        self.flags: Dict[str, Any] = get_with_fallback(data, 'flags', dict)  # This is always None at this time.
