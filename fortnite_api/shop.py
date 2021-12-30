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

from datetime import datetime

from fortnite_api.cosmetics import BrCosmetic


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
