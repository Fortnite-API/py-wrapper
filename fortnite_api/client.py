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

from typing import TYPE_CHECKING, Generic, Optional, TypeVar
from typing_extensions import ParamSpec

from .enums import *
from .aes import Aes
from .http import HTTPClient, AsyncHTTPClient

if TYPE_CHECKING:
    import aiohttp
    import requests

T = TypeVar('T')
TC = TypeVar('TC')
P = ParamSpec('P')
HttpT = TypeVar('HttpT', HTTPClient, AsyncHTTPClient)


class FortniteAPI(Generic[HttpT]):
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

    def __init__(
        self, 
        api_key: Optional[str] = None,
        *,
        session: Optional[requests.Session] = None
    ) -> None:
        self.http: HTTPClient = HTTPClient(
            session=session,
            token=api_key
        ) 

    def fetch_aes(self, key_format: KeyFormat = KeyFormat.HEX) -> Aes:
        data = self.http.get_aes(key_format.value)
        return Aes(data=data) 
    
    
class AsyncFortniteAPI:
    def __init__(
        self, 
        api_key: Optional[str] = None,
        *,
        session: Optional[aiohttp.ClientSession] = None
    ) -> None:
        self.http: AsyncHTTPClient = AsyncHTTPClient(
            session=session,
            token=api_key
        )
        
    async def fetch_aes(self, key_format: KeyFormat = KeyFormat.HEX) -> Aes:
        data = await self.http.get_aes(key_format.value) 
        return Aes(data=data)