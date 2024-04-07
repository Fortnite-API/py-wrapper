from datetime import datetime
from typing import List, Union

from fortnite_api.enums import BrCosmeticType, BrCosmeticRarity


class NewBrCosmetics:
    """Represents a new Battle Royal cosmetic response.

    Attributes
    ----------
    build: :class:`str`
        The build of which are the latest cosmetics from
    previous_build: :class:`str`
        The previous build
    hash: :class:`str`
        The hash of the response
    date: :class:`datetime.datetime`
        The date of the response
    last_addition: :class:`datetime.datetime`
        The date of the last addition
    items: List[:class:`BrCosmetic`]
        A :class:`list` of :class:`BrCosmetic` objects.
    raw_data: Dict[:class:`str`, Any]
        The raw data from request. Can be used for saving and recreating the class.

    """

    def __init__(self, data):
        self.build: str = data['build']
        self.previous_build: str = data['previousBuild']
        self.hash: str = data['hash']
        self.date: datetime = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S%z')
        self.last_addition: datetime = datetime.strptime(data['lastAddition'], '%Y-%m-%dT%H:%M:%S%z')
        self.items: List[BrCosmetic] = [BrCosmetic(i) for i in data['items'] or []]
        self.raw_data: Dict[str, Any] = data


class NewCosmetics:

    def __init__(self, data):
        self.date: datetime = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S%z')
        self.build: str = data['build']
        self.previous_build: str = data['previousBuild']
        hashes = data['hashes']
        self.hash: str = hashes['all']
        self.hash_br: str = hashes['br']
        self.hash_cars: str = hashes['cars']
        self.hash_instruments: str = hashes['instruments']
        self.hash_jam_tracks: str = hashes['tracks']
        self.hash_lego: str = hashes['lego']
        last_additions = data['lastAdditions']
        self.last_addition: datetime = datetime.strptime(last_additions['all'], '%Y-%m-%dT%H:%M:%S%z')
        self.last_addition_br: datetime = datetime.strptime(last_additions['br'], '%Y-%m-%dT%H:%M:%S%z')
        self.last_addition_cars: datetime = datetime.strptime(last_additions['cars'], '%Y-%m-%dT%H:%M:%S%z')
        self.last_addition_instruments: datetime = datetime.strptime(
            last_additions['instruments'], '%Y-%m-%dT%H:%M:%S%z'
        )
        self.last_addition_jam_tracks: datetime = datetime.strptime(last_additions['tracks'], '%Y-%m-%dT%H:%M:%S%z')
        self.last_addition_lego: datetime = datetime.strptime(last_additions['lego'], '%Y-%m-%dT%H:%M:%S%z')
        items = data['items']
        self.items: List[Union[BrCosmetic, CarCosmetic, InstrumentCosmetic, LegoKitCosmetic, JamTrack, LegoCosmeticVariant]] = []
        self.items.extend([BrCosmetic(item) for item in items['br']])
        self.items.extend([CarCosmetic(item) for item in items['cars']])
        self.items.extend([InstrumentCosmetic(item) for item in items['instruments']])
        self.items.extend([LegoKitCosmetic(item) for item in items['legoKits']])
        self.items.extend([JamTrack(item) for item in items['tracks']])
        self.items.extend([LegoCosmeticVariant(item) for item in items['lego']])


