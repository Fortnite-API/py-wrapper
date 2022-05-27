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
import time
import sys
import aiohttp
import asyncio
import requests
from typing import Any, Dict, List, Literal, Optional, Union, TypeVar, TYPE_CHECKING

from . import __version__
from .utils import to_json
from .errors import *

if TYPE_CHECKING:
    from .types import (
        aes
    )

T = TypeVar('T', bound='Any')

# Similar to how dpy manages routes, we'll follow this pattern as well
class Route:

    BASE_URL = 'https://fortnite-api.com/'

    def __init__(self, method: str, endpoint: str, **params: Any) -> None:
        self.method: str = method
        self.endpoint: str = endpoint
        self.params: Optional[Dict[str, Any]] = params

        url = self.BASE_URL + endpoint
        if params is not None:
            url = url.format(params)

        self.url: str = url


class BaseHTTPClient(abc.ABC):
    def __init__(
        self,
        *,
        token: Optional[str] = None,
        run_async: bool = False,
    ) -> None:
        self.run_async: bool = run_async

        self.headers: Dict[str, Any] = {'User-Agent': self.user_agent}
        
        self.token: Optional[str] = token
        if self.token is not None:
            self.headers['Authorization'] = self.token
            
        self.user_agent = 'FortniteApi (https://github.com/Fortnite-API/py-wrapper {}) Python/{1[0]}.{1[1]}'.format(
            __version__, sys.version_info
        )
    
    @abc.abstractmethod
    def request(self, route: Route, **kwargs: Any) -> Any:
        ...

    def get_aes(self, key_format: str) -> aes.Aes:  # Note: replace with typed dict's when they're done
        r: Route = Route('GET', '/v2/aes')
        params: Dict[str, str] = {'keyFormat': key_format}
        return self.request(r, params=params)

    def get_banners(self, language: Optional[str] = None) -> List[Dict[Any, Any]]: 
        r: Route = Route('GET', '/v1/banners')
        params: Dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_banner_colors(self) -> List[Dict[Any, Any]]:
        r: Route = Route('GET', '/v1/banners/colors')
        return self.request(r) 

    def get_cosmetics(self, language: Optional[str] = None) -> List[Dict[Any, Any]]:
        r: Route = Route('GET', '/v2/cosmetics/br')
        params: Dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_new_cosmetics(self, language: Optional[str] = None) -> List[Dict[Any, Any]]:
        r: Route = Route('GET', '/v2/cosmetics/br/new')
        params: Dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_cosmetic(self, id: str, language: Optional[str] = None) -> Dict[Any, Any]:
        r: Route = Route('GET', '/v2/cosmetics/br/{id}', id=id)
        params: Dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)
 
    # kwargs will be expanded upon in client so its understood what you can and cant pass
    def search_cosmetic(self, **kwargs: Any) -> Dict[Any, Any]:
        r: Route = Route('GET', '/v2/cosmetics/br/search')
        return self.request(r, params=kwargs)
    
    def search_cosmetic_all(self, **kwargs: Any) -> List[Dict[Any, Any]]:
        r: Route = Route('GET', '/v2/cosmetics/br/search/all')
        return self.request(r, params=kwargs)

    def get_creator_code(self, name: str) -> Dict[Any, Any]:
        r: Route = Route('GET', '/v2/creatorcode', name=name)
        params: Dict[str, str] = {'name': name}
        return self.request(r, params=params)

    def get_map(self, language: Optional[str] = None) -> Dict[Any, Any]:
        r: Route = Route('GET', '/v1/map')
        params: Dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_news(self, language: Optional[str] = None) -> Dict[Any, Any]:
        r: Route = Route('GET', '/v2/news')
        params: Dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_br_news(self, language: Optional[str] = None) -> Dict[Any, Any]:
        r: Route = Route('GET', '/v2/news/br')
        params: Dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_stw_news(self, language: Optional[str] = None) -> Dict[Any, Any]:
        r: Route = Route('GET', '/v2/news/stw')
        params: Dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_creative_news(self, language: Optional[str] = None) -> Dict[Any, Any]:
        r: Route = Route('GET', '/v2/news/creative')
        params: Dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_playlists(self, language: Optional[str] = None) -> List[Dict[Any, Any]]:
        r: Route = Route('GET', '/v1/playlists')
        params: Dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_playlist(self, id: str, language: Optional[str] = None) -> Dict[Any, Any]:
        r: Route = Route('GET', '/v1/playlists/{id}', id=id)
        params: Dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_br_shop(self, language: Optional[str] = None) -> Dict[Any, Any]:
        r: Route = Route('GET', '/v2/shop/br')
        params: Dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_br_shop_combined(self, language: Optional[str] = None) -> Dict[Any, Any]:
        r: Route = Route('GET', '/v2/shop/br/combined')
        params: Dict[str, str] = {}

        if language:
            params['language'] = language

        return self.request(r, params=params)

    def get_br_stats(
        self,
        name: str,
        account_type: Optional[Literal['epic', 'psn', 'xbl']] = None,
        time_window: Optional[Literal['season', 'lifetime']] = None,
        image: Optional[Literal['all', 'keyboardMouse', 'gamepad', 'touch']] = None,
    ) -> Dict[Any, Any]:
        r: Route = Route('GET', '/v2/stats/br/v2', name=name)
        params: Dict[str, str] = {'name': name}

        if account_type:
            params['account_type'] = account_type

        if time_window:
            params['time_window'] = time_window

        if image:
            params['image'] = image

        return self.request(r, params=params)
    
    def get_br_stats_by_id(
        self,
        account_id: str,
        time_window: Optional[Literal['season', 'lifetime']] = None,
        image: Optional[Literal['all', 'keyboardMouse', 'gamepad', 'touch']] = None,
    ) -> Dict[Any, Any]:
        r: Route = Route('GET', '/v2/stats/br/v2/{account_id}', account_id=account_id)
        params: Dict[str, str] = {}

        if time_window:
            params['time_window'] = time_window

        if image:
            params['image'] = image

        return self.request(r, params=params) 


