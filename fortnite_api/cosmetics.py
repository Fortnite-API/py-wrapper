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

import math
import datetime
from typing import Optional, List, Dict, Any, Tuple

from .enums import BrCosmeticType, BrCosmeticRarity
from .utils import parse_time


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

    __slots__: Tuple[str, ...] = ('build', 'previous_build', 'hash', 'date', 'last_addition', 'items', 'raw_data')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.build: str = data['build']
        self.previous_build: str = data['previousBuild']
        self.hash: str = data['hash']

        self.date: datetime.datetime = parse_time(data['date'])
        self.last_addition: datetime.datetime = parse_time(data['lastAddition'])
        self.items: List[BrCosmetic] = [BrCosmetic(i) for i in data['items'] or []]
        self.raw_data: Dict[str, Any] = data


class BrCosmetic:
    """Represents a Battle Royal cosmetic.

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
    series: Optional[:class:`str`]
        The series of the cosmetic.
    series_image: Optional[:class:`BrCosmeticImage`]
        The series image of the cosmetic.
    backend_series: Optional[:class:`str`]
        The backend series value of the cosmetic.
    set: Optional[:class:`str`]
        The set of the cosmetic in the chosen language.
    set_text: Optional[:class:`str`]
        The text of the set of the cosmetic in the chosen language.
    backend_set: Optional[:class:`str`]
        The backend set value of the cosmetic.
    introduction_chapter: Optional[:class:`str`]
        The introduction chapter of the cosmetic.
    introduction_season: Optional[:class:`str`]
        The introduction season of the cosmetic.
    introduction_text: Optional[:class:`str`]
        The introduction text of the cosmetic in the chosen language.
    backend_introduction: Optional[:class:`int`]
        The backend introduction value of the cosmetic.
    small_icon : Optional[:class:`BrCosmeticImage`]
        The small icon of the cosmetic. The maximum size is 128x128.
    icon: Optional[:class:`BrCosmeticImage`]
        The icon of the cosmetic. The maximum size is 512x512.
    featured: Optional[:class:`BrCosmeticImage`]
        The featured image of the cosmetic. The maximum size is 1024x1024.
    background: Optional[:class:`BrCosmeticImage`]
        The background image of the cosmetic. The maximum size is 2048x1024.
    coverart: Optional[:class:`BrCosmeticImage`]
        The coverart image of the cosmetic. The maximum size is 512x512.
    decal: Optional[:class:`BrCosmeticImage`]
        The decal image of the cosmetic. The maximum size is 128x128.
    variants: List[:class:`BrCosmeticVariant`]
        A :class:`list` of :class:`BrCosmeticVariant`.
    built_in_emote_ids: List[:class:`str`]
        A :class:`list` of built-in emote ids.
    search_tags: List[:class:`str`]
        A :class:`list` of search tags.
    gameplay_tags: List[:class:`str`]
        A :class:`list` of gameplay tags.
    meta_tags: List[:class:`str`]
        A :class:`list` of meta tags.
    showcase_video_url: Optional[:class:`str`]
        The showcase YouTube video url of the cosmetic.
    dynamic_pak_id: Optional[:class:`str`]
        The dynamic pak id of the cosmetic.
    item_preview_hero_path: Optional[:class:`str`]
        The item preview hero path of the cosmetic.
    display_asset_path: Optional[:class:`str`]
        The display asset path of the cosmetic.
    definition_path: Optional[:class:`str`]
        The definition path of the cosmetic.
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

    __slots__: Tuple[str, ...] = (
        'id',
        'name',
        'description',
        'exclusive_description',
        'unlock_requirements',
        'custom_exclusive_callout',
        'type',
        'type_text',
        'backend_type',
        'rarity',
        'rarity_text',
        'backend_rarity',
        'series',
        'series_image',
        'backend_series',
        'set',
        'set_text',
        'backend_set',
        'introduction_chapter',
        'introduction_season',
        'introduction_text',
        'backend_introduction',
        'small_icon',
        'icon',
        'featured',
        'background',
        'coverart',
        'decal',
        'variants',
        'built_in_emote_ids',
        'search_tags',
        'gameplay_tags',
        'meta_tags',
        'showcase_video_url',
        'dynamic_pak_id',
        'item_preview_hero_path',
        'display_asset_path',
        'definition_path',
        'path',
        'added',
        'shop_history',
        'raw_data',
    )

    def __init__(self, data: Dict[str, Any]):
        self.id: str = data['id']
        self.name: str = data['name']
        self.description: str = data['description']
        self.exclusive_description: Optional[str] = data.get('exclusiveDescription')
        self.unlock_requirements: Optional[str] = data.get('unlockRequirements')
        self.custom_exclusive_callout: Optional[str] = data.get('customExclusiveCallout')

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

        series = data['series'] or {}
        self.series: Optional[str] = series.get('value')
        self.series_image: Optional[BrCosmeticImage] = BrCosmeticImage(series['image'], 512) if series.get('image') else None
        self.backend_series: Optional[str] = series.get('backendValue')

        cosmetic_set = data['set'] or {}
        self.set: Optional[str] = cosmetic_set.get('value')
        self.set_text: Optional[str] = cosmetic_set.get('text')
        self.backend_set: Optional[str] = cosmetic_set.get('backendValue')

        introduction = data['introduction'] or {}
        self.introduction_chapter: Optional[str] = introduction.get('chapter')
        self.introduction_season: Optional[str] = introduction.get('season')
        self.introduction_text: Optional[str] = introduction.get('text')
        self.backend_introduction: Optional[int] = introduction.get('backendValue')

        images = data['images'] or {}
        self.small_icon: Optional[BrCosmeticImage] = (
            BrCosmeticImage(images['smallIcon'], 128) if images.get('smallIcon') else None
        )
        self.icon: Optional[BrCosmeticImage] = BrCosmeticImage(images['icon'], 512) if images.get('icon') else None
        self.featured: Optional[BrCosmeticImage] = (
            BrCosmeticImage(images['featured'], 1024) if images.get('featured') else None
        )

        other_images = images.get('other') or {}
        self.background: Optional[BrCosmeticImage] = (
            BrCosmeticImage(other_images['background'], 2048) if other_images.get('background') else None
        )
        self.coverart: Optional[BrCosmeticImage] = (
            BrCosmeticImage(other_images['coverart'], 512) if other_images.get('coverart') else None
        )
        self.decal: Optional[BrCosmeticImage] = (
            BrCosmeticImage(other_images['decal'], 128) if other_images.get('decal') else None
        )

        self.variants: List[BrCosmeticVariant] = [BrCosmeticVariant(va) for va in data['variants'] or []]
        self.built_in_emote_ids: List[str] = [be for be in data.get('builtInEmoteIds') or []]
        self.search_tags: List[str] = [st for st in data['searchTags'] or []]
        self.gameplay_tags: List[str] = [gt for gt in data['gameplayTags'] or []]
        self.meta_tags: List[str] = [mt for mt in data['metaTags'] or []]
        self.showcase_video_url: Optional[str] = (
            f'https://youtube.com/watch?v={data["showcaseVideo"]}' if data['showcaseVideo'] else None
        )
        self.dynamic_pak_id: Optional[str] = data.get('dynamicPakId')
        self.item_preview_hero_path: Optional[str] = data.get('itemPreviewHeroPath')
        self.display_asset_path: Optional[str] = data.get('displayAssetPath')
        self.definition_path: Optional[str] = data.get('definitionPath')
        self.path: str = data['path']
        self.added: datetime.datetime = parse_time(data['added'])

        self.shop_history: List[datetime.datetime] = [parse_time(date) for date in data['shopHistory'] or []]
        self.raw_data: Dict[str, Any] = data

    @property
    def first_appearance(self) -> Optional[datetime.datetime]:
        if not self.shop_history:
            return None

        return self.shop_history[0]

    @property
    def last_appearance(self) -> Optional[datetime.datetime]:
        if not self.shop_history:
            return None

        return self.shop_history[-1]

    @property
    def appearances(self) -> int:
        return len(self.shop_history)

    @property
    def unseen_for(self) -> Optional[int]:
        return (datetime.datetime.now(datetime.timezone.utc) - self.last_appearance).days if self.last_appearance else None


class BrCosmeticImage:
    """Represents a Battle Royale cosmetic image.

    Attributes
    -----------
    url: :class:`str`
        The hash of the image.
    """

    __slots__: Tuple[str, ...] = ('url', '_max_size')

    def __init__(self, url: str, max_size: Optional[int]) -> None:
        self.url: str = url
        self._max_size: Optional[int] = max_size

    def url_as(self, size: int) -> str:
        if self._max_size is None:
            raise ValueError('This image isn\'t resizable.')
        if size < 0 or type(math.sqrt(size)) is float:
            raise TypeError('Size must be a power of 2.')
        if size < 32 or size > self._max_size:
            raise TypeError(f'Size must be between 32 and {self._max_size}.')

        if size == self._max_size:
            return self.url

        url_without_type = self.url.replace('.png', '')
        return f'{url_without_type}_{size}.png'

    def __str__(self) -> str:
        return self.url


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
