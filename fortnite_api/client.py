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
import functools
import inspect
from typing import Any, Callable, List, Literal, Optional, TypeVar, Union, cast, overload

import aiohttp
import requests
from typing_extensions import Concatenate, Coroutine, ParamSpec, Self

from .aes import Aes
from .all import CosmeticsAll
from .banner import Banner, BannerColor
from .cosmetics import CosmeticBr, CosmeticCar, CosmeticInstrument, CosmeticLego, CosmeticLegoKit, CosmeticTrack
from .creator_code import CreatorCode
from .enums import *
from .errors import BetaAccessNotEnabled, BetaUnknownException, MissingAPIKey
from .flags import OptimizationFlags
from .http import HTTPClient, SyncHTTPClient
from .map import Map
from .material import MaterialInstance
from .new import NewBrCosmetics, NewCosmetics
from .news import GameModeNews, News
from .playlist import Playlist
from .proxies import TransformerListProxy
from .shop import Shop
from .stats import BrPlayerStats
from .utils import _transform_dict_for_get_request, copy_doc, remove_prefix

T = TypeVar('T')
TC = TypeVar('TC')
P = ParamSpec('P')
FortniteAPI_T = TypeVar('FortniteAPI_T', bound='FortniteAPI')
SyncFortniteAPI_T = TypeVar('SyncFortniteAPI_T', bound='SyncFortniteAPI')

FetchFunc = Callable[Concatenate[FortniteAPI_T, P], Coroutine[Any, Any, T]]
SyncFetchFunc = Callable[Concatenate[SyncFortniteAPI_T, P], T]


def _remove_coro_doc(cls: T) -> T:
    # Runs through all the functions of the object and anything
    # that has a docstring that starts with '|coro|' is removed
    for value in cls.__dict__.values():
        try:
            doc = getattr(value, '__doc__')
        except AttributeError:
            continue
        else:
            if doc and doc.startswith('|coro|'):
                remove_prefix('|coro|')(value)

    return cls


@overload
def beta_method(func: FetchFunc[FortniteAPI_T, P, T]) -> FetchFunc[FortniteAPI_T, P, T]: ...


@overload
def beta_method(func: SyncFetchFunc[SyncFortniteAPI_T, P, T]) -> SyncFetchFunc[SyncFortniteAPI_T, P, T]: ...


def beta_method(
    func: Union[FetchFunc[FortniteAPI_T, P, T], SyncFetchFunc[SyncFortniteAPI_T, P, T]]
) -> Union[FetchFunc[FortniteAPI_T, P, T], SyncFetchFunc[SyncFortniteAPI_T, P, T]]:
    if inspect.iscoroutinefunction(func):
        # This is coroutine, so we need to wrap it in an async function
        @functools.wraps(func)
        async def _wrapped_async_beta_method(self: FortniteAPI_T, *args: P.args, **kwargs: P.kwargs) -> T:
            if not self.beta:
                raise BetaAccessNotEnabled("Beta access is not enabled for this client.")

            try:
                return await func(self, *args, **kwargs)
            except Exception as exc:
                raise BetaUnknownException(original=exc) from exc

        return _wrapped_async_beta_method
    else:
        # Pyright cannot automatically infer the return type of
        # this function, so we need to manually specify it.
        func = cast(SyncFetchFunc[SyncFortniteAPI_T, P, T], func)

        @functools.wraps(func)
        def _wrapped_sync_beta_method(self: SyncFortniteAPI_T, *args: P.args, **kwargs: P.kwargs) -> T:
            if not self.beta:
                raise BetaAccessNotEnabled("Beta access is not enabled for this client.")

            try:
                return func(self, *args, **kwargs)
            except Exception as exc:
                raise BetaUnknownException(original=exc) from exc

        return _wrapped_sync_beta_method


