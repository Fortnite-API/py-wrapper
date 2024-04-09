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

import datetime
from typing import Any, Dict, Generic, List, Optional, Tuple

from ..asset import Asset
from ..enums import CosmeticBrSearchTag
from ..http import HTTPClientT
from ..utils import get_with_fallback, parse_time
from .common import Cosmetic, CosmeticImages, CosmeticRarity, CosmeticSeries, CosmeticType

__all__: Tuple[str, ...] = ('CosmeticBrSet', 'CosmeticBrIntroduction', 'CosmeticBrVariantOption', 'CosmeticBr')


class CosmeticBrSet:
    """Represents a set that a given cosmetic belongs to.

    Attributes
    ----------
    value: :class:`str`
        The value of the set, also known as the name.
    text: :class:`str`
        The display text of this set. In the form, ``"Part of the {{value}} set."``
    backend_value: :class:`str`
        The backend value of this set.
    """

    __slots__: Tuple[str, ...] = ('value', 'text', 'backend_value')

    def __init__(self, *, data: Dict[str, Any]) -> None:
        self.value: str = data['value']
        self.text: str = data['text']
        self.backend_value: str = data['backendValue']


class CosmeticBrIntroduction:
    """Holds some metadata about when a cosmetic was introduced.

    Attributes
    ----------
    chapter: :class:`int`
        The chapter the cosmetic was introduced in.
    season: :class:`str`
        The season the cosmetic was introduced in. Can be "OG" if the cosmetic was introduced before seasons.
    text: :class:`str`
        The display text of this introduction. In the form, ``"Introduced in Chapter {{chapter}}, Season {{season}}."``
    backend_value: :class:`int`
        The backend value of this introduction.
    """

    __slots__: Tuple[str, ...] = ('chapter', 'season', 'text', 'backend_value')

    def __init__(self, *, data: Dict[str, Any]) -> None:
        self.chapter: int = int(data['chapter'])
        self.season: str = data['season']
        self.text: str = data['text']
        self.backend_value: int = data['backendValue']


class CosmeticBrVariantOption(Generic[HTTPClientT]):
    """Represents a variant option for a cosmetic.

    Attributes
    ----------
    tag: :class:`str`
        The tag of the variant option.
    name: :class:`str`
        The option's name.
    image: :class:`Asset`
        The image of the variant option.
    """

    __slots__: Tuple[str, ...] = ('tag', 'name', 'image')

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.tag: str = data['tag']
        self.name: str = data['name']
        self.image: Asset[HTTPClientT] = Asset(http=http, url=data['image'])


class CosmeticBrVariant(Generic[HTTPClientT]):
    """Represents a variant for a cosmetic.

    Attributes
    ----------
    channel: :class:`str`
        The channel of the variant.
    type: :class:`str`
        The type of the variant.
    options: List[:class:`CosmeticBrVariantOption`]
        The options for the variant, if any.
    """

    __slots__: Tuple[str, ...] = ('channel', 'type', 'options')

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.channel: str = data['channel']
        self.type: str = data['type']  # TODO: Move to enum eventually.

        self.options: List[CosmeticBrVariantOption[HTTPClientT]] = [
            CosmeticBrVariantOption(data=option, http=http) for option in data['options']
        ]