class BaseCosmetic:
    """Represents a Cosmetic.

    Attributes
    -----------
    id: :class:`str`
        The id of the cosmetic.
    name: :class:`str`
        The name of the cosmetic in the chosen language.
    description: :class:`str`
        The description of the cosmetic in the chosen language.
    exclusive_description: Optional[:class:`str`]
        The exclusive description describing extra cosmetic features of the cosmetic in the chosen language.
    unlock_requirements: Optional[:class:`str`]
        The unlock requirements of the cosmetic in the chosen language.
    custom_exclusive_callout: Optional[:class:`str`]
        The custom exclusive callout of the cosmetic in the chosen language.
    type: :class:`BrCosmeticType`
        The type of the cosmetic.
    type_text: :class:`str`
        The display type of the cosmetic.
    backend_type: :class:`str`
        The internal type of the cosmetic.
    rarity: :class:`BrCosmeticRarity`
        The rarity of the cosmetic.
    rarity_text: :class:`str`
        The display rarity of the cosmetic.
    backend_rarity: :class:`str`
        The internal rarity of the cosmetic.
    name: :class:`str`
        The name of the cosmetic in the chosen language.
    description: :class:`str`
        The description of the cosmetic in the chosen language.
    series: Optional[:class:`str`]
        The series of the cosmetic in the chosen language.
    backend_series: Optional[:class:`str`]
        The internal series of the cosmetic.
    gameplay_tags: Optional[List[:class:`str`]]
        A :class:`list` of gameplay tags of the cosmetics.
    path: :class:`str`
        The path of the asset.
    added: :class:`datetime.datetime`
        The timestamp when the item was added to the Fortnite-API.com database.
    shop_history: List[:class:`datetime.datetime`]
        A :class:`list` of :class:`datetime.datetime` when the cosmetic was published in the item shop.
    appearances: :class:`int`
        The amount of appearances in the item shop of the cosmetic.
    first_appearance: Optional[:class:`datetime.datetime`]
        The timestamp when the cosmetic was first published in the item shop.
    last_appearance: Optional[:class:`datetime.datetime`]
        The timestamp when the cosmetic was last published in the item shop.
    unseen_for: Optional[:class:`int`]
        The amount of days since the cosmetic was last published in the item shop.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and recreating the class.
    """

    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')

        try:
            self.type: BrCosmeticType = BrCosmeticType(data['type']['value'])
        except ValueError:
            self.type: BrCosmeticType = BrCosmeticType.UNKNOWN
        self.type_text: str = data['type']['displayValue']
        self.backend_type: str = data['type']['backendValue']

        try:
            self.rarity: BrCosmeticRarity = BrCosmeticRarity(data['rarity']['value'])
        except ValueError:
            self.rarity: BrCosmeticRarity = BrCosmeticRarity.UNKNOWN
        self.rarity_text: str = data['rarity']['displayValue']
        self.backend_rarity: str = data['rarity']['backendValue']

        series = data.get('series', {}) if data.get('series') else {}
        self.series = series.get('value')
        self.series_image = series.get('image')
        self.series_colors = series.get('colors')
        self.backend_series = series.get('backendValue')

        self.gameplay_tags = [gameplay_tag for gameplay_tag in data.get('gameplayTags')] \
            if data.get('gameplayTags') is not None else None
        self.showcase_video_url = 'https://youtube.com/watch?v=' + data.get('showcaseVideo') \
            if data.get('showcaseVideo') else None
        self.path = data.get('path')
        try:
            self.added = datetime.strptime(data.get('added'), '%Y-%m-%dT%H:%M:%S%z')
        except (ValueError, TypeError):
            self.added = None

        self.shop_history = []
        for date in data.get('shopHistory', []) if data.get('shopHistory') else []:
            try:
                self.shop_history.append(datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None))
            except (ValueError, TypeError):
                pass
        self.appearances = len(self.shop_history)
        self.first_appearance = self.shop_history[0] if self.appearances > 0 else None
        self.last_appearance = self.shop_history[self.appearances - 1] if self.appearances > 0 else None
        self.unseen_for = (datetime.utcnow() - self.last_appearance).days if self.last_appearance else None

        self.raw_data = data


