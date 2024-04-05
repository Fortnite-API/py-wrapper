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

from typing import Any, List, Optional, TypeVar

import aiohttp
import requests
from typing_extensions import ParamSpec, Self

from .aes import Aes
from .banner import Banner, BannerColor
from .cosmetics import CosmeticBr, CosmeticCar, CosmeticInstrument, CosmeticLegoKit, CosmeticTrack
from .creator_code import CreatorCode
from .enums import *
from .http import HTTPClient, SyncHTTPClient
from .map import Map
from .new import NewBrCosmetics, NewCosmetics
from .news import GameModeNews, News
from .playlist import Playlist

# from .shop import BrShop
from .stats import BrPlayerStats

T = TypeVar('T')
TC = TypeVar('TC')
P = ParamSpec('P')


class FortniteAPI:
    def __init__(self, api_key: Optional[str] = None, *, session: Optional[aiohttp.ClientSession] = None) -> None:
        self.http: HTTPClient = HTTPClient(session=session, token=api_key)

    async def __aenter__(self) -> Self:
        if self.http.session is None:
            self.http.session = aiohttp.ClientSession()

        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.http.close()

    # COSMETICS
    async def fetch_cosmetics_cars(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticCar[HTTPClient]]:
        data = await self.http.get_cosmetics_cars(language=(language and language.value))
        return [CosmeticCar(data=entry, http=self.http) for entry in data]

    async def fetch_cosmetics_instruments(
        self, *, language: Optional[GameLanguage] = None
    ) -> List[CosmeticInstrument[HTTPClient]]:
        data = await self.http.get_cosmetics_instruments(language=(language and language.value))
        return [CosmeticInstrument(data=entry, http=self.http) for entry in data]

    async def fetch_cosmetics_lego_kits(
        self, *, language: Optional[GameLanguage] = None
    ) -> List[CosmeticLegoKit[HTTPClient]]:
        data = await self.http.get_cosmetics_lego_kits(language=(language and language.value))
        return [CosmeticLegoKit(data=entry, http=self.http) for entry in data]

    async def fetch_cosmetics_tracks(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticTrack[HTTPClient]]:
        data = await self.http.get_cosmetics_tracks(language=(language and language.value))
        return [CosmeticTrack(data=entry, http=self.http) for entry in data]

    async def fetch_cosmetics_br(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticBr[HTTPClient]]:
        data = await self.http.get_cosmetics_br(language=(language and language.value))
        return [CosmeticBr(data=entry, http=self.http) for entry in data]

    async def fetch_cosmetic_br(
        self, /, cosmetic_id: str, *, language: Optional[GameLanguage] = None
    ) -> CosmeticBr[HTTPClient]:
        data = await self.http.get_cosmetic_br(cosmetic_id, language=(language and language.value))
        return CosmeticBr(data=data, http=self.http)

    # NEW COSMETICS

    async def fetch_cosmetics_br_new(self) -> NewBrCosmetics:
        data = await self.http.get_cosmetics_br_new()
        return NewBrCosmetics(data=data, http=self.http)

    async def fetch_cosmetics_new(self) -> NewCosmetics:
        data = await self.http.get_cosmetics_new()
        return NewCosmetics(data=data, http=self.http)

    # AES

    async def fetch_aes(self, *, key_format: KeyFormat = KeyFormat.HEX) -> Aes:
        data = await self.http.get_aes(key_format.value)
        return Aes(data=data)

    # BANNERS
    async def fetch_banners(self, *, language: Optional[GameLanguage] = None) -> List[Banner[HTTPClient]]:
        data = await self.http.get_banners(language=(language and language.value))
        return [Banner(data=entry, http=self.http) for entry in data]

    async def fetch_banner_colors(self) -> List[BannerColor]:
        data = await self.http.get_banner_colors()
        return [BannerColor(data=entry) for entry in data]

    # CREATOR CODES

    async def fetch_creator_code(self, name: str, /) -> CreatorCode:
        data = await self.http.get_creator_code(name)
        return CreatorCode(data=data)

    # MAPS

    async def fetch_map(self, *, language: Optional[GameLanguage] = None) -> Map:
        data = await self.http.get_map(language=(language and language.value))
        return Map(data=data)

    # NEWS

    async def fetch_news(self, *, language: Optional[GameLanguage] = None) -> News:
        data = await self.http.get_news(language=(language and language.value))
        return News(data=data)

    async def fetch_news_br(self, *, language: Optional[GameLanguage] = None) -> GameModeNews:
        data = await self.http.get_news_br(language=(language and language.value))
        return GameModeNews(data=data)

    async def fetch_news_stw(self, *, language: Optional[GameLanguage] = None) -> GameModeNews:
        data = await self.http.get_news_stw(language=(language and language.value))
        return GameModeNews(data=data)

    # PLAYLISTS

    async def fetch_playlists(self, /, *, language: Optional[GameLanguage] = None) -> List[Playlist]:
        data = await self.http.get_playlists(language=(language and language.value))
        return [Playlist(data=entry) for entry in data]

    async def fetch_playlist(self, id: str, /, *, language: Optional[GameLanguage] = None) -> Playlist:
        data = await self.http.get_playlist(id, language=(language and language.value))
        return Playlist(data=data)

    # PLAYER STATS

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
        data = await self.http.get_br_stats_by_id(account_id=id, time_window=time_window.value, image=image.value)
        return BrPlayerStats(data=data)


