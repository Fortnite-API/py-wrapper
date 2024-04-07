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
from .all import CosmeticsAll
from .banner import Banner, BannerColor
from .cosmetics import CosmeticBr, CosmeticCar, CosmeticInstrument, CosmeticLego, CosmeticLegoKit, CosmeticTrack
from .creator_code import CreatorCode
from .enums import *
from .http import HTTPClient, SyncHTTPClient
from .map import Map
from .new import NewBrCosmetics, NewCosmetics
from .news import GameModeNews, News
from .playlist import Playlist

# from .shop import BrShop
from .stats import BrPlayerStats
from .utils import copy_doc, remove_prefix

T = TypeVar('T')
TC = TypeVar('TC')
P = ParamSpec('P')


class FortniteAPI:
    """Represents a Fortnite API client. This is the main class used to interact with the Fortnite API.

    Parameters
    ----------
    api_key: Optional[:class:`str`]
        The API key to use for the client. Defaults to ``None``.
    default_language: :class:`GameLanguage`
        The default language to display the data in. Defaults to :attr:`GameLanguage.ENGLISH`.
    session: Optional[:class:`aiohttp.ClientSession`]
        The session to use for the HTTP requests. Defaults to ``None``. If not provided, a new session will be created for you.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        default_language: GameLanguage = GameLanguage.ENGLISH,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        self.http: HTTPClient = HTTPClient(session=session, token=api_key)
        self.default_language: Optional[GameLanguage] = default_language

    async def __aenter__(self) -> Self:
        if self.http.session is None:
            self.http.session = aiohttp.ClientSession()

        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.http.close()

    def _resolve_language_value(self, language: Optional[GameLanguage]) -> str:
        lang = language or self.default_language or GameLanguage.ENGLISH
        return lang.value

    # COSMETICS
    async def fetch_cosmetics_all(self, *, language: Optional[GameLanguage] = None) -> CosmeticsAll:
        """|coro|

        Fetches all cosmetics available in Fortnite.

        Parameters
        ----------
        language: Optional[:class:`GameLanguage`]
            The language to display the cosmetics in. Defaults to ``None``.
            This will override the default language set in the client.

        Returns
        -------
        :class:`CosmeticsAll`
            The fetched cosmetics.
        """
        data = await self.http.get_cosmetics_all(language=self._resolve_language_value(language))
        return CosmeticsAll(data=data, http=self.http)

    async def fetch_cosmetics_br(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticBr]:
        """|coro|

        Fetches all Battle Royale cosmetics available in Fortnite.

        Parameters
        ----------
        language: Optional[:class:`GameLanguage`]
            The language to display the cosmetics in. Defaults to ``None``.
            This will override the default language set in the client.

        Returns
        -------
        List[:class:`CosmeticBr`]
            The fetched Battle Royale cosmetics.
        """
        data = await self.http.get_cosmetics_br(language=self._resolve_language_value(language))
        return [CosmeticBr(data=entry, http=self.http) for entry in data]

    async def fetch_cosmetics_cars(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticCar]:
        """|coro|

        Fetches all Car cosmetics available in Fortnite.

        Parameters
        ----------
        language: Optional[:class:`GameLanguage`]
            The language to display the cosmetics in. Defaults to ``None``.
            This will override the default language set in the client.

        Returns
        -------
        List[:class:`CosmeticCar`]
            The fetched car cosmetics.
        """
        data = await self.http.get_cosmetics_cars(language=self._resolve_language_value(language))
        return [CosmeticCar(data=entry, http=self.http) for entry in data]

    async def fetch_cosmetics_instruments(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticInstrument]:
        """|coro|

        Fetches all instruments available in Fortnite.

        Parameters
        ----------
        language: Optional[:class:`GameLanguage`]
            The language to display the cosmetics in. Defaults to ``None``.
            This will override the default language set in the client.

        Returns
        -------
        List[:class:`CosmeticInstrument`]
            The fetched instruments.
        """
        data = await self.http.get_cosmetics_instruments(language=self._resolve_language_value(language))
        return [CosmeticInstrument(data=entry, http=self.http) for entry in data]

    async def fetch_cosmetics_lego_kits(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticLegoKit]:
        """|coro|

        Fetches all lego kits available in Fortnite.

        Parameters
        ----------
        language: Optional[:class:`GameLanguage`]
            The language to display the cosmetics in. Defaults to ``None``.
            This will override the default language set in the client.

        Returns
        -------
        List[:class:`CosmeticLegoKit`]
            The fetched lego kits.
        """
        data = await self.http.get_cosmetics_lego_kits(language=self._resolve_language_value(language))
        return [CosmeticLegoKit(data=entry, http=self.http) for entry in data]

    async def fetch_cosmetics_lego(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticLego]:
        """|coro|

        Fetches all lego cosmetics available in Fortnite.

        Parameters
        ----------
        language: Optional[:class:`GameLanguage`]
            The language to display the cosmetics in. Defaults to ``None``.
            This will override the default language set in the client.

        Returns
        -------
        List[:class:`CosmeticLego`]
            The fetched lego cosmetics.
        """
        data = await self.http.get_cosmetics_lego(language=self._resolve_language_value(language))
        return [CosmeticLego(data=entry, http=self.http) for entry in data]

    async def fetch_cosmetics_tracks(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticTrack]:
        """|coro|

        Fetches all audio tracks available in Fortnite.

        Parameters
        ----------
        language: Optional[:class:`GameLanguage`]
            The language to display the cosmetics in. Defaults to ``None``.
            This will override the default language set in the client.

        Returns
        -------
        List[:class:`CosmeticTrack`]
            The fetched audio tracks.
        """
        data = await self.http.get_cosmetics_tracks(language=self._resolve_language_value(language))
        return [CosmeticTrack(data=entry, http=self.http) for entry in data]

    async def fetch_cosmetic_br(self, /, cosmetic_id: str, *, language: Optional[GameLanguage] = None) -> CosmeticBr:
        """|coro|

        Fetch a specific Battle Royale cosmetic by its ID.

        Parameters
        ----------
        cosmetic_id: :class:`str`
            The ID of the cosmetic to fetch.
        language: Optional[:class:`GameLanguage`]
            The language to display the cosmetics in. Defaults to ``None``.
            This will override the default language set in the client.

        Returns
        -------
        :class:`CosmeticBr`
            The cosmetic fetched.
        """
        data = await self.http.get_cosmetic_br(cosmetic_id, language=self._resolve_language_value(language))
        return CosmeticBr(data=data, http=self.http)

    # NEW COSMETICS

    async def fetch_cosmetics_br_new(self) -> NewBrCosmetics:
        """|coro|

        Fetches all new Battle Royale cosmetics recently made available to Fortnite.

        Returns
        -------
        :class:`NewBrCosmetics`
            The fetched new Battle Royale cosmetics.
        """
        data = await self.http.get_cosmetics_br_new()
        return NewBrCosmetics(data=data, http=self.http)

    async def fetch_cosmetics_new(self) -> NewCosmetics:
        """|coro|

        Fetches all new cosmetics recently made available to Fortnite. This encompasses all cosmetics available in the game.

        Returns
        -------
        :class:`NewCosmetics`
            The fetched new cosmetics.
        """
        data = await self.http.get_cosmetics_new()
        return NewCosmetics(data=data, http=self.http)

    # AES

    async def fetch_aes(self, *, key_format: KeyFormat = KeyFormat.HEX) -> Aes:
        """|coro|

        Fetches the AES key used to decrypt encrypted data from Fortnite.

        Parameters
        ----------
        key_format: :class:`KeyFormat`
            The format to return the key in. Defaults to :attr:`KeyFormat.HEX`.

        Returns
        -------
        :class:`Aes`
            The fetched AES key.
        """
        data = await self.http.get_aes(key_format.value)
        return Aes(data=data)

    # BANNERS
    async def fetch_banners(self, *, language: Optional[GameLanguage] = None) -> List[Banner]:
        """|coro|

        Fetch all banners available in Fortnite.

        Parameters
        ----------
        language: Optional[:class:`GameLanguage`]
            The language to display the banners in. Defaults to ``None``.
            This will override the default language set in the client.

        Returns
        -------
        List[:class:`Banner`]
            The fetched banners.
        """
        data = await self.http.get_banners(language=self._resolve_language_value(language))
        return [Banner(data=entry, http=self.http) for entry in data]

    async def fetch_banner_colors(self) -> List[BannerColor]:
        """|coro|

        Fetch all banner colors available in Fortnite.

        Returns
        -------
        List[:class:`BannerColor`]
            The fetched banner colors.
        """
        data = await self.http.get_banner_colors()
        return [BannerColor(data=entry) for entry in data]

    # CREATOR CODES

    async def fetch_creator_code(self, /, *, name: str) -> CreatorCode:
        """|coro|

        Fetch information about a creator code in Fortnite from its name.

        Parameters
        ----------
        name: :class:`str`
            The name of the creator code to fetch.

        Returns
        -------
        :class:`CreatorCode`
            The fetched creator code.
        """
        data = await self.http.get_creator_code(name)
        return CreatorCode(data=data)

    # MAPS

    async def fetch_map(self, *, language: Optional[GameLanguage] = None) -> Map:
        data = await self.http.get_map(language=self._resolve_language_value(language))
        return Map(data=data, http=self.http)

    # NEWS

    async def fetch_news(self, *, language: Optional[GameLanguage] = None) -> News:
        data = await self.http.get_news(language=self._resolve_language_value(language))
        return News(data=data, http=self.http)

    async def fetch_news_br(self, *, language: Optional[GameLanguage] = None) -> GameModeNews:
        data = await self.http.get_news_br(language=self._resolve_language_value(language))
        return GameModeNews(data=data, http=self.http)

    async def fetch_news_stw(self, *, language: Optional[GameLanguage] = None) -> GameModeNews:
        data = await self.http.get_news_stw(language=self._resolve_language_value(language))
        return GameModeNews(data=data, http=self.http)

    # PLAYLISTS

    async def fetch_playlists(self, /, *, language: Optional[GameLanguage] = None) -> List[Playlist]:
        data = await self.http.get_playlists(language=self._resolve_language_value(language))
        return [Playlist(data=entry) for entry in data]

    async def fetch_playlist(self, id: str, /, *, language: Optional[GameLanguage] = None) -> Playlist:
        data = await self.http.get_playlist(id, language=self._resolve_language_value(language))
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
    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        default_language: GameLanguage = GameLanguage.ENGLISH,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.http: SyncHTTPClient = SyncHTTPClient(session=session, token=api_key)
        self.default_language: Optional[GameLanguage] = default_language

    # For with statement
    def __enter__(self) -> Self:
        if self.http.session is None:
            self.http.session = requests.Session()

        return self

    def __exit__(self, *args: Any) -> None:
        self.http.close()

    def _resolve_language_value(self, language: Optional[GameLanguage]) -> str:
        lang = language or self.default_language or GameLanguage.ENGLISH
        return lang.value

    # COSMETICS
    @remove_prefix("|coro|")
    @copy_doc(FortniteAPI.fetch_cosmetics_cars)
    def fetch_cosmetics_cars(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticCar[SyncHTTPClient]]:
        data = self.http.get_cosmetics_cars(language=self._resolve_language_value(language))
        return [CosmeticCar(data=entry, http=self.http) for entry in data]

    @remove_prefix('|coro|')
    @copy_doc(FortniteAPI.fetch_cosmetics_instruments)
    def fetch_cosmetics_instruments(
        self, *, language: Optional[GameLanguage] = None
    ) -> List[CosmeticInstrument[SyncHTTPClient]]:
        data = self.http.get_cosmetics_instruments(language=self._resolve_language_value(language))
        return [CosmeticInstrument(data=entry, http=self.http) for entry in data]

    @remove_prefix('|coro|')
    @copy_doc(FortniteAPI.fetch_cosmetics_lego_kits)
    def fetch_cosmetics_lego_kits(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticLegoKit[SyncHTTPClient]]:
        data = self.http.get_cosmetics_lego_kits(language=self._resolve_language_value(language))
        return [CosmeticLegoKit(data=entry, http=self.http) for entry in data]

    @remove_prefix('|coro|')
    @copy_doc(FortniteAPI.fetch_cosmetics_tracks)
    def fetch_cosmetics_tracks(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticTrack[SyncHTTPClient]]:
        data = self.http.get_cosmetics_tracks(language=self._resolve_language_value(language))
        return [CosmeticTrack(data=entry, http=self.http) for entry in data]

    @remove_prefix('|coro|')
    @copy_doc(FortniteAPI.fetch_cosmetics_br)
    def fetch_cosmetics_br(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticBr[SyncHTTPClient]]:
        data = self.http.get_cosmetics_br(language=self._resolve_language_value(language))
        return [CosmeticBr(data=entry, http=self.http) for entry in data]

    @remove_prefix('|coro|')
    @copy_doc(FortniteAPI.fetch_cosmetic_br)
    def fetch_cosmetic_br(
        self, /, cosmetic_id: str, *, language: Optional[GameLanguage] = None
    ) -> CosmeticBr[SyncHTTPClient]:
        data = self.http.get_cosmetic_br(cosmetic_id, language=self._resolve_language_value(language))
        return CosmeticBr(data=data, http=self.http)

    @remove_prefix('|coro|')
    @copy_doc(FortniteAPI.fetch_cosmetics_lego)
    def fetch_cosmetics_lego(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticLego[SyncHTTPClient]]:
        data = self.http.get_cosmetics_lego(language=self._resolve_language_value(language))
        return [CosmeticLego(data=entry, http=self.http) for entry in data]

    @remove_prefix('|coro|')
    @copy_doc(FortniteAPI.fetch_cosmetics_all)
    def fetch_cosmetics_all(self, *, language: Optional[GameLanguage] = None) -> CosmeticsAll[SyncHTTPClient]:
        data = self.http.get_cosmetics_all(language=self._resolve_language_value(language))
        return CosmeticsAll(data=data, http=self.http)

    # NEW COSMETICS

    @remove_prefix('|coro|')
    @copy_doc(FortniteAPI.fetch_cosmetics_br_new)
    def fetch_cosmetics_br_new(self) -> NewBrCosmetics[SyncHTTPClient]:
        data = self.http.get_cosmetics_br_new()
        return NewBrCosmetics(data=data, http=self.http)

    @remove_prefix('|coro|')
    @copy_doc(FortniteAPI.fetch_cosmetics_new)
    def fetch_cosmetics_new(self) -> NewCosmetics[SyncHTTPClient]:
        data = self.http.get_cosmetics_new()
        return NewCosmetics(data=data, http=self.http)

    # AES

    @remove_prefix('|coro|')
    @copy_doc(FortniteAPI.fetch_aes)
    def fetch_aes(self, *, key_format: KeyFormat = KeyFormat.HEX) -> Aes:
        data = self.http.get_aes(key_format.value)
        return Aes(data=data)

    # BANNERS
    @remove_prefix('|coro|')
    @copy_doc(FortniteAPI.fetch_banners)
    def fetch_banners(self, *, language: Optional[GameLanguage] = None) -> List[Banner[SyncHTTPClient]]:
        data = self.http.get_banners(language=self._resolve_language_value(language))
        return [Banner(data=entry, http=self.http) for entry in data]

    @remove_prefix('|coro|')
    @copy_doc(FortniteAPI.fetch_banner_colors)
    def fetch_banner_colors(self) -> List[BannerColor]:
        data = self.http.get_banner_colors()
        return [BannerColor(data=entry) for entry in data]

    # CREATOR CODES

    @remove_prefix('|coro|')
    @copy_doc(FortniteAPI.fetch_creator_code)
    def fetch_creator_code(self, /, *, name: str) -> CreatorCode:
        data = self.http.get_creator_code(name)
        return CreatorCode(data=data)

    # MAPS

    def fetch_map(self, *, language: Optional[GameLanguage] = None) -> Map[SyncHTTPClient]:
        data = self.http.get_map(language=self._resolve_language_value(language))
        return Map(data=data, http=self.http)

    # NEWS

    def fetch_news(self, *, language: Optional[GameLanguage] = None) -> News[SyncHTTPClient]:
        data = self.http.get_news(language=self._resolve_language_value(language))
        return News(data=data, http=self.http)

    def fetch_news_br(self, *, language: Optional[GameLanguage] = None) -> GameModeNews[SyncHTTPClient]:
        data = self.http.get_news_br(language=self._resolve_language_value(language))
        return GameModeNews(data=data, http=self.http)

    def fetch_news_stw(self, *, language: Optional[GameLanguage] = None) -> GameModeNews[SyncHTTPClient]:
        data = self.http.get_news_stw(language=self._resolve_language_value(language))
        return GameModeNews(data=data, http=self.http)

    # PLAYLISTS

    def fetch_playlists(self, /, *, language: Optional[GameLanguage] = None) -> List[Playlist]:
        data = self.http.get_playlists(language=self._resolve_language_value(language))
        return [Playlist(data=entry) for entry in data]

    def fetch_playlist(self, id: str, /, *, language: Optional[GameLanguage] = None) -> Playlist:
        data = self.http.get_playlist(id, language=self._resolve_language_value(language))
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
