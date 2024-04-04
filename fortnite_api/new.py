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

import datetime
from typing import Any, Generic, Dict, List, Optional

from .cosmetics import CosmeticT, CosmeticBr, CosmeticTrack, CosmeticInstrument, CosmeticCar, CosmeticLego, CosmeticLegoKit
from .utils import parse_time
from .enums import CosmeticType
from .http import HTTPClientT


class NewCosmetic(Generic[CosmeticT]):
    """Represents a response from the new cosmetics endpoint for a given cosmetic type. The types are as follows:

    - ``CosmeticType.BR`` -> List of :class:`CosmeticBr`
    - ``CosmeticType.TRACKS`` -> List of :class:`CosmeticTrack`
    - ``CosmeticType.INSTRUMENTS`` -> List of :class:`CosmeticInstrument`
    - ``CosmeticType.CARS`` -> List of :class:`CosmeticCar`
    - ``CosmeticType.LEGO`` -> List of :class:`CosmeticLego`
    - ``CosmeticType.LEGO_KITS`` -> List of :class:`CosmeticLegoKit`

    Attributes
    ----------
    type: :class:`CosmeticType`
        The type of new cosmetics displayed.
    hash: Optional[:class:`str`]
        The hash of the new cosmetics. Can be ``None`` if no
        new cosmetics have been given for the cosmetic type.
    last_addition: :class:`datetime.datetime`
        The last addition of new cosmetics.
    items: List[:class:`BrCosmetic`]
        The new cosmetics. This corresponds to the type of new cosmetics.
        Can be empty if no new cosmetics have been given.
    """

    def __init__(
        self,
        *,
        type: CosmeticType,
        hash: Optional[str] = None,
        last_addition: datetime.datetime,
        items: List[CosmeticT],
        http: HTTPClientT,
    ) -> None:
        self._http: HTTPClientT = http

        self.type: CosmeticType = type
        self.hash: Optional[str] = hash
        self.last_addition: datetime.datetime = last_addition
        self.items: List[CosmeticT] = items


class NewBrCosmetics(NewCosmetic[CosmeticBr[HTTPClientT]]):
    """Represents a returned response from the new BR cosmetics endpoint.

    This inherits from :class:`NewCosmetic`.

    Attributes
    ----------
    build: :class:`str`
        The build of Fortnite that these cosmetics were added in.
    previous_build: :class:`str`
        The previous build of Fortnite.
    date: :class:`datetime.datetime`
        The date of the new cosmetics.
    raw_data: Dict[:class:`str`, Any]
        The raw data of the new cosmetics.
    """

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        items: List[CosmeticBr[HTTPClientT]] = [CosmeticBr(data=item, http=http) for item in data['items']]

        super().__init__(
            type=CosmeticType.BR,
            hash=data['hash'],
            last_addition=parse_time(data['lastAddition']),
            items=items,
            http=http,
        )

        # Extend this for the endpoint specific data
        self.build: str = data['build']
        self.previous_build: str = data['previousBuild']
        self.date: datetime.datetime = parse_time(data['date'])
        self.raw_data: Dict[str, Any] = data


class NewCosmetics(Generic[HTTPClientT]):
    """Represents a response from the new cosmetics endpoint.

    Attributes
    ----------
    build: :class:`str`
        The build of Fortnite that these cosmetics were added in.
    previous_build: :class:`str`
        The previous build of Fortnite.
    date: :class:`datetime.datetime`
        The date of the new cosmetics.
    global_hash: :class:`str`
        The combined hash of all new cosmetics.
    global_last_addition: :class:`datetime.datetime`
        The last time a new cosmetic was added.
    br: :class:`NewCosmetic`
        The new BR cosmetics.
    tracks: :class:`NewCosmetic`
        The new track cosmetics.
    instruments: :class:`NewCosmetic`
        The new instrument cosmetics.
    cars: :class:`NewCosmetic`
        The new car cosmetics.
    lego: :class:`NewCosmetic`
        The new lego cosmetics.
    lego_kits: :class:`NewCosmetic`
        The new lego kit cosmetics.
    """

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self._http: HTTPClientT = http

        self.build: str = data['build']
        self.previous_build: str = data['previousBuild']
        self.date: datetime.datetime = parse_time(data['date'])
        self.global_hash: str = data['hashes']['all']
        self.global_last_addition: datetime.datetime = parse_time(data['lastAdditions']['all'])

        hashes = data['hashes']
        last_additions = data['lastAdditions']
        items = data['items']

        br_items: List[Dict[str, Any]] = items['br'] or []
        self.br: NewCosmetic[CosmeticBr[HTTPClientT]] = NewCosmetic(
            type=CosmeticType.BR,
            hash=hashes['br'],
            last_addition=parse_time(last_additions['br']),
            items=[CosmeticBr(data=item, http=http) for item in br_items],
            http=self._http,
        )

        track_items: List[Dict[str, Any]] = items['tracks'] or []
        self.tracks: NewCosmetic[CosmeticTrack[HTTPClientT]] = NewCosmetic(
            type=CosmeticType.TRACKS,
            hash=hashes['tracks'],
            last_addition=parse_time(last_additions['tracks']),
            items=[CosmeticTrack(data=item, http=self._http) for item in track_items],
            http=self._http,
        )

        instrument_items: List[Dict[str, Any]] = items['instruments'] or []
        self.instruments: NewCosmetic[CosmeticInstrument[HTTPClientT]] = NewCosmetic(
            type=CosmeticType.INSTRUMENTS,
            hash=hashes['instruments'],
            last_addition=parse_time(last_additions['instruments']),
            items=[CosmeticInstrument(data=item, http=self._http) for item in instrument_items],
            http=self._http,
        )

        car_items: List[Dict[str, Any]] = items['cars'] or []
        self.cars: NewCosmetic[CosmeticCar[HTTPClientT]] = NewCosmetic(
            type=CosmeticType.CARS,
            hash=hashes['cars'],
            last_addition=parse_time(last_additions['cars']),
            items=[CosmeticCar(data=item, http=self._http) for item in car_items],
            http=self._http,
        )

        lego_items: List[Dict[str, Any]] = items['lego'] or []
        self.lego: NewCosmetic[CosmeticLego[HTTPClientT]] = NewCosmetic(
            type=CosmeticType.LEGO,
            hash=hashes['lego'],
            last_addition=parse_time(last_additions['lego']),
            items=[CosmeticLego(data=item, http=self._http) for item in lego_items],
            http=self._http,
        )

        lego_kit_items: List[Dict[str, Any]] = items['legoKits'] or []
        self.lego_kits: NewCosmetic[CosmeticLegoKit[HTTPClientT]] = NewCosmetic(
            type=CosmeticType.LEGO_KITS,
            hash=hashes['legoKits'],
            last_addition=parse_time(last_additions['legoKits']),
            items=[CosmeticLegoKit(data=item, http=self._http) for item in lego_kit_items],
            http=self._http,
        )
