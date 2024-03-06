from datetime import datetime
from typing import List, Optional, Union

from .cosmetics import BrCosmetic, CarCosmetic, InstrumentCosmetic, JamTrack
from .enums import ShopTileSize, CosmeticCompatibleMode


class Shop:

    def __init__(self, data: dict):
        self.hash: str = data['hash']
        self.date: datetime = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S%z')
        self.entries: List[ShopEntry] = [ShopEntry(entry) for entry in data['entries'] or []]
        self.raw_data: dict = data


class ShopEntry:

    def __init__(self, data: dict):
        self.regular_price: int = data['regularPrice']
        self.final_price: int = data['finalPrice']
        self.bundle: Optional[ShopBundle] = ShopBundle(data['bundle']) if data['bundle'] else None
        self.banner: Optional[ShopBanner] = ShopBanner(data['banner']) if data['banner'] else None
        self.giftable: bool = data['giftable']
        self.refundable: bool = data['refundable']
        self.sort_priority: int = data['sortPriority']
        self.layout_id: str = data['layoutId']
        self.layout: Optional[ShopLayout] = ShopLayout(data['layout']) if data['layout'] else None
        self.dev_name: str = data['devName']
        self.offer_id: str = data['offerId']
        self.display_asset_path: Optional[str] = data['displayAssetPath']
        try:
            self.tile_size: ShopTileSize = ShopTileSize(data['tileSize'])
        except ValueError:
            # This is a fix, because Epic believes that they should spell "normal" as "nomal"
            self.tile_size: ShopTileSize = ShopTileSize.NORMAL
        self.new_display_asset_path: Optional[str] = data['newDisplayAssetPath']
        self.new_display_asset: Optional[ShopNewDisplayAsset] = ShopNewDisplayAsset(data['newDisplayAsset']) if data[
            'newDisplayAsset'] else None
        self.items: List[Union[BrCosmetic, CarCosmetic, InstrumentCosmetic, JamTrack]] = []
        if data['brItems']:
            self.items.extend([BrCosmetic(item) for item in data['brItems']])
        if data['cars']:
            self.items.extend([CarCosmetic(item) for item in data['cars']])
        if data['instruments']:
            self.items.extend([InstrumentCosmetic(item) for item in data['instruments']])
        if data['tracks']:
            self.items.extend([JamTrack(item) for item in data['tracks']])
        self.raw_data: dict = data


class ShopBundle:

    def __init__(self, data: dict):
        self.name: str = data['name']
        self.info: str = data['info']
        self.image_url: str = data['image']
        self.raw_data: dict = data


class ShopBanner:

    def __init__(self, data: dict):
        self.value: str = data['value']
        self.intensity: str = data['intensity']
        self.backend_value: str = data['backendValue']
        self.raw_data: dict = data


class ShopLayout:

    def __init__(self, data: dict):
        self.id: str = data['id']
        self.name: str = data['name']
        self.category: str = data['category']
        self.index: int = data['index']
        self.show_ineligible_offers: bool = data['showIneligibleOffers']
        self.background_url: str = data['background']
        self.raw_data: dict = data


class ShopNewDisplayAsset:

    def __init__(self, data: dict):
        self.id: str = data['id']
        self.cosmetic_id: Optional[str] = data['cosmeticId']
        self.material_instances: List[ShopMaterialInstance] = [ShopMaterialInstance(mi) for mi in
                                                               data['materialInstances']]
        self.raw_data: dict = data


class ShopMaterialInstance:

    def __init__(self, data: dict):
        self.id: str = data['id']
        self.primary_mode: CosmeticCompatibleMode = CosmeticCompatibleMode(data['primaryMode'])
        self.images: ShopMaterialInstanceImages = ShopMaterialInstanceImages(data['images'])
        self.colors: Optional[dict] = data['colors']
        self.scalings: Optional[dict] = data['scalings']
        self.flags: Optional[dict] = data['flags']
        self.raw_data: dict = data


