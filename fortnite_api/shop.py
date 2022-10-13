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

from typing import TYPE_CHECKING, Dict, Any, Optional, Tuple, List

from .cosmetics import BrCosmetic
from .utils import parse_time

if TYPE_CHECKING:
    import datetime


class BrShop:
    """Represents a Battle Royale shop.

    Attributes
    -----------
    hash: :class:`str`
        The hash of the shop.
    date: :class:`datetime.datetime`
        The timestamp of the .
    featured: Optional[List[:class:`BrShopEntry`]]
        A list of all featured entries.
    daily: Optional[List[:class:`BrShopEntry`]]
        A list of all daily entries.
    votes: Optional[List[:class:`BrShopEntry`]]
        A list of all vote entries.
    vote_winners: Optional[List[:class:`BrShopEntry`]]
        A list of all vote winner.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    __slots__: Tuple[str, ...] = (
        'hash',
        'date',
        'featured',
        'daily',
        'special_featured',
        'special_daily',
        'votes',
        'vote_winners',
        'raw_data',
    )

    def __init__(self, data: Dict[str, Any]) -> None:
        self.hash: str = data['hash']
        self.date: datetime.datetime = parse_time(data['date'])

        self.featured: Optional[BrShopSection] = (featured := data.get('featured')) and BrShopSection(featured)
        self.daily: Optional[BrShopSection] = (daily := data.get('daily')) and BrShopSection(daily)
        self.special_featured: Optional[BrShopSection] = (special_featured := data.get('specialFeatured')) and BrShopSection(
            special_featured
        )
        self.special_daily: Optional[BrShopSection] = (special_daily := data.get('specialDaily')) and BrShopSection(
            special_daily
        )
        self.votes: Optional[BrShopSection] = (votes := data.get('votes')) and BrShopSection(votes)
        self.vote_winners: Optional[BrShopSection] = (vote_winners := data.get('voteWinners')) and BrShopSection(
            vote_winners
        )
        self.raw_data: Dict[str, Any] = data


class BrShopSection:
    __slots__: Tuple[str, ...] = ('name', 'entries', 'raw_data')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.name: str = data['name']
        self.entries: List[BrShopEntry] = [BrShopEntry(entry_data) for entry_data in data.get('entries', [])]
        self.raw_data: Dict[str, Any] = data


class BrShopEntry:
    """Represents a Battle Royale shop entry.

    Attributes
    -----------
    regular_price: :class:`int`
        The internal price.
    final_price: :class:`int`
        The price which is shown in-game.
    discount: :class:`int`
        The discount on the item.
    giftable: :class:`bool`
        Whether the item is giftable.
    refundable: :class:`bool`
        Whether the item is refundable.
    panel: :class:`int`
        The id of the panel in the featured section. -1 if the item is in no panel.
    sort_priority: :class:`int`
        The sort priority in the featured panels.
    banner: Optional[:class:`str`]
        The text of the banner. This text is shown in a arrow in-game.
    items: List[:class:`BrCosmetic`]
        A list of all cosmetics you get when you buy.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    __slots__: Tuple[str, ...] = (
        'regular_price',
        'final_price',
        'bundle',
        'banner',
        'giftable',
        'refundable',
        'sort_priority',
        'categories',
        'section_id',
        'section',
        'dev_name',
        'offer_id',
        'display_asset_path',
        'tile_size',
        'new_display_asset_path',
        'new_display_asset',
        'items',
        'raw_data',
    )

    def __init__(self, data: Dict[str, Any]) -> None:
        self.regular_price: Optional[int] = data.get('regularPrice')
        self.final_price: Optional[int] = data.get('finalPrice')

        self.bundle: Optional[BrShopBundle] = (bundle := data.get('bundle')) and BrShopBundle(bundle)
        self.banner: Optional[BrShopBanner] = (banner := data.get('banner')) and BrShopBanner(banner)
        self.giftable: Optional[bool] = data.get('giftable')
        self.refundable: Optional[bool] = data.get('refundable')
        self.sort_priority: Optional[int] = data.get('sortPriority')
        self.categories: Optional[List[str]] = data.get('categories')
        self.section_id: Optional[int] = data.get('sectionId')

        self.section: Optional[BrShopSection] = (section := data.get('section')) and BrShopSection(section)
        self.dev_name: Optional[str] = data.get('devName')
        self.offer_id: Optional[int] = data.get('offerId')
        self.display_asset_path: Optional[str] = data.get('displayAssetPath')
        self.tile_size: Optional[str] = data.get('tileSize')
        self.new_display_asset_path: Optional[str] = data.get('newDisplayAssetPath')
        self.new_display_asset: Optional[str] = data.get('newDisplayAsset')
        self.items: List[BrCosmetic] = [BrCosmetic(item_data) for item_data in data.get('items', [])]
        self.raw_data: Dict[str, Any] = data

    @property
    def discount(self) -> Optional[int]:
        return self.regular_price and self.final_price and self.regular_price - self.final_price


class BrShopBundle:

    __slots__: Tuple[str, ...] = ('name', 'info', 'image', 'raw_data')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.name = data.get('name')
        self.info = data.get('info')
        self.image = data.get('image')
        self.raw_data = data


class BrShopBanner:

    __slots__: Tuple[str, ...] = ('value', 'intensity', 'backend_value', 'raw_data')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.value = data.get('value')
        self.intensity = data.get('intensity')
        self.backend_value = data.get('backendValue')
        self.raw_data = data


class BrShopSectionNew:

    __slots__: Tuple[str, ...] = (
        'id',
        'name',
        'index',
        'landing_priority',
        'sort_offers_by_ownership',
        'show_ineligible_offers',
        'show_ineligible_offers_if_giftable',
        'show_timer',
        'enable_toast_notification',
        'hidden',
    )

    def __init__(self, data: Dict[str, Any]) -> None:
        self.id: str = data['id']
        self.name: str = data['name']
        self.index: int = data['index']
        self.landing_priority: int = data['landingPriority']
        self.sort_offers_by_ownership: bool = data['sortOffersByOwnership']
        self.show_ineligible_offers: bool = data['showIneligibleOffers']
        self.show_ineligible_offers_if_giftable: bool = data['showIneligibleOffersIfGiftable']
        self.show_timer: bool = data['showTimer']
        self.enable_toast_notification: bool = data['enableToastNotification']
        self.hidden: bool = data['hidden']


class BrShopNewDisplayAsset:

    __slots__: Tuple[str, ...] = ('id', 'material_instances')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.id: str = data['id']
        self.material_instances: List[BrShopMaterialInstance] = [
            BrShopMaterialInstance(mi) for mi in data.get('materialInstances', [])
        ]


class BrShopMaterialInstance:

    __slots__: Tuple[str, ...] = ('id', 'images', 'colors', 'scalings')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.id: str = data['id']
        self.images: str = data['images']
        self.colors = data['colors']
        self.scalings = data['scalings']
