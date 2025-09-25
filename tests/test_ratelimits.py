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

from unittest.mock import AsyncMock, MagicMock

import aiohttp
import pytest
from pytest_mock import MockerFixture

from fortnite_api.errors import RateLimited
from fortnite_api.http import HTTPClient, Route, SyncHTTPClient
from fortnite_api.utils import now


@pytest.fixture
def async_mock_response(mocker: MockerFixture) -> MagicMock:
    mock_response = mocker.MagicMock()
    mock_response.status = 429
    mock_response.headers = {
        'X-Ratelimit-Remaining': '0',
        'Content-Type': 'application/json',
        'X-Ratelimit-Reset': now().isoformat(timespec='milliseconds'),
    }
    mock_response.text = AsyncMock(return_value='{"data": {"error": "Rate limit exceeded."}, "status": "429"}')

    return mock_response


@pytest.fixture
def sync_mock_response(mocker: MockerFixture) -> MagicMock:
    # Mocks a requests response object
    mock_response = mocker.MagicMock()
    mock_response.status_code = 429
    mock_response.headers = {
        'X-Ratelimit-Remaining': '0',
        'Content-Type': 'application/json',
        'X-Ratelimit-Reset': now().isoformat(timespec='milliseconds'),
    }
    mock_response.text = '{"data": {"error": "Rate limit exceeded."}, "status": "429"}'
    return mock_response


@pytest.fixture
def async_mock_session(mocker: MockerFixture, async_mock_response: MagicMock):
    mock_session = mocker.MagicMock()
    mock_session.request.return_value.__aenter__.return_value = async_mock_response

    return mock_session


@pytest.fixture
def sync_mock_session(mocker: MockerFixture, sync_mock_response: MagicMock):
    # Mocks the requests.Session object
    mock_session = mocker.MagicMock()
    mock_session.request.return_value.__enter__.return_value = sync_mock_response

    return mock_session


@pytest.fixture
def async_client(async_mock_session: aiohttp.ClientSession) -> HTTPClient:
    return HTTPClient(session=async_mock_session)


@pytest.fixture
def sync_client(sync_mock_session: MagicMock) -> SyncHTTPClient:
    return SyncHTTPClient(session=sync_mock_session)


@pytest.mark.asyncio
async def test_async_rate_limit_handling(async_client: HTTPClient):
    # Make a request
    route = Route('GET', 'https://example.com')
    with pytest.raises(RateLimited) as excinfo:
        # This will try 5 times to request, and each time get a 429 response. After it
        # should raise the RateLimited error. Any subsequent requests with the same route
        # should immediately raise the RateLimited error.
        await async_client.request(route)

    # Check that the rate limit error was raised
    assert excinfo.type is RateLimited

    # Assert that the client did in fact try 5 times to request using the mock session
    assert async_client.session.request.call_count == 5  # type: ignore


def test_sync_rate_limit_handling(sync_client: SyncHTTPClient):
    route = Route('GET', 'https://example.com')
    with pytest.raises(RateLimited) as excinfo:
        # This will try 5 times to request, and each time get a 429 response. After it
        # should raise the RateLimited error. Any subsequent requests with the same route
        # should immediately raise the RateLimited error.
        sync_client.request(route)

    assert excinfo.type is RateLimited

    # Assert that the client did in fact try 5 times to request using the mock session
    assert sync_client.session.request.call_count == 5  # type: ignore