class ShopMaterialInstanceImages:

    def __init__(self, data: dict):
        self.offer_image_url: str = data['OfferImage']
        self.fnm_texture_url: Optional[str] = data.get('FNMTexture')
        self.image_background_url: Optional[str] = data.get('ImageBackground')
        self.background_url: Optional[str] = data.get('Background')
        self.raw_data: dict = data


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

    def __init__(self, data):
        self.hash = data.get('hash')
        try:
            self.date = datetime.strptime(data.get('date'), '%Y-%m-%dT%H:%M:%S%z')
        except (ValueError, TypeError):
            self.date = None
        self.featured = BrShopSection(data.get('featured')) if data.get('featured') else None
        self.daily = BrShopSection(data.get('daily')) if data.get('daily') else None
        self.special_featured = BrShopSection(data.get('specialFeatured')) if data.get('specialFeatured') else None
        self.special_daily = BrShopSection(data.get('specialDaily')) if data.get('specialDaily') else None
        self.votes = BrShopSection(data.get('votes')) if data.get('votes') else None
        self.vote_winners = BrShopSection(data.get('voteWinners')) if data.get('voteWinners') else None
        self.raw_data = data


class BrShopSection:

    def __init__(self, data):
        self.name = data.get('name')
        self.entries = [BrShopEntry(entry_data) for entry_data in data.get('entries')] if data.get('entries') else None
        self.raw_data = data


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

    def __init__(self, data):
        self.regular_price = data.get('regularPrice')
        self.final_price = data.get('finalPrice')
        self.discount = self.regular_price - self.final_price if self.regular_price and self.final_price else None
        self.bundle = BrShopBundle(data.get('bundle')) if data.get('bundle') else None
        self.banner = BrShopBanner(data.get('banner')) if data.get('banner') else None
        self.giftable = data.get('giftable')
        self.refundable = data.get('refundable')
        self.sort_priority = data.get('sortPriority')
        self.categories = data.get('categories')
        self.section_id = data.get('sectionId')
        self.section = BrShopSectionNew(data.get('section')) if data.get('section') else None
        self.layout = BrShopLayout(data.get('layout')) if data.get('layout') else None
        self.dev_name = data.get('devName')
        self.offer_id = data.get('offerId')
        self.display_asset_path = data.get('displayAssetPath')
        self.tile_size = data.get('tileSize')
        self.new_display_asset_path = data.get('newDisplayAssetPath')
        self.new_display_asset = data.get('newDisplayAsset')
        self.items = [BrCosmetic(item_data) for item_data in data.get('items')]
        self.raw_data = data


class BrShopBundle:

    def __init__(self, data):
        self.name = data.get('name')
        self.info = data.get('info')
        self.image = data.get('image')
        self.raw_data = data


class BrShopBanner:

    def __init__(self, data):
        self.value = data.get('value')
        self.intensity = data.get('intensity')
        self.backend_value = data.get('backendValue')
        self.raw_data = data


class BrShopSectionNew:

    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.index = data.get('index')
        self.landing_priority = data.get('landingPriority')
        self.sort_offers_by_ownership = data.get('sortOffersByOwnership')
        self.show_ineligible_offers = data.get('showIneligibleOffers')
        self.show_ineligible_offers_if_giftable = data.get('showIneligibleOffersIfGiftable')
        self.show_timer = data.get('showTimer')
        self.enable_toast_notification = data.get('enableToastNotification')
        self.hidden = data.get('hidden')


class BrShopLayout:

    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.category = data.get('category')
        self.index = data.get('index')
        self.show_ineligible_offers = data.get('showIneligibleOffers')


class BrShopNewDisplayAsset:

    def __init__(self, data):
        self.id = data.get('id')
        self.material_instances = [BrShopMaterialInstance(mi) for mi in data.get('materialInstances')]


class BrShopMaterialInstance:

    def __init__(self, data):
        self.id = data.get('id')
        self.images = data.get('images')
        self.colors = data.get('colors')
        self.scalings = data.get('scalings')
