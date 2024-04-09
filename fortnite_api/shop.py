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
from typing import Any, Dict, Generic, List, Optional

from .abc import Hashable
from .asset import Asset
from .cosmetics import CosmeticBr, CosmeticCar, CosmeticInstrument, CosmeticLegoKit, CosmeticTrack
from .http import HTTPClientT
from .material import MaterialInstance
from .utils import get_with_fallback, parse_time


class ShopEntryBundle(Generic[HTTPClientT]):
    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.name: str = data['name']
        self.info: str = data['info']
        self.image: Asset[HTTPClientT] = Asset(url=data['image'], http=http)


class ShopEntryBanner:
    def __init__(self, *, data: Dict[str, Any]) -> None:
        self.value: str = data['value']
        self.intensity: str = data['intensity']
        self.backend_value: str = data['backendValue']


class ShopEntryLayout(Hashable, Generic[HTTPClientT]):
    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.id: str = data['id']
        self.name: str = data['name']
        self.category: Optional[str] = data.get('category')
        self.index: int = data['index']
        self.show_ineligible_offers: str = data['showIneligibleOffers']

        _background = data.get('background')
        self.background: Optional[Asset[HTTPClientT]] = _background and Asset(url=_background, http=http)


class ShopEntryNewDisplayAsset(Hashable, Generic[HTTPClientT]):
    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.id: str = data['id']
        self.cosmetic_id: Optional[str] = data.get('cosmeticId')
        self.material_instances: List[MaterialInstance[HTTPClientT]] = [
            MaterialInstance(data=instance, http=http) for instance in get_with_fallback(data, 'materialInstances', list)
        ]


class ShopEntry(Generic[HTTPClientT]):
    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.regular_price: int = data['regularPrice']
        self.final_price: int = data['finalPrice']

        _bundle = data.get('bundle')
        self.bundle: Optional[ShopEntryBundle[HTTPClientT]] = _bundle and ShopEntryBundle(data=_bundle, http=http)

        _banner = data.get('banner')
        self.banner: Optional[ShopEntryBanner] = _banner and ShopEntryBanner(data=_banner)

        self.giftable: bool = data['giftable']
        self.refundable: bool = data['refundable']
        self.sort_priority: int = data['sortPriority']
        self.layout_id: str = data['layoutId']
        self.layout: ShopEntryLayout[HTTPClientT] = ShopEntryLayout(data=data['layout'], http=http)
        self.dev_name: str = data['devName']
        self.offer_id: str = data['offerId']
        self.display_asset_path: Optional[str] = data.get('displayAssetPath')
        self.tile_size: str = data['tileSize']
        self.new_display_asset_path: str = data['newDisplayAssetPath']
        self.new_display_asset: ShopEntryNewDisplayAsset[HTTPClientT] = ShopEntryNewDisplayAsset(
            data=data['newDisplayAsset'], http=http
        )

        self.br_items: List[CosmeticBr[HTTPClientT]] = [
            CosmeticBr(data=item, http=http) for item in get_with_fallback(data, 'items', list)
        ]
        self.tracks: List[CosmeticTrack[HTTPClientT]] = [
            CosmeticTrack(data=item, http=http) for item in get_with_fallback(data, 'tracks', list)
        ]
        self.instruments: List[CosmeticInstrument[HTTPClientT]] = [
            CosmeticInstrument(data=item, http=http) for item in get_with_fallback(data, 'instruments', list)
        ]
        self.cars: List[CosmeticCar[HTTPClientT]] = [
            CosmeticCar(data=item, http=http) for item in get_with_fallback(data, 'cars', list)
        ]
        self.lego_kits: List[CosmeticLegoKit[HTTPClientT]] = [
            CosmeticLegoKit(data=item, http=http) for item in get_with_fallback(data, 'legoKits', list)
        ]


class Shop(Generic[HTTPClientT]):
    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.hash: str = data['hash']
        self.date: datetime.datetime = parse_time(data['date'])

        self.vbuck_icon: Asset[HTTPClientT] = Asset(url=data['vbuckIcon'], http=http)

        _entries = get_with_fallback(data, 'entries', list)
        self.entries: List[ShopEntry[HTTPClientT]] = [ShopEntry(data=item, http=http) for item in _entries]

        self.raw_data: Dict[str, Any] = data