class SyncFortniteAPI:
    def __init__(self, api_key: Optional[str] = None, *, session: Optional[requests.Session] = None) -> None:
        self.http: SyncHTTPClient = SyncHTTPClient(session=session, token=api_key)

    # For with statement
    def __enter__(self) -> Self:
        if self.http.session is None:
            self.http.session = requests.Session()

        return self

    def __exit__(self, *args: Any) -> None:
        self.http.close()

    # COSMETICS

    # AES

    def fetch_aes(self, *, key_format: KeyFormat = KeyFormat.HEX) -> Aes:
        data = self.http.get_aes(key_format.value)
        return Aes(data=data)

    # BANNERS
    def fetch_banners(self, *, language: Optional[GameLanguage] = None) -> List[Banner[SyncHTTPClient]]:
        data = self.http.get_banners(language=(language and language.value))
        return [Banner(data=entry, http=self.http) for entry in data]

    def fetch_banner_colors(self) -> List[BannerColor]:
        data = self.http.get_banner_colors()
        return [BannerColor(data=entry) for entry in data]

    # CREATOR CODES

    def fetch_creator_code(self, name: str, /) -> CreatorCode:
        data = self.http.get_creator_code(name)
        return CreatorCode(data=data)

    # MAPS

    def fetch_map(self, *, language: Optional[GameLanguage] = None) -> Map:
        data = self.http.get_map(language=(language and language.value))
        return Map(data=data)

    # NEWS

    def fetch_news(self, *, language: Optional[GameLanguage] = None) -> News:
        data = self.http.get_news(language=(language and language.value))
        return News(data=data)

    def fetch_news_br(self, *, language: Optional[GameLanguage] = None) -> GameModeNews:
        data = self.http.get_news_br(language=(language and language.value))
        return GameModeNews(data=data)

    def fetch_news_stw(self, *, language: Optional[GameLanguage] = None) -> GameModeNews:
        data = self.http.get_news_stw(language=(language and language.value))
        return GameModeNews(data=data)

    # PLAYLISTS

    def fetch_playlists(self, /, *, language: Optional[GameLanguage] = None) -> List[Playlist]:
        data = self.http.get_playlists(language=(language and language.value))
        return [Playlist(data=entry) for entry in data]

    def fetch_playlist(self, id: str, /, *, language: Optional[GameLanguage] = None) -> Playlist:
        data = self.http.get_playlist(id, language=(language and language.value))
        return Playlist(data=data)

    # PLAYER STATS

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
        data = self.http.get_br_stats_by_id(account_id=id, time_window=time_window.value, image=image.value)
        return BrPlayerStats(data=data)
