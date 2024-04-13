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

from typing import Any, Dict, Generic, Tuple

from .cosmetics import CosmeticBr, CosmeticInstrument, CosmeticTrack
from .cosmetics.car import CosmeticCar
from .cosmetics.lego import CosmeticLego
from .cosmetics.lego_kit import CosmeticLegoKit
from .http import HTTPClientT
from .proxies import TransformerListProxy
from .utils import get_with_fallback

__all__: Tuple[str, ...] = ('CosmeticsAll',)


class CosmeticsAll(Generic[HTTPClientT]):
    """A class that represents a request to get all cosmetics.

    .. container:: operations

        .. describe:: len(x)

            Returns the total amount of cosmetics.

        .. describe:: iter(x)

            Returns an iterator of the cosmetics. In the following
            order: battle royale, tracks, instruments, cars, lego, lego kits.

        .. describe:: for x in y

            Iterates over the cosmetics. In the following order:
            battle royale, tracks, instruments, cars, lego, lego kits.

    Attributes
    ----------
    br: List[:class:`CosmeticBr`]
        The battle royale cosmetics.
    tracks: List[:class:`CosmeticTrack`]
        The tracks cosmetics.
    instruments: List[:class:`CosmeticInstrument`]
        The instruments cosmetics.
    cars: List[:class:`CosmeticCar`]
        The cars cosmetics.
    lego: List[:class:`CosmeticLego`]
        The lego cosmetics.
    lego_kits: List[:class:`CosmeticLegoKit`]
        The lego kits cosmetics.
    raw_data: Dict[:class:`str`, Any]
        The raw data of the cosmetics.
    """

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self._http: HTTPClientT = http

        _br = get_with_fallback(data, 'br', list)
        self.br: TransformerListProxy[CosmeticBr[HTTPClientT]] = TransformerListProxy(
            _br,
            lambda x: CosmeticBr(data=x, http=self._http),
        )

        _tracks = get_with_fallback(data, 'tracks', list)
        self.tracks: TransformerListProxy[CosmeticTrack[HTTPClientT]] = TransformerListProxy(
            _tracks,
            lambda x: CosmeticTrack(data=x, http=self._http),
        )

        _instruments = get_with_fallback(data, 'instruments', list)
        self.instruments: TransformerListProxy[CosmeticInstrument[HTTPClientT]] = TransformerListProxy(
            _instruments,
            lambda x: CosmeticInstrument(data=x, http=self._http),
        )

        _cars = get_with_fallback(data, 'cars', list)
        self.cars: TransformerListProxy[CosmeticCar[HTTPClientT]] = TransformerListProxy(
            _cars,
            lambda x: CosmeticCar(data=x, http=self._http),
        )

        _lego = get_with_fallback(data, 'lego', list)
        self.lego: TransformerListProxy[CosmeticLego[HTTPClientT]] = TransformerListProxy(
            _lego,
            lambda x: CosmeticLego(data=x, http=self._http),
        )

        _lego_kits = get_with_fallback(data, 'legoKits', list)
        self.lego_kits: TransformerListProxy[CosmeticLegoKit[HTTPClientT]] = TransformerListProxy(
            _lego_kits,
            lambda x: CosmeticLegoKit(data=x, http=self._http),
        )

        self.raw_data: Dict[str, Any] = data

    def __iter__(self):
        for br in self.br:
            yield br

        for track in self.tracks:
            yield track

        for instrument in self.instruments:
            yield instrument

        for car in self.cars:
            yield car

        for lego in self.lego:
            yield lego

        for lego_kit in self.lego_kits:
            yield lego_kit

    def __len__(self):
        return (
            len(self.br) + len(self.tracks) + len(self.instruments) + len(self.cars) + len(self.lego) + len(self.lego_kits)
        )
