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

from .utils import parse_time

from .http import HTTPClientT


class Shop(Generic[HTTPClientT]):
    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.hash: str = data['hash']
        self.date: datetime.datetime = parse_time(data['date'])

        self.vbuck_icon: Asset[HTTPClientT] = Asset(url=data['vbuckIcon'], http=http)

        _featured = data.get('featured')
        self.featured: Optional[ShopEntry[HTTPClientT]] = _featured and ShopEntry(data=_featured, http=http)

        self.raw_data: Dict[str, Any] = data


class ShopEntry(Generic[HTTPClientT]):
    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.name: str = data['name']
        self.entries: List[ShopEntryItem[HTTPClientT]] = [ShopEntryItem(data=item, http=http) for item in data['entries']]


class ShopEntryItem(Generic[HTTPClientT]):
    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.regular_price: int = data['regularPrice']
        self.final_price: int = data['finalPrice']

        _bundle = data.get('bundle')
        self.bundle: Optional[ShopEntryItemBundle[HTTPClientT]] = _bundle and ShopEntryItemBundle(data=_bundle, http=http)

        _banner = data.get('banner')
        self.banner: Optional[ShopEntryItemBanner[HTTPClientT]] = _banner and ShopEntryItemBanner(data=_banner, http=http)

        self.giftable: bool = data['giftable']
        self.refundable: bool = data['refundable']
        self.sort_priority: int = data['sortPriority']
        self.categories: Any = data['categories']  # Unknown at this time.
        self.section_id: str = data['sectionId']
        self.section: Any = data['section']  # Unknown at this time.
        self.layout: ShopEntryItemLayout[HTTPClientT] = ShopEntryItemLayout(data=data['layout'], http=http)
        self.dev_name: str = data['devName']
        self.offer_id: str = data['offerId']
        self.display_asset_path: str = data['displayAssetPath']
        self.tile_size: str = data['tileSize']
        self.new_display_asset_path: str = data['newDisplayAssetPath']
        self.newDisplayAsset: ShopEntryItemNewDisplayAsset[HTTPClientT] = ShopEntryItemNewDisplayAsset(
            data=data['newDisplayAsset'], http=http
        )


class ShopEntryItemBundle(Generic[HTTPClientT]):
    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.name: str = data['name']
        self.info: str = data['info']
        self.image: Asset[HTTPClientT] = Asset(url=data['image'], http=http)


class ShopEntryItemBanner(Generic[HTTPClientT]):
    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.value: str = data['value']
        self.intensity: str = data['intensity']
        self.backend_value: str = data['backendValue']


class ShopEntryItemLayout(Hashable, Generic[HTTPClientT]):
    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.id: str = data['id']
        self.name: str = data['name']
        self.category: str = data['category']
        self.index: int = data['index']
        self.show_ineligible_offers: str = data['showIneligibleOffers']

        _background = data.get('background')
        self.background: Optional[Asset[HTTPClientT]] = _background and Asset(url=_background, http=http)


class ShopEntryItemNewDisplayAsset(Generic[HTTPClientT]):
    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None: ...
