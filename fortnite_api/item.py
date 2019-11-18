from datetime import datetime

from fortnite_api.enums import BrCosmeticType, BrCosmeticRarity


class BrCosmetic:

    def __init__(self, data):
        self.id = data.get('id')
        self.type = BrCosmeticType(data.get('type'))
        self.backend_type = data.get('backendType')
        self.rarity = BrCosmeticRarity(data.get('rarity'))
        self.display_rarity = data.get('displayRarity')
        self.backend_rarity = data.get('backendRarity')
        self.name = data.get('name')
        self.short_description = data.get('shortDescription')
        self.description = data.get('description')
        self.set = data.get('set')
        self.set_text = data.get('setText')
        self.series = data.get('series')
        images = data.get('images', {})
        self.small_icon = BRCosmeticImage(images.get('smallIcon')) if images.get('smallIcon') is not None else None
        self.icon = BRCosmeticImage(images.get('icon')) if images.get('icon') is not None else None
        self.featured = BRCosmeticImage(images.get('featured')) if images.get('featured') is not None else None
        self.background = BRCosmeticImage(images.get('background')) if images.get('background') is not None else None
        self.cover_art = BRCosmeticImage(images.get('coverArt')) if images.get('coverArt') is not None else None
        self.decal = BRCosmeticImage(images.get('decal')) if images.get('decal') is not None else None
        self.variants = [BrCosmeticVariant(variant) for variant in data.get('variants')] \
            if data.get('variants') is not None else None
        self.gameplay_tags = [gameplay_tag for gameplay_tag in data.get('gameplayTags')] \
            if data.get('gameplayTags') is not None else None
        self.display_asset_path = data.get('displayAssetPath')
        self.definition = data.get('definition')
        self.required_item_id = data.get('requiredItemId')
        self.built_in_emote_id = data.get('builtInEmoteId')
        self.path = data.get('path')
        try:
            self.last_updated = datetime.strptime(data.get('lastUpdate'), '%Y-%m-%dT%H:%M:%S%z')
        except ValueError:
            self.last_updated = None
        try:
            self.added = datetime.strptime(data.get('added'), '%Y-%m-%dT%H:%M:%S%z')
        except ValueError:
            self.added = None
        self.raw_data = data


class BRCosmeticImage:

    def __init__(self, data):
        self.hash = data.get('hash')
        self.url = data.get('url')
        self.raw_data = data


class BrCosmeticVariant:

    def __init__(self, data):
        self.type = data.get('type')
        self.options = None
        self.raw_data = data

        if data.get('options'):
            self.options = []
            for variant in data.get('options'):
                self.options.append(variant)


class BrCosmeticVariantOption:

    def __init__(self, data):
        self.name = data.get('name')
        self.image = BRCosmeticImage(data.get('image'))
        self.raw_data = data

