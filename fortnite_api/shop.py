from fortnite_api.item import BrCosmetic


class BrShop:

    def __init__(self, data):
        self.hash = data['hash']
        self.date = data['date']  # TODO: Convert into datetime
        self.featured = [BrShopEntry(item_data) for item_data in data['featured']] if data['featured'] else None
        self.daily = [BrShopEntry(item_data) for item_data in data['daily']] if data['daily'] else None
        self.votes = [BrShopEntry(item_data) for item_data in data['votes']] if data['votes'] else None
        self.vote_winners = [BrShopEntry(item_data) for item_data in data['voteWinners']] if data['voteWinners'] else None
        self.raw_data = data


class BrShopEntry:

    def __init__(self, data):
        self.regular_price = data['regularPrice']
        self.final_price = data['finalPrice']
        self.discount = self.regular_price - self.final_price
        self.is_bundle = data['isBundle']
        self.panel = data['panel']
        self.sort_priority = data['sortPriority']
        self.banner = data['banner']
        self.items = [BrCosmetic(item_data) for item_data in data['items']]
        self.raw_data = data
