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

from typing import Any, TypedDict

import pytest

import fortnite_api
from fortnite_api.abc import ReconstructAble
from fortnite_api.http import HTTPClient

# August 4th, 2024: The goal of this file is to ensure that the reconstruction methods are working as expected.
# Although every object cannot be tested, the most important ones are tested here with the assumption
# that if the overwhelming majority works then the rest should.. in theory... work as well. The
# only way around this "bulk" method would be to write a test for every single object, and with
# the current state of the library, that would be a bit overkill.
#
# If someone has the cojones to do that, then by all means, go ahead.


@pytest.mark.asyncio
async def test_reconstruct(api_key: str) -> None:
    methods_to_test: list[str] = [
        'fetch_cosmetics_all',
        'fetch_cosmetics_br',
        'fetch_cosmetics_cars',
        'fetch_cosmetics_instruments',
        'fetch_cosmetics_lego_kits',
        'fetch_variants_lego',
        'fetch_variants_beans',
        'fetch_cosmetics_tracks',
        'fetch_cosmetics_new',
        'fetch_aes',
        'fetch_banners',
        'fetch_banner_colors',
        'fetch_map',
        'fetch_news',
        'fetch_news_br',
        'fetch_news_stw',
        'fetch_playlists',
        'fetch_shop',
    ]

    async with fortnite_api.Client(api_key=api_key) as client:
        for method in methods_to_test:
            # (1) grab the method from the client
            coro = getattr(client, method)

            # (2) call the method
            try:
                result = await coro()
            except fortnite_api.NotFound:
                continue

            # If this item is reconstruct-able, do some basic checks to ensure
            # that the reconstruction is working as expected.
            if isinstance(result, fortnite_api.abc.ReconstructAble):
                narrowed: fortnite_api.abc.ReconstructAble[dict[str, Any], HTTPClient] = result

                # (3) deconstruct the object
                deconstructed = narrowed.to_dict()

                # Recreate a new instance of said object
                reconstructed = narrowed.from_dict(deconstructed, client=client)

                # (4) check that the original object and the reconstructed object are the same
                # we can't always use __eq__ because not every object has it implemented
                assert deconstructed == reconstructed.to_dict()
                assert type(narrowed) == type(reconstructed)


class DummyData(TypedDict):
    id: str


class DummyReconstruct(ReconstructAble[DummyData, HTTPClient]):
    def __init__(self, *, data: DummyData, http: HTTPClient) -> None:
        super().__init__(data=data, http=http)
        self.id: str = data['id']

    def __eq__(self, value: object) -> bool:
        return isinstance(value, DummyReconstruct) and self.id == value.id

    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)


def test_dummy_reconstruction() -> None:
    data: DummyData = {'id': '1'}

    client = fortnite_api.Client()
    http: HTTPClient = client.http
    dummy = DummyReconstruct(data=data, http=http)

    deconstructed = dummy.to_dict()
    reconstructed = DummyReconstruct.from_dict(deconstructed, client=client)

    assert dummy == reconstructed
    assert dummy.to_dict() == reconstructed.to_dict()
    assert dummy.to_dict() == deconstructed
    assert type(dummy) == type(reconstructed)
    assert isinstance(reconstructed, DummyReconstruct)