class BrCosmetic(BaseCosmetic):
    """Represents a Battle Royale Cosmetic.

    Attributes
    -----------
    set: Optional[:class:`str`]
        The set of the cosmetic in the chosen language.
    set_text: Optional[:class:`str`]
        The text of the set of the cosmetic in the chosen language.
    small_icon: :class:`BrCosmeticImage`
        The icon image in 128x128 resolution of the cosmetic.
    icon: Optional[:class:`BrCosmeticImage`]
        The icon image in 512x512 resolution of the cosmetic.
    featured: Optional[:class:`BrCosmeticImage`]
        The featured image in 1024x1024 resolution of the cosmetic.
    background: Optional[:class:`BrCosmeticImage`]
        The background image in 2048x1024 resolution of a loading screen.
    coverart: Optional[:class:`BrCosmeticImage`]
        The cover art image in 512x512 resolution of a music pack.
    decal: Optional[:class:`BrCosmeticImage`]
        The decal in 512x512 resolution of a spray.
    variants: Optional[List[:class:`BrCosmeticVariant`]]
        A :class:`list` of :class:`BrCosmeticVariant` of the cosmetic.
    display_asset_path: Optional[:class:`str`]
        The path of the display asset.
    """

    def __init__(self, data):
        super().__init__(data)
        self.exclusive_description = data.get('exclusiveDescription')
        self.unlock_requirements = data.get('unlockRequirements')
        self.custom_exclusive_callout = data.get('customExclusiveCallout')

        cosmetic_set = data.get('set', {}) if data.get('set') else {}
        self.set = cosmetic_set.get('value')
        self.set_text = cosmetic_set.get('text')
        self.backend_set = cosmetic_set.get('backendValue')

        introduction = data['introduction'] or {}
        self.introduction_chapter: Optional[str] = introduction.get('chapter')
        self.introduction_season: Optional[str] = introduction.get('season')
        self.introduction_text: Optional[str] = introduction.get('text')
        self.backend_introduction: Optional[int] = introduction.get('backendValue')

        images = data.get('images', {}) if data.get('images') else {}
        self.small_icon = BrCosmeticImage(images.get('smallIcon')) if images.get('smallIcon') else None
        self.icon = BrCosmeticImage(images.get('icon')) if images.get('icon') else None
        self.featured = BrCosmeticImage(images.get('featured')) if images.get('featured') else None
        lego_images = images.get('lego', {}) if images.get('lego') else {}
        self.lego_small = BrCosmeticImage(lego_images.get('small')) if lego_images.get('small') else None
        self.lego_large = BrCosmeticImage(lego_images.get('large')) if lego_images.get('large') else None
        self.lego_wide = BrCosmeticImage(lego_images.get('wide')) if lego_images.get('wide') else None
        other_images = images.get('other', {}) if images.get('other') else {}
        self.background = BrCosmeticImage(other_images.get('background')) if other_images.get('background') else None
        self.coverart = BrCosmeticImage(other_images.get('coverart')) if other_images.get('coverart') else None
        self.decal = BrCosmeticImage(other_images.get('decal')) if other_images.get('decal') else None

        self.variants = [BrCosmeticVariant(variant) for variant in data.get('variants')] \
            if data.get('variants') is not None else None
        self.built_in_emote_ids = [be for be in data.get('builtInEmoteIds')] \
            if data.get('builtInEmoteIds') is not None else None
        self.search_tags = [st for st in data.get('searchTags')] \
            if data.get('searchTags') is not None else None

        self.meta_tags = [meta_tag for meta_tag in data.get('metaTags')] \
            if data.get('metaTags') is not None else None

        self.dynamic_pak_id = data.get('dynamicPakId')
        self.item_preview_hero_path = data.get('itemPreviewHeroPath')
        self.display_asset_path = data.get('displayAssetPath')
        self.definition_path = data.get('definitionPath')


class BrCosmeticVariant:
    """Represents a Battle Royale cosmetic variant.

    Attributes
    -----------
    channel: :class:`str`
        The channel of the variant.
    type: Optional[:class:`str`]
        The type of the variant in the chosen language.
    options: List[:class:`BrCosmeticVariantOption`]
        A :class:`list` of :class:`BrCosmeticVariantOption`.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    def __init__(self, data: Dict[str, Any]):
        self.channel: str = data['channel']
        self.type: Optional[str] = data['type']
        self.options: List[BrCosmeticVariantOption] = [BrCosmeticVariantOption(op) for op in data['options']]
        self.raw_data: Dict[str, Any] = data


class BrCosmeticVariantOption:
    """Represents a Battle Royale cosmetic variant option.

    Attributes
    -----------
    tag: :class:`str`
        The tag of the option.
    name: :class:`str`
        The name of the option in the chosen language.
    image: :class:`BrCosmeticImage`
        A image of the option. The size is 256x256.
    unlock_requirements: Optional[:class:`str`]
        The unlock requirements of the option in the chosen language.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    def __init__(self, data: Dict[str, Any]):
        self.tag: str = data['tag']
        self.name: Optional[str] = data['name']
        self.image: BrCosmeticImage = BrCosmeticImage(data['image'], None)
        self.unlock_requirements: Optional[str] = data.get('unlockRequirements')
        self.raw_data: Dict[str, Any] = data


class CarCosmetic(BaseCosmetic):
    """Represents a Car Cosmetic.

    Attributes
    -----------
    vehicle_id: :class:`str`
        The id of the vehicle.
    small: :class:`CosmeticImage`
        The small image of the cosmetic.
    large: :class:`CosmeticImage`
        The large image of the cosmetic.
    """

    def __init__(self, data):
        super().__init__(data)
        self.vehicle_id = data.get('vehicleId')

        images = data.get('images', {}) if data.get('images') else {}
        self.small = CosmeticImage(images.get('small')) if images.get('small') else None
        self.large = CosmeticImage(images.get('large')) if images.get('large') else None


