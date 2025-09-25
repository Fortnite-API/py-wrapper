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

import abc
import asyncio
import logging
import sys
import time
from collections.abc import Coroutine
from typing import Any, ClassVar, Literal, Optional, Union
from urllib.parse import quote as _uriquote

import aiohttp
import requests
from typing_extensions import TypeAlias, TypeVar

from . import __version__
from .errors import *
from .utils import now, parse_time, to_json

T = TypeVar('T', bound='Any')
AsyncResponse: TypeAlias = Coroutine[Any, Any, T]

HTTPClientT = TypeVar('HTTPClientT', bound='Union[HTTPClient, SyncHTTPClient]', default='HTTPClient')

_log = logging.getLogger(__name__)


class Route:
    """Represents a route to a specific endpoint. This is an internally created structure, and is exposed to the user for
    advanced handling of ratelimits and listening to requests a client makes.

    Attributes
    ----------
    method: :class:`str`
        The HTTP method to use when making the request.
    path: :class:`str`
        The path to the endpoint.
    params: :class:`dict`
        The path parameters given to the endpoint.
    url: :class:`str`
        The formatted URL that is used to make the request.
    """

    # General scheme for this used from https://github.com/Rapptz/discord.py/blob/master/discord/http.py#L292-L327
    # The idea is that, to simplify request logic, a Route can be passed to a request method, and it will handle all the
    # params and URL formatting for you.

    BASE_URL: ClassVar[str] = 'https://fortnite-api.com'

    def __init__(self, method: str, path: str, **params: Any) -> None:
        self.method: str = method
        self.path: str = path
        self.params: Optional[dict[str, Any]] = params

        url = self.BASE_URL + path
        if params:
            url = url.format_map({k: _uriquote(v) if isinstance(v, str) else v for k, v in params.items()})

        self.url: str = url

    @property
    def key(self) -> str:
        """:class:`str`: The key for the route. This is a unique identifier for the route used for ratelimit management."""
        return f'{self.method}:{self.path}'


