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
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Generic, TypeVar

import pytest
import requests
from typing_extensions import Concatenate, ParamSpec, TypeAlias, TypeIs

import fortnite_api
from fortnite_api import ReconstructAble

P = ParamSpec('P')
T = TypeVar('T')

if TYPE_CHECKING:
    Client: TypeAlias = fortnite_api.Client
    SyncClient = fortnite_api.SyncClient

    CoroFunc = Callable[P, Coroutine[Any, Any, T]]


class HybridMethodProxy(Generic[P, T]):
    def __init__(
        self,
        hybrid_client: ClientHybrid,
        sync_client: SyncClient,
        async_method: CoroFunc[Concatenate[Client, P], T],
        sync_method: Callable[Concatenate[SyncClient, P], T],
    ) -> None:
        self.__hybrid_client = hybrid_client
        self.__sync_client = sync_client

        self.__async_method = async_method
        self.__sync_method = sync_method

    def _validate_results(self, async_res: T, sync_res: T) -> None:
        assert type(async_res) is type(sync_res), f"Expected {type(async_res)}, got {type(sync_res)}"

        if isinstance(async_res, fortnite_api.Hashable):
            assert isinstance(sync_res, fortnite_api.Hashable)
            assert async_res == sync_res

        if isinstance(async_res, fortnite_api.ReconstructAble):
            assert isinstance(sync_res, fortnite_api.ReconstructAble)

            sync_res_narrowed: ReconstructAble[Any, fortnite_api.SyncHTTPClient] = sync_res
            async_res_narrowed: ReconstructAble[Any, fortnite_api.HTTPClient] = async_res

            async_raw_data = sync_res_narrowed.to_dict()
            sync_raw_data = sync_res_narrowed.to_dict()
            assert async_raw_data == sync_raw_data

            async_reconstructed = type(async_res_narrowed).from_dict(async_raw_data, client=self.__hybrid_client)
            sync_reconstructed = type(sync_res_narrowed).from_dict(sync_raw_data, client=self.__sync_client)

            assert isinstance(async_reconstructed, type(sync_reconstructed))

    async def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        # Call the sync method first
        sync_result = self.__sync_method(self.__sync_client, *args, **kwargs)

        # Call the async method
        async_result = await self.__async_method(self.__hybrid_client, *args, **kwargs)

        self._validate_results(async_result, sync_result)
        return async_result


class ClientHybrid(fortnite_api.Client):
    """Denotes a "client-hybrid" that calls both a async and sync
    client when a method is called.

    Pytest tests are not called in parallel, so although this is a
    blocking operation it will not affect the overall performance of
    the tests.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        kwargs.pop('session', None)
        session = requests.Session()
        self.__sync_client: fortnite_api.SyncClient = fortnite_api.SyncClient(*args, session=session, **kwargs)

    async def __aexit__(self, *args: Any) -> None:
        # We need to ensure that the sync client is also closed
        self.__sync_client.__exit__(*args)
        return await super().__aexit__(*args)

    @staticmethod
    def __is_coroutine_function(item: Any) -> TypeIs[Callable[..., Coroutine[Any, Any, Any]]]:
        return inspect.iscoroutinefunction(item)

    @staticmethod
    def __is_function(item: Any) -> TypeIs[Callable[..., Any]]:
        return inspect.isfunction(item)

    def __getattribute__(self, name: str) -> Any:
        item = super().__getattribute__(name)

        if not self.__is_coroutine_function(item):
            # Internal function of some sort, want to ignore in case.
            return item

        sync_item = getattr(self.__sync_client, name)
        if not self.__is_function(sync_item):
            # The sync client has a similar name, but it's not a function.
            # This is likely a property or something else that we don't want to
            # call.
            return item

        return HybridMethodProxy(self, self.__sync_client, item, sync_item)


@pytest.mark.asyncio
async def test_hybrid_client():
    async with ClientHybrid() as client:
        data = await client.fetch_aes()
        print(data)
