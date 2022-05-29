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

import time
from typing import TYPE_CHECKING, List, Literal, Optional, TypeVar, Any, Dict, overload, Union
from typing_extensions import ParamSpec, Self

from .enums import *
from .aes import Aes
from .banner import Banner, BannerColor
from .cosmetics import BrCosmetic
from .http import HTTPClient, AsyncHTTPClient
from .creator_code import CreatorCode
from .map import Map
from .news import News, GameModeNews
from .playlist import Playlist
from .shop import BrShop
from .stats import BrPlayerStats

if TYPE_CHECKING:
    import aiohttp
    import requests
    import datetime

T = TypeVar('T')
TC = TypeVar('TC')
P = ParamSpec('P')


class FortniteAPI:
    r"""A number of options can be passed to the :class:`FortniteAPI`.

    Parameters
    -----------
    api_key: :class:`str`
        The API key from Fortnite-API.com\profile to authenticate.
    run_async: Optional[:class:`bool`]
        A boolean whether the API should run in async mode or not.
        Defaults set to ``True``, in which case the api runs sync.

    Attributes
    -----------
    cosmetics: Union[:class:`SyncCosmeticEndpoints`, :class:`AsyncCosmeticEndpoints`]
        The Cosmetic endpoints. The class depends whether the api runs sync or async.
    creator_code: Union[:class:`SyncCreatorCodeEndpoints`, :class:`AsyncCreatorCodeEndpoints`]
         The Creator Code endpoints. The class depends whether the api runs sync or async.
    news: Union[:class:`SyncNewsEndpoints`, :class:`AsyncNewsEndpoints`]
        The News endpoints. The class depends whether the api runs sync or async.
    shop: Union[:class:`SyncShopEndpoints`, :class:`AsyncShopEndpoints`]
        The Shop endpoints. The class depends whether the api runs sync or async.
    """

    def __init__(self, api_key: Optional[str] = None, *, session: Optional[requests.Session] = None) -> None:
        self.http: HTTPClient = HTTPClient(session=session, token=api_key)

    def fetch_aes(self, key_format: KeyFormat = KeyFormat.HEX) -> Aes:
        data = self.http.get_aes(key_format.value)
        return Aes(data=data)

    def fetch_banners(self, *, language: Optional[GameLanguage] = None) -> List[Banner]:
        data = self.http.get_banners(language=(language and language.value))
        return [Banner(data=entry) for entry in data]

    def fetch_banner_colors(self) -> List[BannerColor]:
        data = self.http.get_banner_colors()
        return [BannerColor(data=entry) for entry in data]

    def fetch_cosmetics(self, *, language: Optional[GameLanguage] = None) -> List[BrCosmetic]:
        data = self.http.get_cosmetics(language=(language and language.value))
        return [BrCosmetic(data=entry) for entry in data]

    def fetch_cosmetic(self, id: str, /, *, language: Optional[GameLanguage] = None) -> BrCosmetic:
        data = self.http.get_cosmetic(id, language=(language and language.value))
        return BrCosmetic(data=data)

    @overload
    def search_cosmetic(
        self,
        *,
        multiple: Literal[True] = True,
        language: Optional[GameLanguage] = None,
        search_language: Optional[GameLanguage] = None,
        match_method: Optional[MatchMethod] = None,
        id: Optional[str] = None,
        name: Optional[str] = None,
        descripion: Optional[str] = None,
        type: Optional[BrCosmeticType] = None,
        display_type: Optional[str] = None,
        backend_type: Optional[str] = None,
        rarity: Optional[BrCosmeticRarity] = None,
        display_rarity: Optional[str] = None,
        backend_rarity: Optional[str] = None,
        has_series: Optional[bool] = None,
        series: Optional[str] = None,
        backend_series: Optional[str] = None,
        has_set: Optional[bool] = None,
        set: Optional[str] = None,
        set_text: Optional[str] = None,
        backend_set: Optional[str] = None,
        has_introduction: Optional[bool] = None,
        backend_introduction: Optional[int] = None,
        introduction_chapter: Optional[str] = None,
        introduction_season: Optional[str] = None,
        has_featured_image: Optional[bool] = None,
        has_variants: Optional[bool] = None,
        has_gameplay_tags: Optional[bool] = None,
        gameplay_tag: Optional[str] = None,
        has_meta_tags: Optional[bool] = None,
        meta_tag: Optional[str] = None,
        has_dynamic_pak_id: Optional[bool] = None,
        dynamic_pak_id: Optional[str] = None,
        added: Optional[datetime.datetime] = None,
        added_since: Optional[datetime.datetime] = None,
        unseen_for: Optional[int] = None,
        last_appearance: Optional[int] = None,
    ) -> List[BrCosmetic]:
        ...

    @overload
    def search_cosmetic(
        self,
        *,
        multiple: Literal[False] = False,
        language: Optional[GameLanguage] = None,
        search_language: Optional[GameLanguage] = None,
        match_method: Optional[MatchMethod] = None,
        id: Optional[str] = None,
        name: Optional[str] = None,
        descripion: Optional[str] = None,
        type: Optional[BrCosmeticType] = None,
        display_type: Optional[str] = None,
        backend_type: Optional[str] = None,
        rarity: Optional[BrCosmeticRarity] = None,
        display_rarity: Optional[str] = None,
        backend_rarity: Optional[str] = None,
        has_series: Optional[bool] = None,
        series: Optional[str] = None,
        backend_series: Optional[str] = None,
        has_set: Optional[bool] = None,
        set: Optional[str] = None,
        set_text: Optional[str] = None,
        backend_set: Optional[str] = None,
        has_introduction: Optional[bool] = None,
        backend_introduction: Optional[int] = None,
        introduction_chapter: Optional[str] = None,
        introduction_season: Optional[str] = None,
        has_featured_image: Optional[bool] = None,
        has_variants: Optional[bool] = None,
        has_gameplay_tags: Optional[bool] = None,
        gameplay_tag: Optional[str] = None,
        has_meta_tags: Optional[bool] = None,
        meta_tag: Optional[str] = None,
        has_dynamic_pak_id: Optional[bool] = None,
        dynamic_pak_id: Optional[str] = None,
        added: Optional[datetime.datetime] = None,
        added_since: Optional[datetime.datetime] = None,
        unseen_for: Optional[int] = None,
        last_appearance: Optional[int] = None,
    ) -> BrCosmetic:
        ...

    def search_cosmetic(
        self,
        *,
        multiple: Optional[bool] = False,
        language: Optional[GameLanguage] = None,
        search_language: Optional[GameLanguage] = None,
        match_method: Optional[MatchMethod] = None,
        id: Optional[str] = None,
        name: Optional[str] = None,
        descripion: Optional[str] = None,
        type: Optional[BrCosmeticType] = None,
        display_type: Optional[str] = None,
        backend_type: Optional[str] = None,
        rarity: Optional[BrCosmeticRarity] = None,
        display_rarity: Optional[str] = None,
        backend_rarity: Optional[str] = None,
        has_series: Optional[bool] = None,
        series: Optional[str] = None,
        backend_series: Optional[str] = None,
        has_set: Optional[bool] = None,
        set: Optional[str] = None,
        set_text: Optional[str] = None,
        backend_set: Optional[str] = None,
        has_introduction: Optional[bool] = None,
        backend_introduction: Optional[int] = None,
        introduction_chapter: Optional[str] = None,
        introduction_season: Optional[str] = None,
        has_featured_image: Optional[bool] = None,
        has_variants: Optional[bool] = None,
        has_gameplay_tags: Optional[bool] = None,
        gameplay_tag: Optional[str] = None,
        has_meta_tags: Optional[bool] = None,
        meta_tag: Optional[str] = None,
        has_dynamic_pak_id: Optional[bool] = None,
        dynamic_pak_id: Optional[str] = None,
        added: Optional[datetime.datetime] = None,
        added_since: Optional[datetime.datetime] = None,
        unseen_for: Optional[int] = None,
        last_appearance: Optional[int] = None,
    ) -> Union[BrCosmetic, List[BrCosmetic]]:
        params: Dict[str, Any] = {}

        if language is not None:
            params['language'] = language.value

        if search_language is not None:
            params['searchLanguage'] = search_language.value

        if match_method is not None:
            params['matchMethod'] = match_method.value

        if id is not None:
            params['id'] = id

        if name is not None:
            params['name'] = name

        if descripion is not None:
            params['description'] = descripion

        if type is not None:
            params['type'] = type.value

        if display_type is not None:
            params['displayType'] = display_type

        if backend_type is not None:
            params['backendType'] = backend_type

        if rarity is not None:
            params['rarity'] = rarity.value

        if display_rarity is not None:
            params['displayRarity'] = display_rarity

        if backend_rarity is not None:
            params['backendRarity'] = backend_rarity

        if has_series is not None:
            params['hasSeries'] = has_series

        if series is not None:
            params['series'] = series

        if backend_series is not None:
            params['backendSeries'] = backend_series

        if has_set is not None:
            params['hasSet'] = has_set

        if set is not None:
            params['set'] = set

        if set_text is not None:
            params['setText'] = set_text

        if backend_set is not None:
            params['backendSet'] = backend_set

        if has_introduction is not None:
            params['hasIntroduction'] = has_introduction

        if backend_introduction is not None:
            params['backendIntroduction'] = backend_introduction

        if introduction_chapter is not None:
            params['introductionChapter'] = introduction_chapter

        if introduction_season is not None:
            params['introductionSeason'] = introduction_season

        if has_featured_image is not None:
            params['hasFeaturedImage'] = has_featured_image

        if has_variants is not None:
            params['hasVariants'] = has_variants

        if has_gameplay_tags is not None:
            params['hasGameplayTags'] = has_gameplay_tags

        if gameplay_tag is not None:
            params['gameplayTag'] = gameplay_tag

        if has_meta_tags is not None:
            params['hasMetaTags'] = has_meta_tags

        if meta_tag is not None:
            params['metaTag'] = meta_tag

        if has_dynamic_pak_id is not None:
            params['hasDynamicPakId'] = has_dynamic_pak_id

        if dynamic_pak_id is not None:
            params['dynamicPakId'] = dynamic_pak_id

        if added is not None:
            params['added'] = time.mktime(added.timetuple())

        if added_since is not None:
            params['addedSince'] = time.mktime(added_since.timetuple())

        if unseen_for is not None:
            params['unseenFor'] = unseen_for

        if last_appearance is not None:
            params['lastAppearance'] = last_appearance

        if multiple is True:
            data = self.http.search_cosmetic_all(**params)
            return [BrCosmetic(entry) for entry in data]

        data = self.http.search_cosmetic(**params)
        return BrCosmetic(data)

    def fetch_creator_code(self, name: str, /) -> CreatorCode:
        data = self.http.get_creator_code(name)
        return CreatorCode(data=data)

    def fetch_map(self, *, language: Optional[GameLanguage] = None) -> Map:
        data = self.http.get_map(language=(language and language.value))
        return Map(data=data)

    def fetch_news(self, *, language: Optional[GameLanguage] = None) -> News:
        data = self.http.get_news(language=(language and language.value))
        return News(data=data)

    def fetch_br_news(self, *, language: Optional[GameLanguage] = None) -> GameModeNews:
        data = self.http.get_br_news(language=(language and language.value))
        return GameModeNews(data=data)

    def fetch_stw_news(self, *, language: Optional[GameLanguage] = None) -> GameModeNews:
        data = self.http.get_stw_news(language=(language and language.value))
        return GameModeNews(data=data)

    def fetch_creative_news(self, *, language: Optional[GameLanguage] = None) -> GameModeNews:
        data = self.http.get_creative_news(language=(language and language.value))
        return GameModeNews(data=data)

    def fetch_playlist(self, id: str, /, *, language: Optional[GameLanguage] = None) -> Playlist:
        data = self.http.get_playlist(id, language=(language and language.value))
        return Playlist(data=data)

    def fetch_br_shop(self, *, language: Optional[GameLanguage] = None) -> BrShop:
        data = self.http.get_br_shop(language=(language and language.value))
        return BrShop(data=data)

    def fetch_br_shop_combined(self, *, language: Optional[GameLanguage] = None) -> BrShop:
        raise NotImplementedError('the fawk?')

    def fetch_br_stats(
        self,
        name: str,
        /,
        *,
        type: AccountType = AccountType.EPIC,
        time_window: TimeWindow = TimeWindow.LIFETIME,
        image: StatsImageType = StatsImageType.ALL,
    ) -> BrPlayerStats:
        data = self.http.get_br_stats(name=name, account_type=type.value, time_window=time_window.value, image=image.value)
        return BrPlayerStats(data=data)

    def fetch_br_stats_by_id(
        self, id: str, /, *, time_window: TimeWindow = TimeWindow.LIFETIME, image: StatsImageType = StatsImageType.ALL
    ) -> BrPlayerStats:
        data = self.http.get_br_stats_by_id(id=id, time_window=time_window.value, image=image.value)
        return BrPlayerStats(data=data)