class FortniteAPI:
    """
    .. attributetable:: fortnite_api.FortniteAPI

    Represents a Fortnite API client. This is the main class used to interact with the Fortnite API.

    .. container:: operations

        .. describe:: async with x:

            This class is can be used as a context manager.
            This will automatically open and close the HTTP session for you. If you don't use the ``async with`` statement, you will have to manually close the session. See :ref:`client-context-managers` for more information.

    Parameters
    ----------
    api_key: Optional[:class:`str`]
        The API key to use for the client. If not provided, some endpoints may not be available.
    default_language: Optional[:class:`fortnite_api.GameLanguage`]
        The default language to display the data in. Defaults to :attr:`fortnite_api.GameLanguage.ENGLISH` if not provided.
    session: Optional[:class:`aiohttp.ClientSession`]
        The session to use for the HTTP requests. If not provided, a new session will be created for you and you must use the class as an async context manager.
    beta: :class:`bool`
        Whether or not the client can make requests to the beta API. Any beta endpoints will not be available if this is set to ``False``. Defaults to ``False``. This is to prevent accidental usage of beta endpoints.

        .. note::

            All beta endpoints are prefixed with ``beta_``.
    optimization_flags: Optional[:class:`fortnite_api.OptimizationFlags`]
        Any optimization flags to use for the client. Enabling these can speed up the client or reduce
        the amount of bandwidth used. Defaults to :meth:`fortnite_api.OptimizationFlags.default`. Pass ``None`` or :meth:`fortnite_api.OptimizationFlags.none` to remove all flags. Read the documentation for :class:`fortnite_api.OptimizationFlags` for more information.

    Attributes
    ----------
    default_language: Optional[:class:`fortnite_api.GameLanguage`]
        The default language, if any, passed to the client.
    beta: :class:`bool`
        Denotes if the client can make requests to beta endpoints.
    optimization_flags: Optional[:class:`fortnite_api.OptimizationFlags`]
        Any optimization flags set on the client.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        default_language: GameLanguage = GameLanguage.ENGLISH,
        session: Optional[aiohttp.ClientSession] = None,
        beta: bool = False,
        optimization_flags: OptimizationFlags = OptimizationFlags.default(),
    ) -> None:
        self.http: HTTPClient = HTTPClient(session=session, token=api_key, optimization_flags=optimization_flags)
        self.default_language: Optional[GameLanguage] = default_language
        self.beta: bool = beta
        self.optimization_flags: Optional[OptimizationFlags] = optimization_flags

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
        language: Optional[:class:`fortnite_api.GameLanguage`]
            The language to display the cosmetics in. Defaults to ``None``.
            This will override the default language set on the client.

        Returns
        -------
        :class:`fortnite_api.CosmeticsAll`
            The fetched cosmetics.
        """
        data = await self.http.get_cosmetics_all(language=self._resolve_language_value(language))
        return CosmeticsAll(data=data, http=self.http)

    async def fetch_cosmetics_br(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticBr]:
        """|coro|

        Fetches all Battle Royale cosmetics available in Fortnite.

        Parameters
        ----------
        language: Optional[:class:`fortnite_api.GameLanguage`]
            The language to display the cosmetics in. Defaults to ``None``.
            This will override the default language set on the client.

        Returns
        -------
        List[:class:`fortnite_api.CosmeticBr`]
            The fetched Battle Royale cosmetics.
        """
        data = await self.http.get_cosmetics_br(language=self._resolve_language_value(language))
        return TransformerListProxy(
            data,
            lambda x: CosmeticBr(data=x, http=self.http),
        )

    async def fetch_cosmetics_cars(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticCar]:
        """|coro|

        Fetches all Car cosmetics available in Fortnite.

        Parameters
        ----------
        language: Optional[:class:`fortnite_api.GameLanguage`]
            The language to display the cosmetics in. Defaults to ``None``.
            This will override the default language set on the client.

        Returns
        -------
        List[:class:`fortnite_api.CosmeticCar`]
            The fetched car cosmetics.
        """
        data = await self.http.get_cosmetics_cars(language=self._resolve_language_value(language))
        return TransformerListProxy(
            data,
            lambda x: CosmeticCar(data=x, http=self.http),
        )

    async def fetch_cosmetics_instruments(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticInstrument]:
        """|coro|

        Fetches all instrument cosmetics available in Fortnite.

        Parameters
        ----------
        language: Optional[:class:`fortnite_api.GameLanguage`]
            The language to display the cosmetics in. Defaults to ``None``.
            This will override the default language set on the client.

        Returns
        -------
        List[:class:`fortnite_api.CosmeticInstrument`]
            The fetched instruments.
        """
        data = await self.http.get_cosmetics_instruments(language=self._resolve_language_value(language))
        return TransformerListProxy(
            data,
            lambda x: CosmeticInstrument(data=x, http=self.http),
        )

    async def fetch_cosmetics_lego_kits(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticLegoKit]:
        """|coro|

        Fetches all lego kit cosmetics available in Fortnite.

        Parameters
        ----------
        language: Optional[:class:`fortnite_api.GameLanguage`]
            The language to display the cosmetics in. Defaults to ``None``.
            This will override the default language set on the client.

        Returns
        -------
        List[:class:`fortnite_api.CosmeticLegoKit`]
            The fetched lego kits.
        """
        data = await self.http.get_cosmetics_lego_kits(language=self._resolve_language_value(language))
        return TransformerListProxy(
            data,
            lambda x: CosmeticLegoKit(data=x, http=self.http),
        )

    async def fetch_cosmetics_lego(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticLego]:
        """|coro|

        Fetches all lego cosmetics available in Fortnite.

        Parameters
        ----------
        language: Optional[:class:`fortnite_api.GameLanguage`]
            The language to display the cosmetics in. Defaults to ``None``.
            This will override the default language set on the client.

        Returns
        -------
        List[:class:`fortnite_api.CosmeticLego`]
            The fetched lego cosmetics.
        """
        data = await self.http.get_cosmetics_lego(language=self._resolve_language_value(language))

        return TransformerListProxy(
            data,
            lambda x: CosmeticLego(data=x, http=self.http),
        )

    async def fetch_cosmetics_tracks(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticTrack]:
        """|coro|

        Fetches all audio track cosmetics available in Fortnite.

        Parameters
        ----------
        language: Optional[:class:`fortnite_api.GameLanguage`]
            The language to display the cosmetics in. Defaults to ``None``.
            This will override the default language set on the client.

        Returns
        -------
        List[:class:`fortnite_api.CosmeticTrack`]
            The fetched audio tracks.
        """
        data = await self.http.get_cosmetics_tracks(language=self._resolve_language_value(language))

        return TransformerListProxy(
            data,
            lambda x: CosmeticTrack(data=x, http=self.http),
        )

    async def fetch_cosmetic_br(self, /, cosmetic_id: str, *, language: Optional[GameLanguage] = None) -> CosmeticBr:
        """|coro|

        Fetch a specific Battle Royale cosmetic by its ID.

        Parameters
        ----------
        cosmetic_id: :class:`str`
            The ID of the cosmetic to fetch.
        language: Optional[:class:`fortnite_api.GameLanguage`]
            The language to display the cosmetics in. Defaults to ``None``.
            This will override the default language set on the client.

        Returns
        -------
        :class:`fortnite_api.CosmeticBr`
            The cosmetic fetched.

        Raises
        ------
        :class:`~fortnite_api.NotFound`
            A cosmetic with that ID was not found.
        """
        data = await self.http.get_cosmetic_br(cosmetic_id, language=self._resolve_language_value(language))
        return CosmeticBr(data=data, http=self.http)

    # NEW COSMETICS

    async def fetch_cosmetics_br_new(self) -> NewBrCosmetics:
        """|coro|

        Fetches all newly added Battle Royale cosmetics recently made available in Fortnite.

        Returns
        -------
        :class:`fortnite_api.NewBrCosmetics`
            The fetched new Battle Royale cosmetics.
        """
        data = await self.http.get_cosmetics_br_new()
        return NewBrCosmetics(data=data, http=self.http)

    async def fetch_cosmetics_new(self) -> NewCosmetics:
        """|coro|

        Fetches all new cosmetics recently made available in Fortnite. This encompasses all cosmetic types available in the game.

        Returns
        -------
        :class:`fortnite_api.NewCosmetics`
            The fetched new cosmetics.
        """
        data = await self.http.get_cosmetics_new()
        return NewCosmetics(data=data, http=self.http)

    @overload
    async def search_br_cosmetics(
        self,
        *,
        multiple: Literal[True] = True,
        language: GameLanguage = GameLanguage.ENGLISH,
        search_language: GameLanguage = GameLanguage.ENGLISH,
        match_method: MatchMethod = MatchMethod.FULL,
        id: Optional[str] = ...,
        name: Optional[str] = ...,
        description: Optional[str] = ...,
        type: Optional[CosmeticBrType] = ...,
        type_display: Optional[str] = ...,
        type_backend: Optional[str] = ...,
        rarity: Optional[CosmeticBrRarity] = ...,
        rarity_display: Optional[str] = ...,
        rarity_backend: Optional[str] = ...,
        has_series: Optional[bool] = ...,
        series: Optional[str] = ...,
        series_backend: Optional[str] = ...,
        has_set: Optional[bool] = ...,
        set: Optional[str] = ...,
        set_text: Optional[str] = ...,
        set_backend: Optional[str] = ...,
        has_introduction: Optional[bool] = ...,
        introduction_backend: Optional[str] = ...,
        introduction_chapter: Optional[str] = ...,
        introduction_season: Optional[str] = ...,
        has_featured_image: Optional[bool] = ...,
        has_variants: Optional[bool] = ...,
        gameplay_tag: Optional[str] = ...,
        has_meta_tags: Optional[bool] = ...,
        has_dynamic_pak_id: Optional[bool] = ...,
        dynamic_pak_id: Optional[str] = ...,
        added: Optional[datetime.datetime] = ...,
        added_since: Optional[datetime.datetime] = ...,
        unseen_for: Optional[int] = ...,
        last_appearance: Optional[datetime.datetime] = ...,
    ) -> List[CosmeticBr]: ...

    @overload
    async def search_br_cosmetics(
        self,
        *,
        multiple: Literal[False] = False,
        language: GameLanguage = GameLanguage.ENGLISH,
        search_language: GameLanguage = GameLanguage.ENGLISH,
        match_method: MatchMethod = MatchMethod.FULL,
        id: Optional[str] = ...,
        name: Optional[str] = ...,
        description: Optional[str] = ...,
        type: Optional[CosmeticBrType] = ...,
        type_display: Optional[str] = ...,
        type_backend: Optional[str] = ...,
        rarity: Optional[CosmeticBrRarity] = ...,
        rarity_display: Optional[str] = ...,
        rarity_backend: Optional[str] = ...,
        has_series: Optional[bool] = ...,
        series: Optional[str] = ...,
        series_backend: Optional[str] = ...,
        has_set: Optional[bool] = ...,
        set: Optional[str] = ...,
        set_text: Optional[str] = ...,
        set_backend: Optional[str] = ...,
        has_introduction: Optional[bool] = ...,
        introduction_backend: Optional[str] = ...,
        introduction_chapter: Optional[str] = ...,
        introduction_season: Optional[str] = ...,
        has_featured_image: Optional[bool] = ...,
        has_variants: Optional[bool] = ...,
        gameplay_tag: Optional[str] = ...,
        has_meta_tags: Optional[bool] = ...,
        has_dynamic_pak_id: Optional[bool] = ...,
        dynamic_pak_id: Optional[str] = ...,
        added: Optional[datetime.datetime] = ...,
        added_since: Optional[datetime.datetime] = ...,
        unseen_for: Optional[int] = ...,
        last_appearance: Optional[datetime.datetime] = ...,
    ) -> CosmeticBr: ...

    async def search_br_cosmetics(self, **kwargs: Any) -> Union[CosmeticBr, List[CosmeticBr]]:
        """|coro|

        Searches all Battle Royale cosmetics available in Fortnite and returns
        the best match(es) based on the search criteria. Passing any of the parameters to this function will filter the search results.

        Parameters
        ----------
        multiple: Optional[:class:`bool`]
            Denotes if multiple matches should be returned. If this is ``True`` then a
            list of matches will be returned. If ``False``, then only the best match will be returned. Defaults to ``False``.
        language: Optional[:class:`fortnite_api.GameLanguage`]
            The output language to display the cosmetics in. Will override the default language
            set on the client. Defaults to the client's :attr:`default_language` or :attr:`fortnite_api.GameLanguage.ENGLISH`.
        search_language: Optional[:class:`fortnite_api.GameLanguage`]
            The language to use for the search. Will override the default language set on the client. Defaults to
            the client's :attr:`default_language` or :attr:`fortnite_api.GameLanguage.ENGLISH`.
        match_method: Optional[:class:`fortnite_api.MatchMethod`]
            The method to use for matching the search query. Defaults to :attr:`fortnite_api.MatchMethod.FULL`.
        id: Optional[:class:`str`]
            The ID of the cosmetic.
        name: Optional[:class:`str`]
            The name of the cosmetic.
        description: Optional[:class:`str`]
            The description of the cosmetic.
        type: Optional[:class:`fortnite_api.CosmeticBrType`]
            The cosmetic's type.
        type_display: Optional[:class:`str`]
            The display type of the cosmetic.
        type_backend: Optional[:class:`str`]
            The backend type of the cosmetic.
        rarity: Optional[:class:`fortnite_api.CosmeticBrRarity`]
            The rarity of the cosmetic.
        rarity_display: Optional[:class:`str`]
            The display rarity of the cosmetic.
        rarity_backend: Optional[:class:`str`]
            The backend rarity of the cosmetic.
        has_series: Optional[:class:`bool`]
            If the cosmetic has a series.
        series: Optional[:class:`str`]
            The series of the cosmetic.
        series_backend: Optional[:class:`str`]
            The backend series of the cosmetic.
        has_set: Optional[:class:`bool`]
            If the cosmetic has a set.
        set: Optional[:class:`str`]
            The set of the cosmetic.
        set_text: Optional[:class:`str`]
            The text of the set of the cosmetic.
        set_backend: Optional[:class:`str`]
            The backend set of the cosmetic.
        has_introduction: Optional[:class:`bool`]
            If the cosmetic has an introduction.
        introduction_backend: Optional[:class:`str`]
            The backend introduction value of the cosmetic.
        introduction_chapter: Optional[:class:`str`]
            The chapter when the cosmetic was introduced.
        introduction_season: Optional[:class:`str`]
            The season that the cosmetic was introduced.
        has_featured_image: Optional[:class:`bool`]
            If the cosmetic has a featured image.
        has_variants: Optional[:class:`bool`]
            If the cosmetic has variants.
        gameplay_tag: Optional[:class:`str`]
            A gameplay tag of the cosmetic.
        has_meta_tags: Optional[:class:`bool`]
            If the cosmetic has meta tags.
        has_dynamic_pak_id: Optional[:class:`bool`]
            If the cosmetic has a dynamic pak ID.
        dynamic_pak_id: Optional[:class:`str`]
            The dynamic pak ID of the cosmetic.
        added: Optional[:class:`datetime.datetime`]
            The date when the cosmetic was added.
        added_since: Optional[:class:`datetime.datetime`]
            The date since the cosmetic was added.
        unseen_for: Optional[:class:`int`]
            The amount, in days, that the cosmetic has been unseen.
        last_appearance: Optional[:class:`datetime.datetime`]
            The last appearance of the cosmetic.

        Raises
        ------
        NotFound
            No cosmetics were found with the search criteria.
        """
        multiple = kwargs.pop('multiple')

        kwargs['language'] = self._resolve_language_value(kwargs.get('language'))
        kwargs['search_language'] = self._resolve_language_value(kwargs.get('search_language'))

        match_method = kwargs.pop('match_method', None)
        if match_method is not None:
            kwargs['match_method'] = match_method.value

        payload = _transform_dict_for_get_request(kwargs)
        if multiple is True:
            data = await self.http.search_cosmetic_all(**payload)
            return TransformerListProxy(
                data,
                lambda x: CosmeticBr(data=x, http=self.http),
            )
        else:
            data = await self.http.search_cosmetic(**payload)
            return CosmeticBr(data=data, http=self.http)

    # AES

    async def fetch_aes(self, *, key_format: KeyFormat = KeyFormat.HEX) -> Aes:
        """|coro|

        Fetches the AES key used to decrypt encrypted data from Fortnite.

        Parameters
        ----------
        key_format: :class:`fortnite_api.KeyFormat`
            The format to return the key in. Defaults to :attr:`fortnite_api.KeyFormat.HEX`.

        Returns
        -------
        :class:`fortnite_api.Aes`
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
        language: Optional[:class:`fortnite_api.GameLanguage`]
            The language to display the banners in. Defaults to ``None``.
            This will override the default language set on the client.

        Returns
        -------
        List[:class:`fortnite_api.Banner`]
            The fetched banners.
        """
        data = await self.http.get_banners(language=self._resolve_language_value(language))
        return TransformerListProxy(
            data,
            lambda x: Banner(data=x, http=self.http),
        )

    async def fetch_banner_colors(self) -> List[BannerColor]:
        """|coro|

        Fetch all banner colors available in Fortnite.

        Returns
        -------
        List[:class:`fortnite_api.BannerColor`]
            The fetched banner colors.
        """
        data = await self.http.get_banner_colors()
        return TransformerListProxy(
            data,
            lambda x: BannerColor(data=x),
        )

    # CREATOR CODES

    async def fetch_creator_code(self, /, *, name: str) -> CreatorCode:
        """|coro|

        Fetch information about a creator code in Fortnite from the creator code name.

        Parameters
        ----------
        name: :class:`str`
            The name of the creator code to fetch.

        Returns
        -------
        :class:`fortnite_api.CreatorCode`
            The fetched creator code.

        Raises
        ------
        NotFound
            A creator code with that name was not found.
        """
        data = await self.http.get_creator_code(name)
        return CreatorCode(data=data)

    # MAPS

    async def fetch_map(self, *, language: Optional[GameLanguage] = None) -> Map:
        """|coro|

        Fetches the current map of Fortnite.

        Parameters
        ----------
        language: Optional[:class:`fortnite_api.GameLanguage`]
            The language to display the map in. Defaults to ``None``.
            This will override the default language set on the client.

        Returns
        -------
        :class:`fortnite_api.Map`
            The fetched map.
        """
        data = await self.http.get_map(language=self._resolve_language_value(language))
        return Map(data=data, http=self.http)

    # NEWS

    async def fetch_news(self, *, language: Optional[GameLanguage] = None) -> News:
        """|coro|

        Fetch the news for Fortnite. This includes all news for all game modes.

        Parameters
        ----------
        language: Optional[:class:`fortnite_api.GameLanguage`]
            The language to display the news in. Defaults to ``None``.
            This will override the default language set on the client.

        Returns
        -------
        :class:`fortnite_api.News`
            The fetched news.
        """
        data = await self.http.get_news(language=self._resolve_language_value(language))
        return News(data=data, http=self.http)

    async def fetch_news_br(self, *, language: Optional[GameLanguage] = None) -> GameModeNews:
        """|coro|

        Fetches the current Battle Royale news.

        Parameters
        ----------
        language : Optional[:class:`fortnite_api.GameLanguage`]
            The language to display the news in. Defaults to ``None``.
            This will override the default language set on the client.

        Returns
        -------
        :class:`fortnite_api.GameModeNews`
            The Battle Royale news.
        """
        data = await self.http.get_news_br(language=self._resolve_language_value(language))
        return GameModeNews(data=data, http=self.http)

    async def fetch_news_stw(self, *, language: Optional[GameLanguage] = None) -> GameModeNews:
        """|coro|

        Fetches the current Save the World news.

        Parameters
        ----------
        language : Optional[:class:`fortnite_api.GameLanguage`]
            The language to display the news in. Defaults to ``None``.
            This will override the default language set on the client.

        Returns
        -------
        :class:`fortnite_api.GameModeNews`
            The Save the World news.
        """
        data = await self.http.get_news_stw(language=self._resolve_language_value(language))
        return GameModeNews(data=data, http=self.http)

    # PLAYLISTS

    async def fetch_playlists(self, /, *, language: Optional[GameLanguage] = None) -> List[Playlist]:
        """|coro|

        Fetches a list of current playlists available in Fortnite.

        Parameters
        ----------
        language: Optional[:class:`fortnite_api.GameLanguage`]
            The language to display the playlists in. Defaults to ``None``.
            This will override the default language set on the client.

        Returns
        -------
        List[:class:`fortnite_api.Playlist`]
            The fetched current playlists available in Fortnite.
        """
        data = await self.http.get_playlists(language=self._resolve_language_value(language))
        return TransformerListProxy(
            data,
            lambda x: Playlist(data=x, http=self.http),
        )

    async def fetch_playlist(self, id: str, /, *, language: Optional[GameLanguage] = None) -> Playlist:
        """|coro|

        Fetch a specific playlist by its ID.

        Parameters
        ----------
        id: :class:`str`
            The ID of the playlist to fetch.
        language: Optional[:class:`fortnite_api.GameLanguage`]
            The language to display the playlist in. Defaults to ``None``.
            This will override the default language set on the client.

        Returns
        -------
        :class:`fortnite_api.Playlist`
            The fetched playlist.

        Raises
        ------
        NotFound
            A playlist with that ID was not found.
        """
        data = await self.http.get_playlist(id, language=self._resolve_language_value(language))
        return Playlist(data=data, http=self.http)

    # PLAYER STATS

    async def fetch_br_stats(
        self,
        *,
        name: Optional[str] = None,
        account_id: Optional[str] = None,
        type: AccountType = AccountType.EPIC,
        time_window: TimeWindow = TimeWindow.LIFETIME,
        image: StatsImageType = StatsImageType.NONE,
    ) -> BrPlayerStats:
        """|coro|

        Fetch stats for a Fortnite player by their name.

        .. note::

            The ratelimit for this endpoint is max 3 requests per second, 180 per minute.

        Parameters
        ----------
        name: Optional[:class:`str`]
            The name of the player to fetch stats for. Cannot be used with ``account_id``.
        account_id: Optional[:class:`str`]
            The account ID of the player to fetch stats for. Cannot be used with ``name``.
        type: Optional[:class:`fortnite_api.AccountType`]
            The type of account to search statistics for. This parameter is only to narrow the search when
            fetching account stats by name. It will not do anything when fetching by ``account_id``.
            Defaults to :attr:`fortnite_api.AccountType.EPIC`.
        time_window: Optional[:class:`fortnite_api.TimeWindow`]
            The time window to search statistics for. Defaults to :attr:`fortnite_api.TimeWindow.LIFETIME`.
        image: Optional[:class:`fortnite_api.StatsImageType`]
            The type of image to display in the statistics. Defaults to :attr:`fortnite_api.StatsImageType.NONE`. If this
            is set to :attr:`fortnite_api.StatsImageType.NONE`, there will be no image in the response.

        Returns
        -------
        :class:`fortnite_api.BrPlayerStats`
            The fetched player statistics.

        Raises
        ------
        NotFound
            A player with that name was not found.
        ValueError
            You cannot pass both a ``name`` and an ``account_id`` to fetch stats at the
            same time, or, you must pass either a ``name`` or an ``account_id`` to fetch stats.
        RateLimitExceeded
            The rate limit for this endpoint has been exceeded.
        MissingAPIKey
            The client does not have an API key set to fetch player stats.
        """
        if self.http.token is None:
            raise MissingAPIKey("An API key is required to fetch player stats.")

        if name is not None and account_id is not None:
            raise ValueError("You cannot pass both a name and an ID to fetch stats.")

        if account_id is not None:
            data = await self.http.get_br_stats_by_id(
                account_id=account_id, time_window=time_window and time_window.value, image=image and image.value
            )
            return BrPlayerStats(data=data, http=self.http)

        if name is not None:
            data = await self.http.get_br_stats(
                name=name,
                account_type=type and type.value,
                time_window=time_window and time_window.value,
                image=image and image.value,
            )
            return BrPlayerStats(data=data, http=self.http)

        raise ValueError("You must pass either a name or an account_id to fetch stats.")

    # SHOP
    async def fetch_shop(self, /, *, language: Optional[GameLanguage] = None) -> Shop:
        """|coro|

        Fetches the current Fortnite item shop.

        Parameters
        ----------
        language: Optional[:class:`fortnite_api.GameLanguage`]
            The language to display the playlist in. Defaults to ``None``.
            This will override the default language set on the client.

        Returns
        -------
        :class:`fortnite_api.Shop`
            The fetched item shop.
        """
        data = await self.http.get_shop(language=self._resolve_language_value(language))
        return Shop(data=data, http=self.http)

    # BETA METHODS

    @beta_method
    async def beta_fetch_material_instances(self) -> List[MaterialInstance]:
        """|coro|

        Fetches all the material instances available in Fortnite.

        .. note::

            This is a beta method. This cannot be called unless :attr:`beta`
            is set to ``True`` in the client.

        .. warning::

            This is a beta method. At any time, the endpoint this method calls could be removed or
            changed, and this method could break. Always be prepared for this.

        Returns
        --------
        List[:class:`fortnite_api.MaterialInstance`]
            The fetched material instances.

        Raises
        ------
        BetaAccessNotEnabled
            The client does not have beta access enabled through :attr:`~beta`.
        BetaUnknownException
            An unknown error occurred while fetching the material instances. This could be due to
            an issue with the API or the client. Any unknown errors raised will be wrapped in this exception.
        """
        data = await self.http.beta_get_material_instances()

        return TransformerListProxy(
            data,
            lambda x: MaterialInstance(data=x, http=self.http),
        )


