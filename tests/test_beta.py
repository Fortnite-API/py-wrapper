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

import pytest

import fortnite_api
from fortnite_api.client import beta_method


def test_sync_cannot_call_beta_method():
    client = fortnite_api.SyncClient(beta=False)
    with client, pytest.raises(expected_exception=fortnite_api.BetaAccessNotEnabled):
        client.beta_fetch_new_display_assets()


@pytest.mark.asyncio
async def test_async_cannot_call_beta_method():
    client = fortnite_api.Client(beta=False)
    with pytest.raises(fortnite_api.BetaAccessNotEnabled):
        async with client:
            await client.beta_fetch_new_display_assets()


# A mock of the SyncClient beta function that raises an error
class MockSyncFortniteAPI(fortnite_api.SyncClient):

    @beta_method
    def beta_mock_call(self):
        raise ValueError('Mock error')


# A mock of the Client beta function that raises an error
class MockFortniteAPI(fortnite_api.Client):

    @beta_method
    async def beta_mock_call(self):
        raise ValueError('Mock error')


def test_sync_beta_method_error():
    client = MockSyncFortniteAPI(beta=True)
    with client, pytest.raises(fortnite_api.BetaUnknownException) as exc_info:
        client.beta_mock_call()

    # Ensure the exception.__cause__ is the original exception
    assert exc_info.value.__cause__ is not None
    assert isinstance(exc_info.value.__cause__, ValueError)


@pytest.mark.asyncio
async def test_async_beta_method_error():
    client = MockFortniteAPI(beta=True)
    with pytest.raises(fortnite_api.BetaUnknownException) as exc_info:
        async with client:
            await client.beta_mock_call()

    # Ensure the exception.__cause__ is the original exception
    assert exc_info.value.__cause__ is not None
    assert isinstance(exc_info.value.__cause__, ValueError)