class AsyncFortniteAPI:
    def __init__(self, api_key: Optional[str] = None, *, session: Optional[aiohttp.ClientSession] = None) -> None:
        self.http: AsyncHTTPClient = AsyncHTTPClient(session=session, token=api_key)

    async def __aenter__(self) -> Self:
        if self.http.session is None:
            self.http.session = aiohttp.ClientSession()

        return self

    async def __aexit__(self, *args: Any) -> None:
        if self.http.session is not None:
            await self.http.session.close()

    async def fetch_aes(self, *, key_format: KeyFormat = KeyFormat.HEX) -> Aes:
        data = await self.http.get_aes(key_format.value)
        return Aes(data=data)

    async def fetch_banners(self, *, language: Optional[GameLanguage] = None) -> List[Banner]:
        data = await self.http.get_banners(language=(language and language.value))
        return [Banner(data=entry) for entry in data]

    async def fetch_banner_colors(self) -> List[BannerColor]:
        data = await self.http.get_banner_colors()
        return [BannerColor(data=entry) for entry in data]

    async def fetch_cosmetics(self, *, language: Optional[GameLanguage] = None) -> List[BrCosmetic]:
        data = await self.http.get_cosmetics(language=(language and language.value))
        return [BrCosmetic(data=entry) for entry in data]

    async def fetch_cosmetic(self, id: str, /, *, language: Optional[GameLanguage] = None) -> BrCosmetic:
        data = await self.http.get_cosmetic(id, language=(language and language.value))
        return BrCosmetic(data=data)

    @overload
    async def search_cosmetic(
        self,
        *,
        multiple: Literal[True] = True,
        language: Optional[GameLanguage] = None,
        search_language: Optional[GameLanguage] = None,
        match_method: Optional[MatchMethod] = None,
        id: Optional[str] = None,
        name: Optional[str] = None,
        descripion: Optional[str] = None,
        type: Optional[BrCosmeticType] = None,
        display_type: Optional[str] = None,
        backend_type: Optional[str] = None,
        rarity: Optional[BrCosmeticRarity] = None,
        display_rarity: Optional[str] = None,
        backend_rarity: Optional[str] = None,
        has_series: Optional[bool] = None,
        series: Optional[str] = None,
        backend_series: Optional[str] = None,
        has_set: Optional[bool] = None,
        set: Optional[str] = None,
        set_text: Optional[str] = None,
        backend_set: Optional[str] = None,
        has_introduction: Optional[bool] = None,
        backend_introduction: Optional[int] = None,
        introduction_chapter: Optional[str] = None,
        introduction_season: Optional[str] = None,
        has_featured_image: Optional[bool] = None,
        has_variants: Optional[bool] = None,
        has_gameplay_tags: Optional[bool] = None,
        gameplay_tag: Optional[str] = None,
        has_meta_tags: Optional[bool] = None,
        meta_tag: Optional[str] = None,
        has_dynamic_pak_id: Optional[bool] = None,
        dynamic_pak_id: Optional[str] = None,
        added: Optional[datetime.datetime] = None,
        added_since: Optional[datetime.datetime] = None,
        unseen_for: Optional[int] = None,
        last_appearance: Optional[int] = None,
    ) -> List[BrCosmetic]:
        ...

    @overload
    async def search_cosmetic(
        self,
        *,
        multiple: Literal[False] = False,
        language: Optional[GameLanguage] = None,
        search_language: Optional[GameLanguage] = None,
        match_method: Optional[MatchMethod] = None,
        id: Optional[str] = None,
        name: Optional[str] = None,
        descripion: Optional[str] = None,
        type: Optional[BrCosmeticType] = None,
        display_type: Optional[str] = None,
        backend_type: Optional[str] = None,
        rarity: Optional[BrCosmeticRarity] = None,
        display_rarity: Optional[str] = None,
        backend_rarity: Optional[str] = None,
        has_series: Optional[bool] = None,
        series: Optional[str] = None,
        backend_series: Optional[str] = None,
        has_set: Optional[bool] = None,
        set: Optional[str] = None,
        set_text: Optional[str] = None,
        backend_set: Optional[str] = None,
        has_introduction: Optional[bool] = None,
        backend_introduction: Optional[int] = None,
        introduction_chapter: Optional[str] = None,
        introduction_season: Optional[str] = None,
        has_featured_image: Optional[bool] = None,
        has_variants: Optional[bool] = None,
        has_gameplay_tags: Optional[bool] = None,
        gameplay_tag: Optional[str] = None,
        has_meta_tags: Optional[bool] = None,
        meta_tag: Optional[str] = None,
        has_dynamic_pak_id: Optional[bool] = None,
        dynamic_pak_id: Optional[str] = None,
        added: Optional[datetime.datetime] = None,
        added_since: Optional[datetime.datetime] = None,
        unseen_for: Optional[int] = None,
        last_appearance: Optional[int] = None,
    ) -> BrCosmetic:
        ...

    async def search_cosmetic(
        self,
        *,
        multiple: Optional[bool] = False,
        language: Optional[GameLanguage] = None,
        search_language: Optional[GameLanguage] = None,
        match_method: Optional[MatchMethod] = None,
        id: Optional[str] = None,
        name: Optional[str] = None,
        descripion: Optional[str] = None,
        type: Optional[BrCosmeticType] = None,
        display_type: Optional[str] = None,
        backend_type: Optional[str] = None,
        rarity: Optional[BrCosmeticRarity] = None,
        display_rarity: Optional[str] = None,
        backend_rarity: Optional[str] = None,
        has_series: Optional[bool] = None,
        series: Optional[str] = None,
        backend_series: Optional[str] = None,
        has_set: Optional[bool] = None,
        set: Optional[str] = None,
        set_text: Optional[str] = None,
        backend_set: Optional[str] = None,
        has_introduction: Optional[bool] = None,
        backend_introduction: Optional[int] = None,
        introduction_chapter: Optional[str] = None,
        introduction_season: Optional[str] = None,
        has_featured_image: Optional[bool] = None,
        has_variants: Optional[bool] = None,
        has_gameplay_tags: Optional[bool] = None,
        gameplay_tag: Optional[str] = None,
        has_meta_tags: Optional[bool] = None,
        meta_tag: Optional[str] = None,
        has_dynamic_pak_id: Optional[bool] = None,
        dynamic_pak_id: Optional[str] = None,
        added: Optional[datetime.datetime] = None,
        added_since: Optional[datetime.datetime] = None,
        unseen_for: Optional[int] = None,
        last_appearance: Optional[int] = None,
    ) -> Union[BrCosmetic, List[BrCosmetic]]:
        params: Dict[str, Any] = {}

        if language is not None:
            params['language'] = language.value

        if search_language is not None:
            params['searchLanguage'] = search_language.value

        if match_method is not None:
            params['matchMethod'] = match_method.value

        if id is not None:
            params['id'] = id

        if name is not None:
            params['name'] = name

        if descripion is not None:
            params['description'] = descripion

        if type is not None:
            params['type'] = type.value

        if display_type is not None:
            params['displayType'] = display_type

        if backend_type is not None:
            params['backendType'] = backend_type

        if rarity is not None:
            params['rarity'] = rarity.value

        if display_rarity is not None:
            params['displayRarity'] = display_rarity

        if backend_rarity is not None:
            params['backendRarity'] = backend_rarity

        if has_series is not None:
            params['hasSeries'] = has_series

        if series is not None:
            params['series'] = series

        if backend_series is not None:
            params['backendSeries'] = backend_series

        if has_set is not None:
            params['hasSet'] = has_set

        if set is not None:
            params['set'] = set

        if set_text is not None:
            params['setText'] = set_text

        if backend_set is not None:
            params['backendSet'] = backend_set

        if has_introduction is not None:
            params['hasIntroduction'] = has_introduction

        if backend_introduction is not None:
            params['backendIntroduction'] = backend_introduction

        if introduction_chapter is not None:
            params['introductionChapter'] = introduction_chapter

        if introduction_season is not None:
            params['introductionSeason'] = introduction_season

        if has_featured_image is not None:
            params['hasFeaturedImage'] = has_featured_image

        if has_variants is not None:
            params['hasVariants'] = has_variants

        if has_gameplay_tags is not None:
            params['hasGameplayTags'] = has_gameplay_tags

        if gameplay_tag is not None:
            params['gameplayTag'] = gameplay_tag

        if has_meta_tags is not None:
            params['hasMetaTags'] = has_meta_tags

        if meta_tag is not None:
            params['metaTag'] = meta_tag

        if has_dynamic_pak_id is not None:
            params['hasDynamicPakId'] = has_dynamic_pak_id

        if dynamic_pak_id is not None:
            params['dynamicPakId'] = dynamic_pak_id

        if added is not None:
            params['added'] = time.mktime(added.timetuple())

        if added_since is not None:
            params['addedSince'] = time.mktime(added_since.timetuple())

        if unseen_for is not None:
            params['unseenFor'] = unseen_for

        if last_appearance is not None:
            params['lastAppearance'] = last_appearance

        if multiple is True:
            data = await self.http.search_cosmetic_all(**params)
            return [BrCosmetic(entry) for entry in data]

        data = await self.http.search_cosmetic(**params)
        return BrCosmetic(data)

    async def fetch_creator_code(self, name: str, /) -> CreatorCode:
        data = await self.http.get_creator_code(name)
        return CreatorCode(data=data)

    async def fetch_map(self, *, language: Optional[GameLanguage] = None) -> Map:
        data = await self.http.get_map(language=(language and language.value))
        return Map(data=data)

    async def fetch_news(self, *, language: Optional[GameLanguage] = None) -> News:
        data = await self.http.get_news(language=(language and language.value))
        return News(data=data)

    async def fetch_br_news(self, *, language: Optional[GameLanguage] = None) -> GameModeNews:
        data = await self.http.get_br_news(language=(language and language.value))
        return GameModeNews(data=data)

    async def fetch_stw_news(self, *, language: Optional[GameLanguage] = None) -> GameModeNews:
        data = await self.http.get_stw_news(language=(language and language.value))
        return GameModeNews(data=data)

    async def fetch_creative_news(self, *, language: Optional[GameLanguage] = None) -> GameModeNews:
        data = await self.http.get_creative_news(language=(language and language.value))
        return GameModeNews(data=data)

    async def fetch_playlist(self, id: str, /, *, language: Optional[GameLanguage] = None) -> Playlist:
        data = await self.http.get_playlist(id, language=(language and language.value))
        return Playlist(data=data)

    async def fetch_br_shop(self, *, language: Optional[GameLanguage] = None) -> BrShop:
        data = await self.http.get_br_shop(language=(language and language.value))
        return BrShop(data=data)

    async def fetch_br_shop_combined(self, *, language: Optional[GameLanguage] = None) -> BrShop:
        raise NotImplementedError('the fawk?')

    async def fetch_br_stats(
        self,
        name: str,
        /,
        *,
        type: AccountType = AccountType.EPIC,
        time_window: TimeWindow = TimeWindow.LIFETIME,
        image: StatsImageType = StatsImageType.ALL,
    ) -> BrPlayerStats:
        data = await self.http.get_br_stats(
            name=name, account_type=type.value, time_window=time_window.value, image=image.value
        )
        return BrPlayerStats(data=data)

    async def fetch_br_stats_by_id(
        self, id: str, /, *, time_window: TimeWindow = TimeWindow.LIFETIME, image: StatsImageType = StatsImageType.ALL
    ) -> BrPlayerStats:
        data = await self.http.get_br_stats_by_id(id=id, time_window=time_window.value, image=image.value)
        return BrPlayerStats(data=data)