class HTTPMixin(abc.ABC):
    def __init__(self, *, token: Optional[str] = None) -> None:
        self.token: Optional[str] = token

        self.user_agent = 'FortniteApi (https://github.com/Fortnite-API/py-wrapper {0}) Python/{1[0]}.{1[1]}'.format(  # noqa: UP032
            __version__, sys.version_info
        )

        self.headers: dict[str, Any] = {'User-Agent': self.user_agent}
        if self.token is not None:
            self.headers['Authorization'] = self.token

    @abc.abstractmethod
    def request(self, route: Route, **kwargs: Any) -> Any: ...

    def get_cosmetics_br(self, language: Optional[str] = None, response_flags: Optional[int] = None):
        r: Route = Route('GET', '/v2/cosmetics/br')
        params: dict[str, Union[str, int]] = {}

        if language:
            params['language'] = language

        if response_flags:
            params['responseFlags'] = response_flags

        return self.request(r, params=params)

    def get_cosmetics_cars(self, language: Optional[str] = None, response_flags: Optional[int] = None):
        r: Route = Route('GET', '/v2/cosmetics/cars')
        params: dict[str, Union[str, int]] = {}

        if language:
            params['language'] = language

        if response_flags:
            params['responseFlags'] = response_flags

        return self.request(r, params=params)

    def get_cosmetics_instruments(self, language: Optional[str] = None, response_flags: Optional[int] = None):
        r: Route = Route('GET', '/v2/cosmetics/instruments')
        params: dict[str, Union[str, int]] = {}

        if language:
            params['language'] = language

        if response_flags:
            params['responseFlags'] = response_flags

        return self.request(r, params=params)

    def get_cosmetics_lego_kits(self, language: Optional[str] = None, response_flags: Optional[int] = None):
        r: Route = Route('GET', '/v2/cosmetics/lego/kits')
        params: dict[str, Union[str, int]] = {}

        if language:
            params['language'] = language

        if response_flags:
            params['responseFlags'] = response_flags

        return self.request(r, params=params)

    def get_cosmetics_tracks(self, language: Optional[str] = None, response_flags: Optional[int] = None):
        r: Route = Route('GET', '/v2/cosmetics/tracks')
        params: dict[str, Union[str, int]] = {}

        if language:
            params['language'] = language

        if response_flags:
            params['responseFlags'] = response_flags

        return self.request(r, params=params)

    def get_cosmetics_lego(self, language: Optional[str] = None, response_flags: Optional[int] = None):
        r: Route = Route('GET', '/v2/cosmetics/lego')
        params: dict[str, Union[str, int]] = {}

        if language:
            params['language'] = language

        if response_flags:
            params['responseFlags'] = response_flags

        return self.request(r, params=params)

    def get_cosmetics_beans(self, language: Optional[str] = None, response_flags: Optional[int] = None):
        r: Route = Route('GET', '/v2/cosmetics/beans')
        params: dict[str, Union[str, int]] = {}

        if language:
            params['language'] = language

        if response_flags:
            params['responseFlags'] = response_flags

        return self.request(r, params=params)

    def get_cosmetics_new(self, language: Optional[str] = None, response_flags: Optional[int] = None):
        r: Route = Route('GET', '/v2/cosmetics/new')
        params: dict[str, Union[str, int]] = {}

        if language:
            params['language'] = language

        if response_flags:
            params['responseFlags'] = response_flags

        return self.request(r, params=params)

    def get_cosmetic_br(self, id: str, language: Optional[str] = None, response_flags: Optional[int] = None):
        r: Route = Route('GET', '/v2/cosmetics/br/{id}', id=id)
        params: dict[str, Union[str, int]] = {}

        if language:
            params['language'] = language

        if response_flags:
            params['responseFlags'] = response_flags

        return self.request(r, params=params)

    def get_cosmetics_all(self, language: Optional[str] = None, response_flags: Optional[int] = None):
        r: Route = Route('GET', '/v2/cosmetics')
        params: dict[str, Union[str, int]] = {}

        if language:
            params['language'] = language

        if response_flags:
            params['responseFlags'] = response_flags

        return self.request(r, params=params)

    def get_aes(self, key_format: str):
        r: Route = Route('GET', '/v2/aes')
        params: dict[str, str] = {'keyFormat': key_format}
        return self.request(r, params=params)

    def get_banners(self, language: Optional[str] = None):
        r: Route = Route('GET', '/v1/banners')
        params: dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_banner_colors(self):
        r: Route = Route('GET', '/v1/banners/colors')
        return self.request(r)

    # kwargs will be expanded upon in client so its understood what you can and cant pass
    def search_cosmetic(self, **kwargs: Any):
        r: Route = Route('GET', '/v2/cosmetics/br/search')
        return self.request(r, params=kwargs)

    def search_cosmetic_all(self, **kwargs: Any):
        r: Route = Route('GET', '/v2/cosmetics/br/search/all')
        return self.request(r, params=kwargs)

    def get_creator_code(self, name: str):
        r: Route = Route('GET', '/v2/creatorcode', name=name)
        params: dict[str, str] = {'name': name}
        return self.request(r, params=params)

    def get_map(self, language: Optional[str] = None):
        r: Route = Route('GET', '/v1/map')
        params: dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_news(self, language: Optional[str] = None):
        r: Route = Route('GET', '/v2/news')
        params: dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_news_br(self, language: Optional[str] = None):
        r: Route = Route('GET', '/v2/news/br')
        params: dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_news_stw(self, language: Optional[str] = None):
        r: Route = Route('GET', '/v2/news/stw')
        params: dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_playlists(self, language: Optional[str] = None):
        r: Route = Route('GET', '/v1/playlists')
        params: dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_playlist(self, id: str, language: Optional[str] = None):
        r: Route = Route('GET', '/v1/playlists/{id}', id=id)
        params: dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_shop(self, language: Optional[str] = None, response_flags: Optional[int] = None):
        r: Route = Route('GET', '/v2/shop')
        params: dict[str, Union[str, int]] = {}

        if language:
            params['language'] = language

        if response_flags:
            params['responseFlags'] = response_flags

        return self.request(r, params=params)

    def get_br_stats(
        self,
        name: str,
        account_type: Literal['epic', 'psn', 'xbl'] = 'epic',
        time_window: Literal['season', 'lifetime'] = 'lifetime',
        image: Literal['all', 'keyboardMouse', 'gamepad', 'touch', 'none'] = 'none',
    ):
        r: Route = Route('GET', '/v2/stats/br/v2', name=name)
        params: dict[str, str] = {'name': name, 'accountType': account_type, 'timeWindow': time_window, 'image': image}

        return self.request(r, params=params)

    def get_br_stats_by_id(
        self,
        account_id: str,
        time_window: Literal['season', 'lifetime'] = 'lifetime',
        image: Literal['all', 'keyboardMouse', 'gamepad', 'touch', 'none'] = 'none',
    ):
        r: Route = Route('GET', '/v2/stats/br/v2/{account_id}', account_id=account_id)
        params: dict[str, str] = {'timeWindow': time_window, 'image': image}

        return self.request(r, params=params)

    def beta_get_new_display_assets(self):
        r: Route = Route('GET', '/beta/newdisplayassets')
        return self.request(r)

    def beta_get_material_instances(self):
        r: Route = Route('GET', '/beta/materialinstances')
        return self.request(r)


