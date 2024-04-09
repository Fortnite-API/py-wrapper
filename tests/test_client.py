import inspect
import fortnite_api as fn_api

import pytest
import requests
import aiohttp


def test_sync_client_initialization():
    with requests.Session() as session, fn_api.SyncFortniteAPI(session=session) as client:
        assert client

    with fn_api.SyncFortniteAPI() as client:
        assert client


@pytest.mark.asyncio
async def test_async_client_initialization():
    async with aiohttp.ClientSession() as session, fn_api.FortniteAPI(session=session) as client:
        assert client

    assert session.closed == True, "Session should be closed after client is closed"

    async with fn_api.FortniteAPI() as client:
        assert client

    client_session = client.http.session
    assert client_session and client_session.closed


# A test to ensure that all the methods on async and sync clients are the same.
# The async client has all the main methods, so we'll walk through the async client.
def test_client_method_equivalence():
    for method in fn_api.FortniteAPI.__dict__.values():
        try:
            doc = getattr(method, '__doc__')
        except AttributeError:
            continue
        else:
            if doc and inspect.iscoroutinefunction(method):
                # This is some documented coroutine function, ensure it's on the sync client
                assert hasattr(fn_api.SyncFortniteAPI, method.__name__)