class InstrumentCosmetic(BaseCosmetic):
    """Represents an Instrument Cosmetic.

    Attributes
    -----------
    small: :class:`CosmeticImage`
        The small image of the cosmetic.
    large: :class:`CosmeticImage`
        The large image of the cosmetic.
    """

    def __init__(self, data):
        super().__init__(data)
        images = data.get('images', {}) if data.get('images') else {}
        self.small = CosmeticImage(images.get('small')) if images.get('small') else None
        self.large = CosmeticImage(images.get('large')) if images.get('large') else None


class LegoKitCosmetic(BaseCosmetic):

    def __init__(self, data):
        super().__init__(data)
        images = data.get('images', {}) if data.get('images') else {}
        self.small = CosmeticImage(images.get('small')) if images.get('small') else None
        self.large = CosmeticImage(images.get('large')) if images.get('large') else None


class LegoCosmeticVariant:
    """Represents a Lego Cosmetic Variant.

    Attributes
    -----------
    tag: :class:`str`
        The tag of the variant.
    name: :class:`str`
        The name of the variant in the chosen language.
    image: :class:`BrCosmeticImage`
        A image of the variant.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    def __init__(self, data):
        self.cosmetic_id = data.get('cosmeticId')
        self.sound_library_tags = data.get('soundLibraryTags')
        images = data.get('images', {}) if data.get('images') else {}
        self.small = CosmeticImage(images.get('small')) if images.get('small') else None
        self.large = CosmeticImage(images.get('large')) if images.get('large') else None
        self.wide = CosmeticImage(images.get('wide')) if images.get('wide') else None
        self.path = data.get('path')


class JamTrack:
    """Represents a Jam Track.

    Attributes
    -----------
    id: :class:`str`
        The id of the jam track.
    dev_name: :class:`str`
        The dev name of the jam track.
    title: :class:`str`
        The title of the jam track.
    artist: :class:`str`
        The artist of the jam track.
    album: :class:`str`
        The album of the jam track.
    release_year: :class:`int`
        The release year of the jam track.
    bpm: :class:`int`
        The bpm of the jam track.
    duration: :class:`int`
        The duration of the jam track.
    difficutly: :class:`int`
        The difficulty of the jam track.
    gameplay_tags: List[:class:`str`]
        A :class:`list` of gameplay tags of the jam track.
    genres: List[:class:`str`]
        A :class:`list` of genres of the jam track.
    album_art_url: :class:`str`
        The album art url of the jam track.
    added: :class:`datetime.datetime`
        The timestamp when the item was added to the Fortnite-API.com database.
    shop_history: List[:class:`datetime.datetime`]
        A :class:`list` of timestamps when the jam track was in the shop.
    appearances: :class:`int`
        The amount of times the jam track was in the shop.
    first_appearance: Optional[:class:`datetime.datetime`]
        The timestamp when the jam track was first in the shop.
    last_appearance: Optional[:class:`datetime.datetime`]
        The timestamp when the jam track was last in the shop.
    unseen_for: Optional[:class:`int`]
        The amount of days the jam track is unseen.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    def __init__(self, data):
        self.id = data.get('id')
        self.dev_name = data.get('devName')
        self.title = data.get('title')
        self.artist = data.get('artist')
        self.album = data.get('album')
        self.release_year = data.get('releaseYear')
        self.bpm = data.get('bpm')
        self.duration = data.get('duration')
        self.difficutly = data.get('difficutly')
        self.gameplay_tags = data.get('gameplayTags')
        self.genres = data.get('genres')
        self.album_art_url = data.get('albumArt')
        try:
            self.added = datetime.strptime(data.get('added'), '%Y-%m-%dT%H:%M:%S%z')
        except (ValueError, TypeError):
            self.added = None
        self.shop_history = []
        for date in data.get('shopHistory', []) if data.get('shopHistory') else []:
            try:
                self.shop_history.append(datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None))
            except (ValueError, TypeError):
                pass
        self.appearances = len(self.shop_history)
        self.first_appearance = self.shop_history[0] if self.appearances > 0 else None
        self.last_appearance = self.shop_history[self.appearances - 1] if self.appearances > 0 else None
        self.unseen_for = (datetime.utcnow() - self.last_appearance).days if self.last_appearance else None
        self.raw_data = data


class CosmeticImage:
    """Represents a Battle Royale cosmetic image.

    Attributes
    -----------
    url: :class:`str`
        The hash of the image.
    """

    def __init__(self, url):
        self.url = url

    def url_as(self, size):
        if (size & (size - 1) != 0) or size <= 0:
            raise ValueError('Size must be a positive power of 2')

        url_without_type = self.url.replace('.png', '')
        return url_without_type + '_' + str(size) + '.png'

    def __str__(self):
        return self.url


BrCosmeticImage = CosmeticImage
