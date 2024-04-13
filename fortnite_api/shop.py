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
from typing import Any, Dict, Generic, List, Optional, Tuple

from .abc import Hashable
from .asset import Asset
from .cosmetics import CosmeticBr, CosmeticCar, CosmeticInstrument, CosmeticLegoKit, CosmeticTrack
from .enums import BannerIntensity, TileSize
from .http import HTTPClientT
from .material import MaterialInstance
from .utils import get_with_fallback, parse_time

__all__: Tuple[str, ...] = (
    'ShopEntryBundle',
    'ShopEntryBanner',
    'ShopEntryLayout',
    'ShopEntryNewDisplayAsset',
    'ShopEntry',
    'Shop',
)


class ShopEntryBundle(Generic[HTTPClientT]):
    """Represents a shop entry bundle.

    Attributes
    ----------
    name: :class:`str`
        The name of the bundle.
    info: :class:`str`
        The information of the bundle.
    image: :class:`fortnite_api.Asset`
        The image of the bundle.
    """

    __slots__: Tuple[str, ...] = ('name', 'info', 'image')

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.name: str = data['name']
        self.info: str = data['info']
        self.image: Asset[HTTPClientT] = Asset(url=data['image'], http=http)


class ShopEntryBanner:
    """A class to represent a shop entry banner.

    Attributes
    ----------
    value: :class:`str`
        The text of the banner.
    intensity: :class:`fortnite_api.BannerIntensity`
        The intensity of the banner.
    backend_value: :class:`str`
        The backend value of the banner.
    """

    __slots__: Tuple[str, ...] = ('value', 'intensity', 'backend_value')

    def __init__(self, *, data: Dict[str, Any]) -> None:
        self.value: str = data['value']
        self.intensity: BannerIntensity = BannerIntensity(data['intensity'])
        self.backend_value: str = data['backendValue']


class ShopEntryLayout(Hashable, Generic[HTTPClientT]):
    """Represents the layout of a shop entry.

    Attributes
    ----------
    id: :class:`str`
        The ID of the layout.
    name: :class:`str`
        The name of the layout.
    category: Optional[:class:`str`]
        The category of the layout, if any.
    index: :class:`int`
        The index of the layout.
    show_ineligible_offers: :class:`str`
        Whether ineligible offers are displayed in the layout or not.
    background: Optional[:class:`fortnite_api.Asset`]
        The background asset of the layout, if any.
    """

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.id: str = data['id']
        self.name: str = data['name']
        self.category: Optional[str] = data.get('category')
        self.index: int = data['index']
        self.show_ineligible_offers: str = data['showIneligibleOffers']

        _background = data.get('background')
        self.background: Optional[Asset[HTTPClientT]] = _background and Asset(url=_background, http=http)


class ShopEntryNewDisplayAsset(Hashable, Generic[HTTPClientT]):
    """Represents a new display asset for a shop entry. A display asset is an asset that is
    used to visually represent a cosmetic item in the shop.

    Attributes
    ----------
    id: :class:`str`
        The ID of the display asset.
    cosmetic_id: Optional[:class:`str`]
        The ID of the cosmetic item associated with the display asset, if any.
    material_instances: List[:class:`fortnite_api.MaterialInstance`]
        A list of material instances used by the display asset.
    """

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.id: str = data['id']
        self.cosmetic_id: Optional[str] = data.get('cosmeticId')
        self.material_instances: List[MaterialInstance[HTTPClientT]] = [
            MaterialInstance(data=instance, http=http) for instance in get_with_fallback(data, 'materialInstances', list)
        ]


class ShopEntry(Generic[HTTPClientT]):
    """Represents an item shop entry. Each entry in the shop contains
    related cosmetics that are available in the shop.

    Attributes
    ----------
    regular_price: :class:`int`
        The regular price of the entry.
    final_price: :class:`int`
        The final price of the entry. This is in case it is on sale.
    bundle: Optional[:class:`fortnite_api.ShopEntryBundle`]
        The bundle that this entry belongs to, if any.
    banner: Optional[:class:`fortnite_api.ShopEntryBanner`]
        The banner information for this shop entry, if any.
    giftable: :class:`bool`
        Whether this entry is giftable.
    refundable: :class:`bool`
        Whether this entry is refundable.
    sort_priority: :class:`int`
        The sort priority of this entry.
    layout_id: :class:`str`
        The layout ID of this entry.
    layout: :class:`fortnite_api.ShopEntryLayout`
        The layout of this entry.
    dev_name: :class:`str`
        The internal dev name of this entry.
    offer_id: :class:`str`
        The offer ID of this entry.
    display_asset_path: Optional[:class:`str`]
        The display asset path of this entry.
    tile_size: :class:`fortnite_api.TileSize`
        The tile size of this entry.
    new_display_asset_path: :class:`str`
        The new display asset path of this entry.
    new_display_asset: :class:`fortnite_api.ShopEntryNewDisplayAsset`
        The new display asset of this entry.
    br_items: List[:class:`fortnite_api.CosmeticBr`]
        The Battle Royale cosmetics in this entry.
    tracks: List[:class:`fortnite_api.CosmeticTrack`]
        The tracks in this entry.
    instruments: List[:class:`fortnite_api.CosmeticInstrument`]
        The instruments in this entry.
    cars: List[:class:`fortnite_api.CosmeticCar`]
        The cars in this entry.
    lego_kits: List[:class:`fortnite_api.CosmeticLegoKit`]
        The LEGO kits in this entry.
    """

    __slots__: Tuple[str, ...] = (
        'regular_price',
        'final_price',
        'bundle',
        'banner',
        'giftable',
        'refundable',
        'sort_priority',
        'layout_id',
        'layout',
        'dev_name',
        'offer_id',
        'display_asset_path',
        'tile_size',
        'new_display_asset_path',
        'new_display_asset',
        'br_items',
        'tracks',
        'instruments',
        'cars',
        'lego_kits',
    )

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

        _tile_size: str = data['tileSize']

        # A check to correct an Epic games spelling mistake.
        if _tile_size.lower() == 'nomal':
            _tile_size = 'Normal'

        self.tile_size: TileSize = TileSize(_tile_size)

        self.new_display_asset_path: str = data['newDisplayAssetPath']

        _new_display_asset = data.get('newDisplayAsset')
        self.new_display_asset: Optional[ShopEntryNewDisplayAsset[HTTPClientT]] = (
            _new_display_asset and ShopEntryNewDisplayAsset(data=data['newDisplayAsset'], http=http)
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
    """Represents the Fortnite shop.

    Attributes
    ----------
    hash: :class:`str`
        A unique hash that represents this shop.
    date: :class:`datetime.datetime`
        The date when this shop was last updated.
    vbuck_icon: :class:`fortnite_api.Asset`
        An asset of the V-buck icon.
    entries: List[:class:`fortnite_api.ShopEntry`]
        A list of shop entries. Each entry contains cosmetics that are available in the shop.
    raw_data: :class:`dict`
        The raw data of the shop.
    """

    __slots__: Tuple[str, ...] = ('hash', 'date', 'vbuck_icon', 'entries', 'raw_data')

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.hash: str = data['hash']
        self.date: datetime.datetime = parse_time(data['date'])

        self.vbuck_icon: Asset[HTTPClientT] = Asset(url=data['vbuckIcon'], http=http)

        _entries = get_with_fallback(data, 'entries', list)
        self.entries: List[ShopEntry[HTTPClientT]] = [ShopEntry(data=item, http=http) for item in _entries]

        self.raw_data: Dict[str, Any] = data
