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

from typing import Any, Dict, Generic, Optional, Tuple

from .abc import Hashable
from .asset import Asset
from .enums import CosmeticCompatibleMode
from .http import HTTPClientT
from .utils import get_with_fallback

__all__: Tuple[str, ...] = ('MaterialInstanceImages', 'MaterialInstanceColors', 'MaterialInstance')


class MaterialInstanceImages(Generic[HTTPClientT]):
    """Represents some images of a Material instance, as they are rendered in game.

    Attributes
    ----------
    offer_image: :class:`Asset`
        The offer image of the Material instance. This is the image that is shown in the battle royale shop.
    background: :class:`Asset`
        The background of the Material instance. This is the background gradient of the material instance.
    """

    __slots__: Tuple[str, ...] = ('offer_image', 'background')

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.offer_image: Asset[HTTPClientT] = Asset(url=data['OfferImage'], http=http)

        _background = data.get('Background')
        self.background: Optional[Asset[HTTPClientT]] = _background and Asset(url=_background, http=http)


class MaterialInstanceColors:
    """Represents some metadata about the colors of a Material instance. Every material instance image
    has a background gradient, made up of a background color A and background color B that falls off to a
    specific color. This class represents that information.

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


class MaterialInstance(Hashable, Generic[HTTPClientT]):
    """Material instancing is a way to create a parent Material that you can
    use as a base to make a wide variety of different looking children (Material instances).

    Fortnite takes advantage of this concept for its cosmetics. This allows developers to create a single
    cosmetic and then create many different versions of it using Material instances. This is used
    across not just skins but also extended onto lego cosmetics as well.

    This class represents a Material instance, which is said to be a child of a bigger parent Material.

    Attributes
    ----------
    id: :class:`str`
        The ID of the Material instance.
    primary_mode: :class:`CosmeticCompatibleMode`
        The primary mode of the Material instance. This denotes what the cosmetic material instance is compatible with.
    images: :class:`MaterialInstanceImages`
        Represents some images of the Material instance, as they are rendered in game.
    colors: Optional[:class:`MaterialInstanceColors`]
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
        self.id: str = data['id']
        self.primary_mode: CosmeticCompatibleMode = CosmeticCompatibleMode(data['primaryMode'])

        self.images: MaterialInstanceImages[HTTPClientT] = MaterialInstanceImages(data=data['images'], http=http)

        _colors = data.get('colors')
        self.colors: Optional[MaterialInstanceColors] = _colors and MaterialInstanceColors(data=_colors)
        self.scalings: Dict[str, Any] = get_with_fallback(data, 'scalings', dict)

        self.flags: Dict[str, Any] = get_with_fallback(data, 'flags', dict)  # This is always None at this time.
