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

import aiohttp
import pytest
import requests

import fortnite_api


def test_sync_client_initialization():
    with requests.Session() as session, fortnite_api.SyncClient(session=session) as client:
        assert client

    with fortnite_api.SyncClient() as client:
        assert client


@pytest.mark.asyncio
async def test_async_client_initialization():
    async with aiohttp.ClientSession() as session, fortnite_api.Client(session=session) as client:
        assert client

    assert session.closed, "Session should be closed after client is closed"

    async with fortnite_api.Client() as client:
        assert client

    client_session = client.http.session
    assert client_session and client_session.closed


# A test to ensure that all the methods on async and sync clients are the same.
# The async client has all the main methods, so we'll walk through the async client.
def test_client_method_equivalence():
    for method in fortnite_api.Client.__dict__.values():
        try:
            doc = getattr(method, '__doc__')
        except AttributeError:
            continue
        else:
            if doc and inspect.iscoroutinefunction(method):
                # This is some documented coroutine function, ensure it's on the sync client
                assert hasattr(fortnite_api.SyncClient, method.__name__)


@pytest.mark.asyncio
async def test_async_client_without_content_manager():
    session = aiohttp.ClientSession()
    client = fortnite_api.Client(session=session)
    assert client
    assert client.http.session is not None

    # Ensure we can make a request
    await client.fetch_aes()

    await session.close()
    assert client.http.session.closed

    # Ensure we can't make a request after closing the session
    with pytest.raises(RuntimeError):
        await client.fetch_aes()


def test_sync_client_without_content_manager():
    session = requests.Session()
    client = fortnite_api.SyncClient(session=session)
    assert client
    assert client.http.session is not None

    # Ensure we can make a request
    client.fetch_aes()

    # Requests Session close doesn't actually close the session, so we'll just close it and
    # assume it's closed.
    session.close()