@_remove_coro_doc
class SyncFortniteAPI:
    """
    .. attributetable:: fortnite_api.SyncFortniteAPI

    Represents a Sync Fortnite API client. This is the main class used to interact with the Fortnite API.

    .. container:: operations

        .. describe:: with x:

            This class is a context manager. This means you can use it with the ``with`` statement.
            This will automatically open and close the HTTP session for you. If you don't use the ``with`` statement, you will have to manually close the session.

    Parameters
    ----------
    api_key: Optional[:class:`str`]
        The API key to use for the client. If not provided, some endpoints may not be available.
    default_language: :class:`fortnite_api.GameLanguage`
        The default language to display the data in. Defaults to :attr:`fortnite_api.GameLanguage.ENGLISH`.
    session: Optional[:class:`requests.Session`]
        The session to use for the HTTP requests. If not provided, a new session will be created for you and you must use the class as an async context manager.
    beta: :class:`bool`
        Whether or not the client can make requests to the beta API. Any beta endpoints will not be available if this is set to ``False``. Defaults to ``False``.

        .. note::

            All beta endpoints are prefixed with ``beta_``.
    optimization_flags: Optional[:class:`fortnite_api.OptimizationFlags`]
        Any optimization flags to use for the client. Enabling these can speed up the client or reduce
        the amount of bandwidth used. Defaults to :meth:`fortnite_api.OptimizationFlags.default`. Pass ``None`` or :meth:`fortnite_api.OptimizationFlags.none` to remove all flags. Read the documentation for :class:`fortnite_api.OptimizationFlags` for more information.

    Attributes
    ----------
    default_language: Optional[:class:`fortnite_api.GameLanguage`]
        The default language, if any, passed to the client.
    beta: :class:`bool`
        Denotes if the client can make requests to beta endpoints.
    optimization_flags: Optional[:class:`fortnite_api.OptimizationFlags`]
        Any optimization flags set on the client.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        default_language: GameLanguage = GameLanguage.ENGLISH,
        session: Optional[requests.Session] = None,
        beta: bool = False,
        optimization_flags: OptimizationFlags = OptimizationFlags.default(),
    ) -> None:
        self.http: SyncHTTPClient = SyncHTTPClient(session=session, token=api_key, optimization_flags=optimization_flags)
        self.default_language: Optional[GameLanguage] = default_language
        self.beta: bool = beta

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
    @copy_doc(FortniteAPI.fetch_cosmetics_cars)
    def fetch_cosmetics_cars(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticCar[SyncHTTPClient]]:
        data = self.http.get_cosmetics_cars(language=self._resolve_language_value(language))
        return TransformerListProxy(
            data,
            lambda x: CosmeticCar(data=x, http=self.http),
        )

    @copy_doc(FortniteAPI.fetch_cosmetics_instruments)
    def fetch_cosmetics_instruments(
        self, *, language: Optional[GameLanguage] = None
    ) -> List[CosmeticInstrument[SyncHTTPClient]]:
        data = self.http.get_cosmetics_instruments(language=self._resolve_language_value(language))
        return TransformerListProxy(
            data,
            lambda x: CosmeticInstrument(data=x, http=self.http),
        )

    @copy_doc(FortniteAPI.fetch_cosmetics_lego_kits)
    def fetch_cosmetics_lego_kits(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticLegoKit[SyncHTTPClient]]:
        data = self.http.get_cosmetics_lego_kits(language=self._resolve_language_value(language))
        return TransformerListProxy(
            data,
            lambda x: CosmeticLegoKit(data=x, http=self.http),
        )

    @copy_doc(FortniteAPI.fetch_cosmetics_tracks)
    def fetch_cosmetics_tracks(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticTrack[SyncHTTPClient]]:
        data = self.http.get_cosmetics_tracks(language=self._resolve_language_value(language))
        return TransformerListProxy(
            data,
            lambda x: CosmeticTrack(data=x, http=self.http),
        )

    @copy_doc(FortniteAPI.fetch_cosmetics_br)
    def fetch_cosmetics_br(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticBr[SyncHTTPClient]]:
        data = self.http.get_cosmetics_br(language=self._resolve_language_value(language))
        return TransformerListProxy(
            data,
            lambda x: CosmeticBr(data=x, http=self.http),
        )

    @copy_doc(FortniteAPI.fetch_cosmetic_br)
    def fetch_cosmetic_br(
        self, /, cosmetic_id: str, *, language: Optional[GameLanguage] = None
    ) -> CosmeticBr[SyncHTTPClient]:
        data = self.http.get_cosmetic_br(cosmetic_id, language=self._resolve_language_value(language))
        return CosmeticBr(data=data, http=self.http)

    @copy_doc(FortniteAPI.fetch_cosmetics_lego)
    def fetch_cosmetics_lego(self, *, language: Optional[GameLanguage] = None) -> List[CosmeticLego[SyncHTTPClient]]:
        data = self.http.get_cosmetics_lego(language=self._resolve_language_value(language))
        return TransformerListProxy(
            data,
            lambda x: CosmeticLego(data=x, http=self.http),
        )

    @copy_doc(FortniteAPI.fetch_cosmetics_all)
    def fetch_cosmetics_all(self, *, language: Optional[GameLanguage] = None) -> CosmeticsAll[SyncHTTPClient]:
        data = self.http.get_cosmetics_all(language=self._resolve_language_value(language))
        return CosmeticsAll(data=data, http=self.http)

    # NEW COSMETICS

    @copy_doc(FortniteAPI.fetch_cosmetics_br_new)
    def fetch_cosmetics_br_new(self) -> NewBrCosmetics[SyncHTTPClient]:
        data = self.http.get_cosmetics_br_new()
        return NewBrCosmetics(data=data, http=self.http)

    @copy_doc(FortniteAPI.fetch_cosmetics_new)
    def fetch_cosmetics_new(self) -> NewCosmetics[SyncHTTPClient]:
        data = self.http.get_cosmetics_new()
        return NewCosmetics(data=data, http=self.http)

    @overload
    def search_br_cosmetics(
        self,
        *,
        multiple: Literal[True],
        language: GameLanguage = GameLanguage.ENGLISH,
        search_language: GameLanguage = GameLanguage.ENGLISH,
        match_method: Literal['full', 'contains', 'starts', 'ends'] = 'full',
        id: Optional[str] = ...,
        name: Optional[str] = ...,
        description: Optional[str] = ...,
        type: Optional[CosmeticBrType] = ...,
        type_display: Optional[str] = ...,
        type_backend: Optional[str] = ...,
        rarity: Optional[CosmeticBrRarity] = ...,
        rarity_display: Optional[str] = ...,
        rarity_backend: Optional[str] = ...,
        has_series: Optional[bool] = ...,
        series: Optional[str] = ...,
        series_backend: Optional[str] = ...,
        has_set: Optional[bool] = ...,
        set: Optional[str] = ...,
        set_text: Optional[str] = ...,
        set_backend: Optional[str] = ...,
        has_introduction: Optional[bool] = ...,
        introduction_backend: Optional[str] = ...,
        introduction_chapter: Optional[str] = ...,
        introduction_season: Optional[str] = ...,
        has_featured_image: Optional[bool] = ...,
        has_variants: Optional[bool] = ...,
        gameplay_tag: Optional[str] = ...,
        has_meta_tags: Optional[bool] = ...,
        has_dynamic_pak_id: Optional[bool] = ...,
        dynamic_pak_id: Optional[str] = ...,
        added: Optional[datetime.datetime] = ...,
        added_since: Optional[datetime.datetime] = ...,
        unseen_for: Optional[int] = ...,
        last_appearance: Optional[datetime.datetime] = ...,
    ) -> List[CosmeticBr[SyncHTTPClient]]: ...

    @overload
    def search_br_cosmetics(
        self,
        *,
        multiple: Literal[False],
        language: GameLanguage = GameLanguage.ENGLISH,
        search_language: GameLanguage = GameLanguage.ENGLISH,
        match_method: Literal['full', 'contains', 'starts', 'ends'] = 'full',
        id: Optional[str] = ...,
        name: Optional[str] = ...,
        description: Optional[str] = ...,
        type: Optional[CosmeticBrType] = ...,
        type_display: Optional[str] = ...,
        type_backend: Optional[str] = ...,
        rarity: Optional[CosmeticBrRarity] = ...,
        rarity_display: Optional[str] = ...,
        rarity_backend: Optional[str] = ...,
        has_series: Optional[bool] = ...,
        series: Optional[str] = ...,
        series_backend: Optional[str] = ...,
        has_set: Optional[bool] = ...,
        set: Optional[str] = ...,
        set_text: Optional[str] = ...,
        set_backend: Optional[str] = ...,
        has_introduction: Optional[bool] = ...,
        introduction_backend: Optional[str] = ...,
        introduction_chapter: Optional[str] = ...,
        introduction_season: Optional[str] = ...,
        has_featured_image: Optional[bool] = ...,
        has_variants: Optional[bool] = ...,
        gameplay_tag: Optional[str] = ...,
        has_meta_tags: Optional[bool] = ...,
        has_dynamic_pak_id: Optional[bool] = ...,
        dynamic_pak_id: Optional[str] = ...,
        added: Optional[datetime.datetime] = ...,
        added_since: Optional[datetime.datetime] = ...,
        unseen_for: Optional[int] = ...,
        last_appearance: Optional[datetime.datetime] = ...,
    ) -> CosmeticBr[SyncHTTPClient]: ...

    @copy_doc(FortniteAPI.search_br_cosmetics)
    def search_br_cosmetics(self, **kwargs: Any) -> Union[CosmeticBr[SyncHTTPClient], List[CosmeticBr[SyncHTTPClient]]]:
        multiple = kwargs.pop('multiple')

        kwargs['language'] = self._resolve_language_value(kwargs.get('language'))
        kwargs['search_language'] = self._resolve_language_value(kwargs.get('search_language'))

        payload = _transform_dict_for_get_request(kwargs)
        if multiple is True:
            data = self.http.search_cosmetic_all(**payload)
            return TransformerListProxy(
                data,
                lambda x: CosmeticBr(data=x, http=self.http),
            )
        else:
            data = self.http.search_cosmetic(**payload)
            return CosmeticBr(data=data, http=self.http)

    # AES

    @copy_doc(FortniteAPI.fetch_aes)
    def fetch_aes(self, *, key_format: KeyFormat = KeyFormat.HEX) -> Aes:
        data = self.http.get_aes(key_format.value)
        return Aes(data=data)

    # BANNERS
    @copy_doc(FortniteAPI.fetch_banners)
    def fetch_banners(self, *, language: Optional[GameLanguage] = None) -> List[Banner[SyncHTTPClient]]:
        data = self.http.get_banners(language=self._resolve_language_value(language))
        return TransformerListProxy(
            data,
            lambda x: Banner(data=x, http=self.http),
        )

    @copy_doc(FortniteAPI.fetch_banner_colors)
    def fetch_banner_colors(self) -> List[BannerColor]:
        data = self.http.get_banner_colors()
        return TransformerListProxy(
            data,
            lambda x: BannerColor(data=x),
        )

    # CREATOR CODES

    @copy_doc(FortniteAPI.fetch_creator_code)
    def fetch_creator_code(self, /, *, name: str) -> CreatorCode:
        data = self.http.get_creator_code(name)
        return CreatorCode(data=data)

    # MAPS

    @copy_doc(FortniteAPI.fetch_map)
    def fetch_map(self, *, language: Optional[GameLanguage] = None) -> Map[SyncHTTPClient]:
        data = self.http.get_map(language=self._resolve_language_value(language))
        return Map(data=data, http=self.http)

    # NEWS

    @copy_doc(FortniteAPI.fetch_news)
    def fetch_news(self, *, language: Optional[GameLanguage] = None) -> News[SyncHTTPClient]:
        data = self.http.get_news(language=self._resolve_language_value(language))
        return News(data=data, http=self.http)

    @copy_doc(FortniteAPI.fetch_news_br)
    def fetch_news_br(self, *, language: Optional[GameLanguage] = None) -> GameModeNews[SyncHTTPClient]:
        data = self.http.get_news_br(language=self._resolve_language_value(language))
        return GameModeNews(data=data, http=self.http)

    @copy_doc(FortniteAPI.fetch_news_stw)
    def fetch_news_stw(self, *, language: Optional[GameLanguage] = None) -> GameModeNews[SyncHTTPClient]:
        data = self.http.get_news_stw(language=self._resolve_language_value(language))
        return GameModeNews(data=data, http=self.http)

    # PLAYLISTS

    @copy_doc(FortniteAPI.fetch_playlists)
    def fetch_playlists(self, /, *, language: Optional[GameLanguage] = None) -> List[Playlist[SyncHTTPClient]]:
        data = self.http.get_playlists(language=self._resolve_language_value(language))
        return TransformerListProxy(
            data,
            lambda x: Playlist(data=x, http=self.http),
        )

    @copy_doc(FortniteAPI.fetch_playlist)
    def fetch_playlist(self, id: str, /, *, language: Optional[GameLanguage] = None) -> Playlist[SyncHTTPClient]:
        data = self.http.get_playlist(id, language=self._resolve_language_value(language))
        return Playlist(data=data, http=self.http)

    # PLAYER STATS

    @copy_doc(FortniteAPI.fetch_br_stats)
    def fetch_br_stats(
        self,
        *,
        name: Optional[str] = None,
        account_id: Optional[str] = None,
        type: AccountType = AccountType.EPIC,
        time_window: TimeWindow = TimeWindow.LIFETIME,
        image: StatsImageType = StatsImageType.NONE,
    ) -> BrPlayerStats[SyncHTTPClient]:
        if name is not None and account_id is not None:
            raise ValueError("You cannot pass both a name and an ID to fetch stats.")

        if account_id is not None:
            data = self.http.get_br_stats_by_id(
                account_id=account_id, time_window=time_window and time_window.value, image=image and image.value
            )
            return BrPlayerStats(data=data, http=self.http)

        if name is not None:
            data = self.http.get_br_stats(
                name=name,
                account_type=type and type.value,
                time_window=time_window and time_window.value,
                image=image and image.value,
            )
            return BrPlayerStats(data=data, http=self.http)

        raise ValueError("You must pass either a name or an account_id to fetch stats.")

    @copy_doc(FortniteAPI.beta_fetch_material_instances)
    @beta_method
    def beta_fetch_material_instances(self) -> List[MaterialInstance[SyncHTTPClient]]:
        data = self.http.beta_get_material_instances()

        return TransformerListProxy(
            data,
            lambda x: MaterialInstance(data=x, http=self.http),
        )

    @copy_doc(FortniteAPI.fetch_shop)
    def fetch_shop(self, /, *, language: Optional[GameLanguage] = None) -> Shop[SyncHTTPClient]:
        data = self.http.get_shop(language=self._resolve_language_value(language))
        return Shop(data=data, http=self.http)
