from fortnite_api.enums import BrCosmeticType, BrCosmeticRarity


class BrCosmetic:

    def __init__(self, data):
        self.id = data['id']
        self.type = BrCosmeticType(data['type'])
        self.backend_type = data['backendType']
        self.rarity = BrCosmeticRarity(data['rarity'])
        self.backend_rarity = data['backendRarity']
        self.name = data['name']
        self.short_description = data['shortDescription']
        self.description = data['description']
        self.set = data['set']
        self.series = data['series']
        images = data['images']
        self.small_icon = BRCosmeticImage(images['smallIcon']) if images['smallIcon'] is not None else None
        self.icon = BRCosmeticImage(images['icon']) if images['icon'] is not None else None
        self.featured = BRCosmeticImage(images['featured']) if images['featured'] is not None else None
        self.background = BRCosmeticImage(images['background']) if images['background'] is not None else None
        self.cover_art = BRCosmeticImage(images['coverArt']) if images['coverArt'] is not None else None
        self.decal = BRCosmeticImage(images['decal']) if images['decal'] is not None else None
        self.variants = [BrCosmeticVariant(variant) for variant in data['variants']] if data['variants'] is not None else None
        self.gameplay_tags = [gameplay_tag for gameplay_tag in data['gameplayTags']] if data['gameplayTags'] is not None else None
        self.display_asset_path = data['displayAssetPath']
        self.definition = data['definition']
        self.required_item_id = data['requiredItemId']
        self.built_in_emote_id = data['builtInEmoteId']
        self.path = data['path']
        self.last_updated = data['lastUpdate']  # TODO: Convert into datetime
        self.added = data['added']  # TODO: Convert into datetime
        self.raw_data = data


class BRCosmeticImage:

    def __init__(self, data):
        self.hash = data['hash']
        self.url = data['url']
        self.raw_data = data


class BrCosmeticVariant:

    def __init__(self, data):
        self.type = data['type']
        self.options = None
        self.raw_data = data

        if data['options']:
            self.options = []
            for variant in data['options']:
                self.options.append(variant)


class BrCosmeticVariantOption:

    def __init__(self, data):
        self.name = data['name']
        self.image = BRCosmeticImage(data['image'])
        self.raw_data = data

