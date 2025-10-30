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
import logging
from collections.abc import Callable, Coroutine
from typing import TYPE_CHECKING, Any, Concatenate, Generic, TypeAlias, TypeVar, cast

import pytest
import requests
from typing_extensions import ParamSpec

import fortnite_api

P = ParamSpec('P')
T = TypeVar('T')

if TYPE_CHECKING:
    import fortnite_api.http

    Client: TypeAlias = fortnite_api.Client
    SyncClient = fortnite_api.SyncClient

    CoroFunc = Callable[P, Coroutine[Any, Any, T]]

log = logging.getLogger(__name__)


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

    @property
    def __name__(self) -> str:
        return self.__async_method.__name__

    def _validate_results(self, async_res: T, sync_res: T) -> None:
        assert type(async_res) is type(sync_res), f"Expected {type(async_res)}, got {type(sync_res)}"

        if isinstance(async_res, fortnite_api.Hashable):
            assert isinstance(sync_res, fortnite_api.Hashable)
            assert async_res == sync_res
            log.debug('Hashable comparison passed for method %s.', self.__async_method.__name__)

        if isinstance(async_res, fortnite_api.ReconstructAble):
            assert isinstance(sync_res, fortnite_api.ReconstructAble)

            sync_res_narrowed = cast(fortnite_api.ReconstructAble[Any, fortnite_api.http.SyncHTTPClient], sync_res)
            async_res_narrowed = cast(fortnite_api.ReconstructAble[Any, fortnite_api.http.HTTPClient], async_res)

            async_raw_data = sync_res_narrowed.to_dict()
            sync_raw_data = sync_res_narrowed.to_dict()
            assert async_raw_data == sync_raw_data
            log.debug('Raw data equality passed for method %s', self.__async_method.__name__)

            async_reconstructed = type(async_res_narrowed).from_dict(async_raw_data, client=self.__hybrid_client)
            sync_reconstructed = type(sync_res_narrowed).from_dict(sync_raw_data, client=self.__sync_client)

            assert isinstance(async_reconstructed, type(sync_reconstructed))
            assert type(async_reconstructed) is type(async_res_narrowed)
            assert type(sync_reconstructed) is type(sync_res_narrowed)
            log.debug('Reconstructed data equality passed for method %s', self.__async_method.__name__)

    async def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        # Call the sync method first
        sync_result = self.__sync_method(self.__sync_client, *args, **kwargs)

        # Call the async method
        async_result = await self.__async_method(self.__hybrid_client, *args, **kwargs)

        log.debug('Validating results for %s', self.__async_method.__name__)
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
        self.__inject_hybrid_methods()

    def __inject_hybrid_methods(self) -> None:
        # Walks through all the public coroutine methods in this class. If it finds one,
        # it will mark it as a hybrid proxy method with it and its sync counterpart.
        for key, value in fortnite_api.Client.__dict__.items():
            if inspect.iscoroutinefunction(value):
                sync_value = getattr(fortnite_api.SyncClient, key, None)
                if sync_value is not None and inspect.isfunction(sync_value):
                    setattr(self, key, HybridMethodProxy(self, self.__sync_client, value, sync_value))

    async def __aexit__(self, *args: Any) -> None:
        # We need to ensure that the sync client is also closed
        self.__sync_client.__exit__(*args)
        return await super().__aexit__(*args)


@pytest.mark.asyncio
async def test_hybrid_client():
    hybrid_client = ClientHybrid()

    # Walk through all coroutines in the normal client - ensure that
    # every coro on the normal is a proxy method on the hybrid client.
    for key, value in fortnite_api.Client.__dict__.items():
        if inspect.iscoroutinefunction(value) and not key.startswith('_'):
            assert hasattr(hybrid_client, key)

            method = getattr(hybrid_client, key)
            assert isinstance(method, HybridMethodProxy)
