from datetime import datetime

from fortnite_api.cosmetics import BrCosmetic


class BrShop:

    def __init__(self, data):
        self.hash = data.get('hash')
        try:
            self.date = datetime.strptime(data.get('date'), '%Y-%m-%dT%H:%M:%S%z')
        except ValueError:
            self.date = None
        self.featured = [BrShopEntry(item_data) for item_data in data.get('featured')] if data.get('featured') else None
        self.daily = [BrShopEntry(item_data) for item_data in data.get('daily')] if data.get('daily') else None
        self.votes = [BrShopEntry(item_data) for item_data in data.get('votes')] if data.get('votes') else None
        self.vote_winners = [BrShopEntry(item_data) for item_data in data.get('voteWinners')] \
            if data.get('voteWinners') else None
        self.raw_data = data


class BrShopEntry:

    def __init__(self, data):
        self.regular_price = data.get('regularPrice')
        self.final_price = data.get('finalPrice')
        self.discount = self.regular_price - self.final_price
        self.is_bundle = data.get('isBundle')
        self.is_special = data.get('isSpecial')
        self.refundable = data.get('refundable')
        self.giftable = data.get('giftable')
        self.panel = data.get('panel')
        self.sort_priority = data.get('sortPriority')
        self.banner = data.get('banner')
        self.items = [BrCosmetic(item_data) for item_data in data.get('items')]
        self.raw_data = data
