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

from typing import Any, Dict, Generic, List

from .cosmetics import CosmeticBr, CosmeticInstrument, CosmeticTrack
from .cosmetics.car import CosmeticCar
from .cosmetics.lego import CosmeticLego
from .cosmetics.lego_kit import CosmeticLegoKit
from .http import HTTPClientT
from .utils import get_with_fallback


class CosmeticsAll(Generic[HTTPClientT]):
    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self._http: HTTPClientT = http

        _br = get_with_fallback(data, 'br', list)
        self.br: List[CosmeticBr[HTTPClientT]] = [CosmeticBr(data=cosmetic, http=self._http) for cosmetic in _br]

        _tracks = get_with_fallback(data, 'tracks', list)
        self.tracks: List[CosmeticTrack[HTTPClientT]] = [CosmeticTrack(data=track, http=self._http) for track in _tracks]

        _instruments = get_with_fallback(data, 'instruments', list)
        self.instruments: List[CosmeticInstrument[HTTPClientT]] = [
            CosmeticInstrument(data=instrument, http=self._http) for instrument in _instruments
        ]

        _cars = get_with_fallback(data, 'cars', list)
        self.cars: List[CosmeticCar[HTTPClientT]] = [CosmeticCar(data=car, http=self._http) for car in _cars]

        _lego = get_with_fallback(data, 'lego', list)
        self.lego: List[CosmeticLego[HTTPClientT]] = [CosmeticLego(data=lego, http=self._http) for lego in _lego]

        _lego_kits = get_with_fallback(data, 'legoKits', list)
        self.lego_kits: List[CosmeticLegoKit[HTTPClientT]] = [
            CosmeticLegoKit(data=lego_kit, http=self._http) for lego_kit in _lego_kits
        ]

        self.raw_data: Dict[str, Any] = data
