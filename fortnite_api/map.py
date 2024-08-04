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

from typing import Any, Dict, List, Optional, Tuple

from .abc import Hashable, ReconstructAble
from .asset import Asset
from .http import HTTPClientT
from .proxies import TransformerListProxy
from .utils import simple_repr

__all__: Tuple[str, ...] = ('Map', 'MapImages', 'POI', 'POILocation')


@simple_repr
class MapImages(ReconstructAble[Dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.MapImages

    Represents the images of a given POI map. This inherits
    from :class:`~fortnite_api.ReconstructAble`.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

    Attributes
    ----------
    blank: :class:`fortnite_api.Asset`
        The asset pointing to an image of the map that does not contain any POI names.
    pois: :class:`fortnite_api.Asset`
        The asset pointing to an image of the map that contains the POI names.
    """

    __slots__: Tuple[str, ...] = ('blank', 'pois')

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.blank: Asset[HTTPClientT] = Asset(http=http, url=data['blank'])
        self.pois: Asset[HTTPClientT] = Asset(http=http, url=data['pois'])


@simple_repr
class Map(ReconstructAble[Dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.Map

    Represents a Fortnite map. This inherits from :class:`~fortnite_api.ReconstructAble`.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

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
        super().__init__(data=data, http=http)

        self.images: MapImages[HTTPClientT] = MapImages(data=data['images'], http=http)

        self.pois: List[POI[HTTPClientT]] = TransformerListProxy(
            data['pois'],
            transform_data=lambda poi: POI(data=poi, http=http),
        )

        self.raw_data: Dict[str, Any] = data


@simple_repr
class POI(Hashable, ReconstructAble[Dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.POI

    Represents a specific POI in a Fortnite map. This inherits from :class:`~fortnite_api.Hashable`
    and :class:`~fortnite_api.ReconstructAble`.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

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

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.id: str = data['id']
        self.name: Optional[str] = data.get('name')
        self.location: POILocation[HTTPClientT] = POILocation(data=data['location'], http=http)


@simple_repr
class POILocation(ReconstructAble[Dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.POILocation

    Holds the x, y, z coordinates of a POI in a Fortnite map. This inherits
    from :class:`~fortnite_api.ReconstructAble`.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

        .. describe:: iter(x)

            Returns a iter of the x, y, z coordinates.

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

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.x: float = data['x']
        self.y: float = data['y']
        self.z: float = data['z']

    def __iter__(self) -> Tuple[float, float, float]:
        return self.x, self.y, self.z
