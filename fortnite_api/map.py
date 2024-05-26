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

from typing import Any, Dict, Generic, List, Tuple

from .abc import Hashable
from .asset import Asset
from .http import HTTPClientT
from .proxies import TransformerListProxy

__all__: Tuple[str, ...] = ('Map', 'MapImages', 'POI', 'POILocation')


class MapImages(Generic[HTTPClientT]):
    """
    .. attributetable:: fortnite_api.MapImages

    Represents the images of a given POI map.

    Attributes
    ----------
    blank: :class:`fortnite_api.Asset`
        The asset pointing to an image of the map that does not contain any POI names.
    pois: :class:`fortnite_api.Asset`
        The asset pointing to an image of the map that contains the POI names.
    """

    __slots__: Tuple[str, ...] = ('blank', 'pois')

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.blank: Asset[HTTPClientT] = Asset(http=http, url=data['blank'])
        self.pois: Asset[HTTPClientT] = Asset(http=http, url=data['pois'])


class Map(Generic[HTTPClientT]):
    """
    .. attributetable:: fortnite_api.Map

    Represents a Fortnite map.

    Attributes
    ----------
    images: :class:`fortnite_api.MapImages`
        The images of the map.
    pois: List[:class:`fortnite_api.POI`]
        The list of POIs in the map.
    raw_data: :class:`dict`
        The raw data of the map.
    """

    __slots__: Tuple[str, ...] = ('images', 'pois', 'raw_data')

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.images: MapImages[HTTPClientT] = MapImages(data=data['images'], http=http)

        self.pois: List[POI] = TransformerListProxy(
            data['pois'],
            transform_data=lambda poi: POI(data=poi),
        )

        self.raw_data: Dict[str, Any] = data


class POI(Hashable):
    """
    .. attributetable:: fortnite_api.POI

    Represents a specific POI in a Fortnite map. This inherits from :class:`~fortnite_api.Hashable`.

    Attributes
    ----------
    id: :class:`str`
        The ID of the POI.
    name: :class:`str`
        The name of the POI.
    location: :class:`fortnite_api.POILocation`
        The location of the POI.
    """

    __slots__: Tuple[str, ...] = ('id', 'name', 'location')

    def __init__(self, *, data: Dict[str, Any]) -> None:
        self.id = data['id']
        self.name = data['name']
        self.location = POILocation(data=data['location'])


class POILocation:
    """
    .. attributetable:: fortnite_api.POILocation

    Holds the x, y, z coordinates of a POI in a Fortnite map.

    Attributes
    ----------
    x: :class:`float`
        The x coordinate.
    y: :class:`float`
        The y coordinate.
    z: :class:`float`
        The z coordinate.
    """

    __slots__: Tuple[str, ...] = ('x', 'y', 'z')

    def __init__(self, *, data: Dict[str, Any]) -> None:
        self.x: float = data['x']
        self.y: float = data['y']
        self.z: float = data['z']