class HTTPClient(HTTPMixin):
    def __init__(self, *args: Any, session: Optional[aiohttp.ClientSession] = None, **kwargs: Any) -> None:
        self.session: Optional[aiohttp.ClientSession] = session
        super().__init__(*args, **kwargs)

    async def close(self) -> None:
        if self.session is not None:
            await self.session.close()

    async def _parse_async_response(self, response: aiohttp.ClientResponse) -> Union[dict[str, Any], str, bytes]:
        try:
            text = await response.text()
        except UnicodeDecodeError:
            return await response.read()

        content_type = response.headers.get('Content-Type')
        if content_type and content_type.startswith('application/json'):
            return to_json(text)

        return text

    async def request(self, route: Route, **kwargs: Any) -> Any:
        if self.session is None:
            raise RuntimeError(
                'aiohttp.ClientSession is not set. Must either pass session to Client constructor or use the async context manager.'
            )

        response: Optional[aiohttp.ClientResponse] = None
        data = None
        error = None

        for tries in range(5):
            async with self.session.request(route.method, route.url, headers=self.headers, **kwargs) as response:
                _log.debug('Request to %s %s returned status %s', route.method, route.url, response.status)
                data = await self._parse_async_response(response)

            if 300 > response.status >= 200:
                if isinstance(data, dict):
                    # Fortnite API wraps everything in a "data" key, so unwrap it if possible.
                    return data.get('data', data)

                return data

            # Let's try and find an error message
            error = 'Error message not provided!'
            if isinstance(data, dict):
                error = data.get('data', data).get('error', error)

            if response.status == 401:
                raise Unauthorized(error, response, data)

            if response.status == 403:
                raise Forbidden(error, response, data)

            if response.status == 404:
                raise NotFound(error, response, data)

            if response.status == 429:
                # The client has been rate limited
                # We're going to wait for the limit to be up and then retry
                reset = response.headers.get('X-Ratelimit-Reset')
                if reset is None:
                    raise RateLimited(error, response, data)

                then = parse_time(reset)
                wait_time = (then - now()).total_seconds()
                # If, for some reason, the time is negative, we'll continue
                if wait_time > 0:
                    await asyncio.sleep((then - now()).total_seconds())

                continue

            if response.status > 500:
                await asyncio.sleep(1 + tries * 2)
                continue

        if response is not None:
            # If we hit the limit 5 times, there are bigger issues.
            if response.status == 429:
                raise RateLimited(error, response, data)
            if response.status > 500:
                raise ServiceUnavailable(error, response, data)

            raise HTTPException(error, response, data)

        raise RuntimeError('Unreachable code reached!')


class SyncHTTPClient(HTTPMixin):
    def __init__(self, *args: Any, session: Optional[requests.Session] = None, **kwargs: Any) -> None:
        self.session: Optional[requests.Session] = session
        super().__init__(*args, **kwargs)

    def close(self) -> None:
        if self.session is not None:
            self.session.close()

    def _parse_sync_response(self, response: requests.Response) -> Union[dict[str, Any], str, bytes]:
        content_type = response.headers.get('Content-Type')
        if content_type and content_type.startswith('image/'):
            return response.content

        try:
            data = response.text
        except Exception:
            data = response.content

        if content_type and content_type.startswith('application/json'):
            return to_json(data)

        return data

    def request(self, route: Route, **kwargs: Any) -> Any:
        if self.session is None:
            raise RuntimeError(
                'requests.Session is not set. Must either pass session to Client constructor or use the context manager.'
            )

        response: Optional[requests.Response] = None
        data = None
        error = None
        for tries in range(5):
            with self.session.request(route.method, route.url, headers=self.headers, **kwargs) as response:
                _log.debug('Request to %s %s returned status %s', route.method, route.url, response.status_code)

                data = self._parse_sync_response(response)

            if 300 > response.status_code >= 200:  # Everything is ok
                if isinstance(data, dict):
                    return data.get('data', data)

                return data

            # Let's try and find an error message
            error = 'Error message not provided!'
            if isinstance(data, dict):
                error = data.get('error', error)

            if response.status_code == 401:
                raise Unauthorized(error, response, data)

            if response.status_code == 403:
                raise Forbidden(error, response, data)

            if response.status_code == 404:
                raise NotFound(error, response, data)

            if response.status_code == 429:
                # The client has been rate limited
                # We're going to wait for the limit to be up and then retry
                reset = response.headers.get('X-Ratelimit-Reset')
                if reset is None:
                    raise RateLimited(error, response, data)

                then = parse_time(reset)
                wait_time = (then - now()).total_seconds()

                # If, for some reason, the time is negative, we'll continue
                if wait_time > 0:
                    time.sleep((then - now()).total_seconds())

                continue

            if response.status_code > 500:
                time.sleep(1 + tries * 2)
                continue

        if response is not None:
            # If we hit the limit 5 times, there are bigger issues.
            if response.status_code == 429:
                raise RateLimited(error, response, data)
            if response.status_code > 500:
                raise ServiceUnavailable(error, response, data)

            raise HTTPException(error, response, data)

        raise RuntimeError('Unreachable code reached!')
