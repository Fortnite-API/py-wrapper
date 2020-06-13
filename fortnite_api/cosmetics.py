import math
from datetime import datetime

from fortnite_api.enums import BrCosmeticType, BrCosmeticRarity


class BrCosmetic:
    """Represents a Battle Royale Cosmetic.

    Attributes
    -----------
    id: :class:`str`
        The id of the cosmetic.
    type: :class:`BrCosmeticType`
        The type of the cosmetic.
    backend_type: :class:`str`
        The internal type of the cosmetic.
    rarity: :class:`BrCosmeticRarity`
        The rarity of the cosmetic.
    backend_rarity: :class:`str`
        The internal rarity of the cosmetic.
    name: :class:`str`
        The name of the cosmetic in the chosen language.
    description: :class:`str`
        The description of the cosmetic in the chosen language.
    set: Optional[:class:`str`]
        The set of the cosmetic in the chosen language.
    set_text: Optional[:class:`str`]
        The text of the set of the cosmetic in the chosen language.
    series: Optional[:class:`str`]
        The series of the cosmetic in the chosen language.
    backend_series: Optional[:class:`str`]
        The internal series of the cosmetic.
    small_icon: :class:`BrCosmeticImage`
        The icon image in 128x128 resolution of the cosmetic.
    icon: Optional[:class:`BrCosmeticImage`]
        The icon image in 512x512 resolution of the cosmetic.
    featured: Optional[:class:`BrCosmeticImage`]
        The featured image in 1024x1024 resolution of the cosmetic.
    background: Optional[:class:`BrCosmeticImage`]
        The background image in 2048x1024 resolution of a loading screen.
    cover_art: Optional[:class:`BrCosmeticImage`]
        The cover art image in 512x512 resolution of a music pack.
    decal: Optional[:class:`BrCosmeticImage`]
        The decal in 512x512 resolution of a spray.
    variants: Optional[List[:class:`BrCosmeticVariant`]]
        A :class:`list` of :class:`BrCosmeticVariant` of the cosmetic.
    gameplay_tags: Optional[List[:class:`str`]]
        A :class:`list` of gameplay tags of the cosmetics.
    display_asset_path: Optional[:class:`str`]
        The path of the display asset.
    path: :class:`str`
        The path of the asset.
    added: :class:`datetime.datetime`
        The timestamp when the item was added to the Fortnite-API.com database.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and recreating the class.
    """

    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')

        cosmetic_type = data.get('type', {}) if data.get('type') else {}
        self.type = BrCosmeticType(cosmetic_type.get('value'))
        self.display_type = cosmetic_type.get('displayValue')
        self.backend_type = cosmetic_type.get('backendValue')

        rarity = data.get('rarity', {}) if data.get('rarity') else {}
        try:
            self.rarity = BrCosmeticRarity(rarity.get('value'))
        except ValueError:
            self.rarity = BrCosmeticRarity.UNKNOWN
        self.rarity_text = rarity.get('text')
        self.backend_rarity = rarity.get('backendValue')

        series = data.get('series', {}) if data.get('series') else {}
        self.series = series.get('value')
        self.series_image = series.get('image')
        self.backend_series = series.get('backendValue')

        cosmetic_set = data.get('set', {}) if data.get('set') else {}
        self.set = cosmetic_set.get('value')
        self.set_text = cosmetic_set.get('text')
        self.backend_set = cosmetic_set.get('backendValue')

        introduction = data.get('introduction', {}) if data.get('introduction') else {}
        self.introduction_chapter = introduction.get('chapter')
        self.introduction_season = introduction.get('season')
        self.introduction_text = introduction.get('text')
        self.backend_introduction = introduction.get('backendValue')

        images = data.get('images', {}) if data.get('images') else {}
        self.small_icon = BrCosmeticImage(images.get('smallIcon')) if images.get('smallIcon') else None
        self.icon = BrCosmeticImage(images.get('icon')) if images.get('icon') else None
        self.featured = BrCosmeticImage(images.get('featured')) if images.get('featured') else None
        other_images = images.get('other', {}) if images.get('other') else {}
        self.background = BrCosmeticImage(other_images.get('background')) if other_images.get('background') else None
        self.cover_art = BrCosmeticImage(other_images.get('coverart')) if other_images.get('coverart') else None
        self.decal = BrCosmeticImage(other_images.get('decal')) if other_images.get('decal') else None
        self.background = BrCosmeticImage(other_images.get('background')) if other_images.get('background') else None

        self.variants = [BrCosmeticVariant(variant) for variant in data.get('variants')] \
            if data.get('variants') is not None else None
        self.gameplay_tags = [gameplay_tag for gameplay_tag in data.get('gameplayTags')] \
            if data.get('gameplayTags') is not None else None
        self.display_asset_path = data.get('displayAssetPath')
        self.definition_path = data.get('definitionPath')
        self.path = data.get('path')
        try:
            self.added = datetime.strptime(data.get('added'), '%Y-%m-%dT%H:%M:%S%z')
        except (ValueError, ValueError):
            self.added = None

        self.shop_history = []
        for date in data.get('shopHistory', []) if data.get('shopHistory') else []:
            try:
                self.shop_history.append(datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None))
            except (ValueError, ValueError):
                pass
        self.appearances = len(self.shop_history)
        self.first_appearance = self.shop_history[0] if self.appearances > 0 else None
        self.last_appearance = self.shop_history[self.appearances - 1] if self.appearances > 0 else None
        self.unseen_for = (datetime.utcnow() - self.last_appearance).days if self.last_appearance else None
        self.raw_data = data


class BrCosmeticImage:
    """Represents a Battle Royale cosmetic image.

    Attributes
    -----------
    url: :class:`str`
        The hash of the image.
    """

    def __init__(self, url):
        self.url = url

    def url_as(self, size):
        if size < 0 or type(math.sqrt(size)) is float:
            raise TypeError('Size must be a power of 2.')
        url_without_type = self.url.replace('.png', '')
        return url_without_type + '_' + size + '.png'

    def __str__(self):
        return self.url


class BrCosmeticVariant:
    """Represents a Battle Royale cosmetic image.

    Attributes
    -----------
    channel: :class:`str`
        The channel of the variant.
    type: Optional[:class:`str`]
        The type of the variant in the chosen language.
    options: List[:class:`BrCosmeticVariantOption`]
        A :class:`list` of :class:`BrCosmeticVariantOption` of the variant.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    def __init__(self, data):
        self.channel = data.get('channel')
        self.type = data.get('type')
        self.options = [BrCosmeticVariantOption(option) for option in data.get('options')] \
            if data.get('options') is not None else None
        self.raw_data = data


class BrCosmeticVariantOption:
    """Represents a Battle Royale cosmetic image.

    Attributes
    -----------
    tag: :class:`str`
        The tag of the option.
    name: :class:`str`
        The name of the option in the chosen language.
    image: :class:`BrCosmeticImage`
        A image of the option.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    def __init__(self, data):
        self.tag = data.get('tag')
        self.name = data.get('name')
        self.image = BrCosmeticImage(data.get('image'))
        self.raw_data = data