class AsyncHTTPClient(BaseHTTPClient):
    
    def __init__(self, *args: Any, session: Optional[aiohttp.ClientSession] = None, **kwargs: Any) -> None:
        self.session: Optional[aiohttp.ClientSession] = session
        self._http_lock: asyncio.Lock = asyncio.Lock()
        super().__init__(*args, **kwargs)
    
    async def _parse_async_response(self, response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str, bytes]:
        try:
            text = await response.text()
        except UnicodeDecodeError:
            return await response.read()

        if response.headers['Content-Type'].startswith('application/json'):
            return to_json(text)

        return text

    async def request(self, route: Route, **kwargs: Any) -> Any:
        if self.session is None:
            self.session = aiohttp.ClientSession()

        response: Optional[aiohttp.ClientResponse] = None
        async with self._http_lock:
            for tries in range(5):  # Just in case we get rate limited

                async with self.session.request(route.method, route.url, headers=self.headers, **kwargs) as response:
                    data = await self._parse_async_response(response)

                    if 300 > response.status >= 200:  # Everything is ok
                        if isinstance(data, dict):
                            return data.get('data', data)

                        return data

                    # Let's try and find an error message
                    error: str = 'Error message not provided!'
                    if isinstance(data, dict):
                        error = data.get('data', data).get('error', error)

                    if response.status == 401:
                        raise Unauthorized(error)

                    if response.status == 403:
                        raise Forbidden(error)

                    if response.status == 404:
                        raise NotFound(error)

                    if response.status == 429:  # NOTE: Handle this better down the road
                        raise RateLimited(error)

                    if response.status in {500, 502, 504}:
                        await asyncio.sleep(1 + tries * 2)
                        continue

                    if response.status > 500:
                        raise ServiceUnavailable(error)

        if response is not None:
            raise ServiceUnavailable('Service unavailable')

        raise RuntimeError('Unreachable code reached!')


class HTTPClient(BaseHTTPClient):
    
    def __init__(self, *args: Any, session: Optional[requests.Session] = None, **kwargs: Any) -> None:
        self.session: requests.Session = session or requests.Session()
        super().__init__(*args, **kwargs)
    
    def request(self, route: Route, **kwargs: Any) -> Any:
        response: Optional[requests.Response] = None
        for tries in range(5):
            with self.session.request(route.method, route.url, headers=self.headers, **kwargs) as response:
                # We arent able to parse the same as we are in async mode, so we'll need
                # to use some other logic here
                if response.headers['Content-Type'].startswith('application/json'):
                    data = to_json(response.text)
                else:
                    try:
                        data = response.text
                    except Exception:
                        data = response.content

            if 300 > response.status_code >= 200:  # Everything is ok
                if isinstance(data, dict):
                    return data.get('data', data)

                return data

            # Let's try and find an error message
            error: str = 'Error message not provided!'
            if isinstance(data, dict):
                error = data.get('error', error)

            if response.status_code == 401:
                raise Unauthorized(error)

            if response.status_code == 403:
                raise Forbidden(error)

            if response.status_code == 404:
                raise NotFound(error)

            if response.status_code == 429:  # NOTE: Handle this better down the road
                raise RateLimited(error)

            if response.status_code in {500, 502, 504}:
                time.sleep(1 + tries * 2)
                continue

            if response.status_code > 500:
                raise ServiceUnavailable(error)

        if response is not None:
            raise ServiceUnavailable('Service unavailable')

        raise RuntimeError('Unreachable code reached!')
