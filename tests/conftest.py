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

import os
from typing import Final

import pytest

from fortnite_api.flags import ResponseFlags
from fortnite_api.http import HTTPClient, SyncHTTPClient

# Constants for general testing
TEST_ACCOUNT_ID: Final[str] = "4735ce9132924caf8a5b17789b40f79c"
TEST_ACCOUNT_NAME: Final[str] = "Ninja"
TEST_CREATOR_CODE: Final[str] = "ninja"
TEST_INVALID_CREATOR_CODE: Final[str] = "invalidcreatorcode"

# Constant for testing cosmetics
TEST_COSMETIC_ID: Final[str] = "Backpack_BrakePedal"
TEST_INVALID_COSMETIC_ID: Final[str] = "Invalid"

# Constants for testing playlist fetching
TEST_PLAYLIST_ID: Final[str] = "Playlist_NoBuildBR_Duo"
TEST_INVALID_PLAYLIST_ID: Final[str] = "Invalid"

# Constants for fetching stats
TEST_STAT_ACCOUNT_NAME = "Luc1412"
TEST_INVALID_STAT_ACCOUNT_NAME = "InvalidAccountName"
TEST_STAT_ACCOUNT_ID = "369644c6224d4845aa2b00e63b60241d"
TEST_INVALID_STAT_ACCOUNT_ID = "21332424543544535435435"


@pytest.fixture(scope='session')
def api_key() -> str:
    # This fixture is called once per test session, so we can check if we are in a CI environment
    # or a local development environment. If we are in a CI environment, we can get the API key from
    # the environment variables, otherwise we can load it from a .env file.

    gh_actions = os.environ.get('GITHUB_ACTIONS')
    if gh_actions and gh_actions == 'true':
        return os.environ['TEST_API_KEY']

    # This is a local development environment, try and load a .env file and get the API key
    from dotenv import load_dotenv

    load_dotenv()
    return os.environ['TEST_API_KEY']


@pytest.fixture(scope='session', params=[flag for flag in ResponseFlags])
def response_flags(request: pytest.FixtureRequest) -> ResponseFlags:
    # Returns all the possible flags that can be used in the client. This is to ensure that passing
    # flags to both the client and the methods that require them is consistent.
    return request.param


@pytest.fixture(scope='session')
def mock_sync_http() -> SyncHTTPClient:
    return SyncHTTPClient()


@pytest.fixture(scope='session')
def mock_async_http() -> HTTPClient:
    return HTTPClient()
