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

import dataclasses
from typing import Any, Dict, Generic, Optional, Tuple

from .abc import Hashable
from .asset import Asset
from .enums import CosmeticCompatibleMode
from .http import HTTPClientT


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
        self.background: Asset[HTTPClientT] = Asset(url=data['Background'], http=http)


class MaterialInstanceColors:
    """Represents some metadata about the colors of a Material instance. Every material instance image
    has a background gradient, made up of a background color A and background color B that falls off to a
    specific color. This class represents that information.

    Attributes
    ----------
    background_color_a: :class:`str`
        The first background color of the Material instance.
    background_color_b: :class:`str`
        The second background color of the Material instance.
    fall_off_color: :class:`str`
        The fall off color of the Material instance.
    """

    __slots__: Tuple[str, ...] = ('background_color_a', 'background_color_b', 'fall_off_color')

    def __init__(self, *, data: Dict[str, Any]) -> None:
        self.background_color_a: str = data['BackgroundColorA']
        self.background_color_b: str = data['BackgroundColorB']
        self.fall_off_color: str = data['FallOff_Color']


@dataclasses.dataclass(slots=True, frozen=True)
class ScalingsInfo:
    """This class represents some information about specific scaling attributes of a Material instance.

    In specific, this class represents the gradient and spotlight of a Material instance.

    Attributes
    ----------
    hardness: :class:`float`
        The hardness of the scaling attribute.
    position_x: :class:`float`
        The position of the scaling attribute on the x-axis.
    position_y: :class:`float`
        The position of the scaling attribute on the y-axis.
    size: :class:`float`
        The size of the scaling attribute.
    intensity: Optional[:class:`float`]
        The intensity of the scaling attribute. This will be ``None`` if the info is about a gradient,
        otherwise it will be a float.
    """

    hardness: float
    position_x: float
    position_y: float
    size: float
    intensity: Optional[float] = None


class MaterialInstanceScalings:
    """Represents some information about the scaling of a Material instance."""

    def __init__(self, *, data: Dict[str, Any]) -> None:
        self.background_balance: Optional[float] = data.get('Background-Balance')
        self.vignette_density: Optional[float] = data.get('Vignette Density')
        self.vignette_radius: Optional[float] = data.get('Vignette Radius')
        self.vignette_strength: Optional[float] = data.get('Vignette-Strength')

        self.density_enhanced: Optional[float] = data.get('DensityEnhanced')
        self.radius_enhanced: Optional[float] = data.get('RadiusEnhanced')

        self.offset_image_x: Optional[float] = data.get('OffsetImage_X')
        self.offset_image_y: Optional[float] = data.get('OffsetImage_Y')

        self.zoom_image_percent: Optional[float] = data.get('ZoomImage_Percent')
        self.refraction_depth_bias: Optional[float] = data.get('RefractionDepthBias')

        self.effect_bump_multiply: Optional[float] = data.get('Effect-Bump-Multiply')
        self.effect_time_factor: Optional[float] = data.get('Effect-Time-Factor')

        self.sine_offset: Optional[float] = data.get('Sine Offset')
        self.streak_angle: Optional[float] = data.get('Streak Angle')
        self.streak_power_angle: Optional[float] = data.get('Streak Power Angle')

        # TODO: Move these into objects? streak_X objects?
        self.streak_g_multiply_max: Optional[float] = data.get('Streak-G-Multiply-Max')
        self.streak_g_multiply_min: Optional[float] = data.get('Streak-G-Multiply-Min')
        self.streak_g_power_max: Optional[float] = data.get('Streak-G-Power-Max')
        self.streak_g_power_min: Optional[float] = data.get('Streak-G-Power-Min')
        self.streak_g_u_offset: Optional[float] = data.get('Streak-G-U-Offset')
        self.streak_g_u_tile: Optional[float] = data.get('Streak-G-U-Tile')
        self.streak_g_v_offset: Optional[float] = data.get('Streak-G-V-Offset')
        self.streak_g_v_tile: Optional[float] = data.get('Streak-G-V-Tile')
        self.streak_r_multiply_max: Optional[float] = data.get('Streak-R-Multiply-Max')
        self.streak_r_multiply_min: Optional[float] = data.get('Streak-R-Multiply-Min')
        self.streak_r_power_max: Optional[float] = data.get('Streak-R-Power-Max')
        self.streak_r_power_min: Optional[float] = data.get('Streak-R-Power-Min')
        self.streak_r_u_offset: Optional[float] = data.get('Streak-R-U-Offset')
        self.streak_r_u_tile: Optional[float] = data.get('Streak-R-U-Tile')
        self.streak_r_v_offset: Optional[float] = data.get('Streak-R-V-Offset')
        self.streak_r_v_tile: Optional[float] = data.get('Streak-R-V-Tile')

        # TODO: These must be made optional (add check for if they are all none then don't show)
        self.gradient: ScalingsInfo = ScalingsInfo(
            hardness=data['Gradient_Hardness'],
            position_x=data['Gradient_Position_X'],
            position_y=data['Gradient_Position_Y'],
            size=data['Gradient_Size'],
        )

        # TODO These must be made optional (add check for if they are all none then don't show)
        self.spotlight: ScalingsInfo = ScalingsInfo(
            hardness=data['Spotlight_Hardness'],
            intensity=data['Spotlight_Intensity'],
            position_x=data['Spotlight_Position_X'],
            position_y=data['Spotlight_Position_Y'],
            size=data['Spotlight_Size'],
        )

        self.falloff_color_fill_percent: Optional[float] = data.get('FallOffColor_Fill_Percent')
        self.falloff_color_position: Optional[float] = data.get('FallOffColor_Postion')
        self.offset_image_y_compensation: Optional[float] = data.get('OffsetImage_Y_Compensation')


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
    colors: :class:`MaterialInstanceColors`
        Holds some metadata about the colors of the Material instance.
    scalings: Optional[:class:`MaterialInstanceScalings`]
        Some information about the scalings of the Material instance, if any.
    flags: None
        The flags of the material instance.

        .. warning::

            This is always None, as the flags are unknown at this time.
    """

    __slots__: Tuple[str, ...] = ('id', 'primary_mode', 'images', 'colors', 'scalings', 'flags')

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.id: str = data['id']
        self.primary_mode: CosmeticCompatibleMode = CosmeticCompatibleMode(data['primaryMode'])

        self.images: MaterialInstanceImages[HTTPClientT] = MaterialInstanceImages(data=data['images'], http=http)
        self.colors: MaterialInstanceColors = MaterialInstanceColors(data=data['colors'])

        _scalings = data.get('scalings')
        self.scalings: Optional[MaterialInstanceScalings] = _scalings and MaterialInstanceScalings(data=_scalings)

        self.flags: None = data['flags']  # This is always None at this time.
