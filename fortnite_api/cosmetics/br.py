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
from typing import Any, Dict, Generic, List, Optional

from ..asset import Asset
from ..enums import CosmeticBrSearchTag
from ..http import HTTPClientT
from ..utils import parse_time
from .common import Cosmetic, CosmeticImages, CosmeticRarity, CosmeticSeries, CosmeticType


class CosmeticSet:
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

    def __init__(self, *, data: Dict[str, Any]) -> None:
        self.value: str = data['value']
        self.text: str = data['text']
        self.backend_value: str = data['backendValue']


class CosmeticIntroduction:
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

    def __init__(self, *, data: Dict[str, Any]) -> None:
        self.chapter: int = int(data['chapter'])
        self.season: str = data['season']
        self.text: str = data['text']
        self.backend_value: int = data['backendValue']


class CosmeticVariantOption(Generic[HTTPClientT]):
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

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.tag: str = data['tag']
        self.name: str = data['name']
        self.image: Asset[HTTPClientT] = Asset[HTTPClientT](http=http, url=data['image'])


class CosmeticVariant(Generic[HTTPClientT]):
    """Represents a variant for a cosmetic.

    Attributes
    ----------
    channel: :class:`str`
        The channel of the variant.
    type: :class:`str`
        The type of the variant.
    options: List[:class:`CosmeticVariantOption`]
        The options for the variant, if any.
    """

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.channel: str = data['channel']
        self.type: str = data['type']  # TODO: Move to enum eventually.

        self.options: List[CosmeticVariantOption[HTTPClientT]] = [
            CosmeticVariantOption[HTTPClientT](data=option, http=http) for option in data['options']
        ]


class CosmeticBr(Cosmetic[HTTPClientT]):
    """Represents a Battle Royale cosmetic.

    Attributes
    ----------
    name: :class:`str`
        The name of the cosmetic.
    description: :class:`str`
        The description of the cosmetic.
    type: Optional[:class:`CosmeticType`]
        The type of the cosmetic.
    rarity: Optional[:class:`CosmeticRarity`]
        The cosmetic's rarity.
    series: Optional[:class:`CosmeticSeries`]
        The series of the cosmetic, if any.
    set: Optional[:class:`CosmeticSet`]
        The set that the cosmetic belongs to, if any.
    introduction: Optional[:class:`CosmeticIntroduction`]
        Metadata about when the cosmetic was introduced, if available.
    images: Optional[:class:`CosmeticImages`]
        The images of the cosmetic.
    variants: List[:class:`CosmeticVariant`]
        The variants of the cosmetic, if any.
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
    display_asset_path: Optional[:class:`str`]
        The display asset path of the cosmetic, if available.
    definition_path: Optional[:class:`str`]
        The definition path of the cosmetic, if available.
    path: Optional[:class:`str`]
        The path of the cosmetic, if available.
    shop_history: List[:class:`datetime.datetime`]
        The shop history of the cosmetic.
    """

    def __init__(
        self,
        *,
        data: Dict[str, Any],
        http: HTTPClientT,
    ) -> None:
        super().__init__(http=http, data=data)

        self.name: str = data['name']
        self.description: str = data['description']

        _type = data.get('type')
        self.type: Optional[CosmeticType] = _type and CosmeticType(data=_type)

        rarity = data.get('rarity')
        self.rarity: Optional[CosmeticRarity] = rarity and CosmeticRarity(data=rarity)

        series = data.get('series')
        self.series: Optional[CosmeticSeries[HTTPClientT]] = series and CosmeticSeries(http=http, data=series)

        _set = data.get('set')
        self.set: Optional[CosmeticSet] = _set and CosmeticSet(data=_set)

        introduction = data.get('introduction')
        self.introduction: Optional[CosmeticIntroduction] = introduction and CosmeticIntroduction(data=introduction)

        images = data.get('images')
        self.images: Optional[CosmeticImages[HTTPClientT]] = images and CosmeticImages(http=http, data=images)

        variants: List[Dict[str, Any]] = data.get('variants', None) or []
        self.variants: List[CosmeticVariant[HTTPClientT]] = [
            CosmeticVariant(data=variant, http=http) for variant in variants
        ]

        search_tags: List[str] = data.get('searchTags', []) or []
        self.search_tags: List[CosmeticBrSearchTag] = [CosmeticBrSearchTag(tag) for tag in search_tags]

        self.gameplay_tags: List[str] = data.get('gameplayTags', []) or []
        self.meta_tags: List[str] = data.get('metaTags', []) or []

        self.showcase_video: Optional[str] = data.get('showcaseVideo', None)
        self.dynamic_pak_id: Optional[str] = data.get('dynamicPakId', None)
        self.display_asset_path: Optional[str] = data.get('displayAssetPath', None)
        self.definition_path: Optional[str] = data.get('definitionPath', None)
        self.path: Optional[str] = data.get('path', None)

        _shop_history: List[str] = data.get('shopHistory') or []
        self.shop_history: List[datetime.datetime] = [parse_time(time) for time in _shop_history]
