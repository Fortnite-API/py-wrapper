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

import inspect
from typing import TYPE_CHECKING, Generic, Optional, Union, Type, Awaitable, TypeVar, Any, overload, Coroutine
from typing_extensions import ParamSpec

from .endpoints import *
from .enums import *
from .aes import AES
from .http import HTTPClient, AsyncHTTPClient, BaseHTTPClient

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
        run_async: bool = False,
        session: Optional[Union[requests.Session, aiohttp.ClientSession]] = None
    ) -> None:
        self.http: BaseHTTPClient[Any] = BaseHTTPClient(
            session=session,
            token=api_key,
            run_async=run_async
        )
        
    async def _wrap_async_method(self, result: Awaitable[Any], object_cls: Type[T]) -> T:
        data = await result
        return object_cls(data=data)
        
    @overload
    def fetch_aes(self: FortniteAPI[HTTPClient], key_format: KeyFormat) -> AES:
        ...
    
    @overload
    def fetch_aes(self: FortniteAPI[AsyncHTTPClient], key_format: KeyFormat) -> Coroutine[Any, Any, AES]:
        ...
        
    def fetch_aes(self, key_format: KeyFormat) -> Union[Coroutine[Any, Any, AES], AES]:
        data = self.http.get_aes(key_format.value)
        if inspect.isawaitable(data):
            return self._wrap_async_method(data, AES)

        return AES(data=data) # type: ignore