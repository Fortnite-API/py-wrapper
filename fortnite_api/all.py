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

from .cosmetics import CosmeticBr, CosmeticCar, CosmeticInstrument, CosmeticLegoKit, CosmeticTrack, VariantBean, VariantLego
from .http import HTTPClientT
from .proxies import TransformerListProxy
from .utils import get_with_fallback, simple_repr

__all__: Tuple[str, ...] = ('CosmeticsAll',)


@simple_repr
class CosmeticsAll(Generic[HTTPClientT]):
    """
    .. attributetable:: fortnite_api.CosmeticsAll

    A class that represents a request to fetch all cosmetics available in Fortnite.

    .. container:: operations

        .. describe:: len(x)

            Returns the total amount of cosmetics available.

        .. describe:: iter(x)

            Returns an iterator of the cosmetics, working through one unique cosmetic type before
            continuing onto the next. Works in the following
            order: :class:`~fortnite_api.CosmeticBr`, :class:`~fortnite_api.CosmeticTrack`,
            :class:`~fortnite_api.CosmeticInstrument`, :class:`~fortnite_api.CosmeticCar`,
            :class:`~fortnite_api.VariantLego`, :class:`~fortnite_api.CosmeticLegoKit`.

            .. code-block:: python3

                all_cosmetics = await client.fetch_all_cosmetics()
                for cosmetic in all_cosmetics:
                    print(cosmetic.id, cosmetic.type)

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

    Attributes
    ----------
    br: List[:class:`fortnite_api.CosmeticBr`]
        A list of all battle royale cosmetics.
    tracks: List[:class:`fortnite_api.CosmeticTrack`]
        A list of all track cosmetics.
    instruments: List[:class:`fortnite_api.CosmeticInstrument`]
        A list of all instrument cosmetics.
    cars: List[:class:`fortnite_api.CosmeticCar`]
        A list of all car cosmetics.
    lego: List[:class:`fortnite_api.VariantLego`]
        A list of all lego cosmetic variants.
    lego_kits: List[:class:`fortnite_api.CosmeticLegoKit`]
        A list of all lego kit cosmetics.
    raw_data: :class:`dict`
        The raw data of the request. Can be used to recreate the object without
        fetching the data again.
    """

    __slots__: Tuple[str, ...] = (
        '_http',
        'br',
        'tracks',
        'instruments',
        'cars',
        'lego',
        'lego_kits',
        'beans',
        'raw_data',
    )

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
        self.lego: TransformerListProxy[VariantLego[HTTPClientT]] = TransformerListProxy(
            _lego,
            lambda x: VariantLego(data=x, http=self._http),
        )

        _lego_kits = get_with_fallback(data, 'legoKits', list)
        self.lego_kits: TransformerListProxy[CosmeticLegoKit[HTTPClientT]] = TransformerListProxy(
            _lego_kits,
            lambda x: CosmeticLegoKit(data=x, http=self._http),
        )

        _beans = get_with_fallback(data, 'beans', list)
        self.beans: TransformerListProxy[VariantBean[HTTPClientT]] = TransformerListProxy(
            _beans,
            lambda x: VariantBean(data=x, http=self._http),
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