class CosmeticBr(Cosmetic[HTTPClientT]):
    """Represents a Battle Royale cosmetic.

    Attributes
    ----------
    name: :class:`str`
        The name of the cosmetic.
    description: :class:`str`
        The description of the cosmetic.
    exclusive_description: Optional[:class:`str`]
        The exclusive description of the cosmetic, if available.
    unlock_requirements: Optional[:class:`str`]
        The unlock requirements of the cosmetic, if available.
    custom_exclusive_callout: Optional[:class:`str`]
        The custom exclusive callout of the cosmetic, if available.
    type: Optional[:class:`CosmeticType`]
        The type of the cosmetic.
    rarity: Optional[:class:`CosmeticRarity`]
        The cosmetic's rarity.
    series: Optional[:class:`CosmeticSeries`]
        The series of the cosmetic, if any.
    set: Optional[:class:`CosmeticBrSet`]
        The set that the cosmetic belongs to, if any.
    introduction: Optional[:class:`CosmeticBrIntroduction`]
        Metadata about when the cosmetic was introduced, if available.
    images: Optional[:class:`CosmeticImages`]
        The images of the cosmetic.
    variants: List[:class:`CosmeticBrVariant`]
        The variants of the cosmetic, if any.
    built_in_emote_ids: List[:class:`str`]
        The built-in emote IDs of the cosmetic.
    search_tags: List[:class:`CosmeticBrSearchTag`]
        The search tags of the cosmetic.
    gameplay_tags: List[:class:`str`]
        The gameplay tags of the cosmetic.
    meta_tags: List[:class:`str`]
        The meta tags of the cosmetic.
    showcase_video: Optional[:class:`str`]
        The showcase video of the cosmetic, if available.
    dynamic_pak_id: Optional[:class:`str`]
        The dynamic pak ID of the cosmetic, if available.
    item_preview_hero_path: Optional[:class:`str`]
        The item preview hero path of the cosmetic, if available.
    display_asset_path: Optional[:class:`str`]
        The display asset path of the cosmetic, if available.
    definition_path: Optional[:class:`str`]
        The definition path of the cosmetic, if available.
    path: Optional[:class:`str`]
        The path of the cosmetic, if available.
    shop_history: List[:class:`datetime.datetime`]
        The shop history of the cosmetic.
    """

    __slots__: Tuple[str, ...] = (
        'name',
        'description',
        'exclusive_description',
        'unlock_requirements',
        'custom_exclusive_callout',
        'type',
        'rarity',
        'series',
        'set',
        'introduction',
        'images',
        'variants',
        'built_in_emote_ids',
        'search_tags',
        'gameplay_tags',
        'meta_tags',
        'showcase_video',
        'dynamic_pak_id',
        'item_preview_hero_path',
        'display_asset_path',
        'definition_path',
        'path',
        'shop_history',
    )

    def __init__(
        self,
        *,
        data: Dict[str, Any],
        http: HTTPClientT,
    ) -> None:
        super().__init__(http=http, data=data)

        self.name: str = data['name']
        self.description: str = data['description']
        self.exclusive_description: Optional[str] = data.get('exclusiveDescription')
        self.unlock_requirements: Optional[str] = data.get('unlockRequirements')
        self.custom_exclusive_callout: Optional[str] = data.get('customExclusiveCallout')

        _type = data.get('type')
        self.type: Optional[CosmeticType] = _type and CosmeticType(data=_type)

        rarity = data.get('rarity')
        self.rarity: Optional[CosmeticRarity] = rarity and CosmeticRarity(data=rarity)

        series = data.get('series')
        self.series: Optional[CosmeticSeries[HTTPClientT]] = series and CosmeticSeries(http=http, data=series)

        _set = data.get('set')
        self.set: Optional[CosmeticBrSet] = _set and CosmeticBrSet(data=_set)

        introduction = data.get('introduction')
        self.introduction: Optional[CosmeticBrIntroduction] = introduction and CosmeticBrIntroduction(data=introduction)

        images = data.get('images')
        self.images: Optional[CosmeticImages[HTTPClientT]] = images and CosmeticImages(http=http, data=images)

        variants: List[Dict[str, Any]] = get_with_fallback(data, 'variants', list)
        self.variants: List[CosmeticBrVariant[HTTPClientT]] = [
            CosmeticBrVariant(data=variant, http=http) for variant in variants
        ]

        built_in_emote_ids: List[str] = get_with_fallback(data, 'builtInEmoteId', list)
        self.built_in_emote_ids: List[str] = built_in_emote_ids

        search_tags: List[str] = get_with_fallback(data, 'searchTags', list)
        self.search_tags: List[CosmeticBrSearchTag] = [CosmeticBrSearchTag(tag) for tag in search_tags]

        self.gameplay_tags: List[str] = get_with_fallback(data, 'gameplayTags', list)
        self.meta_tags: List[str] = get_with_fallback(data, 'metaTags', list)

        self.showcase_video: Optional[str] = data.get('showcaseVideo')
        self.dynamic_pak_id: Optional[str] = data.get('dynamicPakId')
        self.item_preview_hero_path: Optional[str] = data.get('itemPreviewHeroPath')
        self.display_asset_path: Optional[str] = data.get('displayAssetPath')
        self.definition_path: Optional[str] = data.get('definitionPath')
        self.path: Optional[str] = data.get('path')

        self.shop_history: List[datetime.datetime] = [
            parse_time(time) for time in get_with_fallback(data, 'shopHistory', list)
        ]
