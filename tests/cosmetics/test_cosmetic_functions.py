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

from ..client.test_client_hybrid import ClientHybrid
from ..conftest import TEST_COSMETIC_ID, TEST_INVALID_COSMETIC_ID
from .cosmetic_utils import (
    test_cosmetic_br,
    test_cosmetic_car,
    test_cosmetic_instrument,
    test_cosmetic_lego_kits,
    test_cosmetic_track,
    test_variant_bean,
    test_variant_lego,
)


@pytest.mark.asyncio
async def test_fetch_cosmetics_br(api_key: str):
    async with ClientHybrid(api_key=api_key) as client:
        cosmetics_br = await client.fetch_cosmetics_br()

    for cosmetic in cosmetics_br:
        test_cosmetic_br(cosmetic)


@pytest.mark.asyncio
async def test_fetch_cosmetics_cars(api_key: str, response_flags: fortnite_api.ResponseFlags):
    async with ClientHybrid(api_key=api_key, response_flags=response_flags) as client:
        cosmetics_cars = await client.fetch_cosmetics_cars()

    for cosmetic in cosmetics_cars:
        test_cosmetic_car(cosmetic)


@pytest.mark.asyncio
async def test_fetch_cosmetics_instruments(api_key: str, response_flags: fortnite_api.ResponseFlags):
    async with ClientHybrid(api_key=api_key, response_flags=response_flags) as client:
        cosmetics_instruments = await client.fetch_cosmetics_instruments()

    for cosmetic in cosmetics_instruments:
        test_cosmetic_instrument(cosmetic)


@pytest.mark.asyncio
async def test_fetch_cosmetics_lego_kits(api_key: str, response_flags: fortnite_api.ResponseFlags):
    async with ClientHybrid(api_key=api_key, response_flags=response_flags) as client:
        lego_kits = await client.fetch_cosmetics_lego_kits()

    for kit in lego_kits:
        test_cosmetic_lego_kits(kit)


@pytest.mark.asyncio
async def test_fetch_variants_lego(api_key: str, response_flags: fortnite_api.ResponseFlags):
    async with ClientHybrid(api_key=api_key, response_flags=response_flags) as client:
        lego_variants = await client.fetch_variants_lego()

    for lego in lego_variants:
        test_variant_lego(lego)


@pytest.mark.asyncio
async def test_fetch_variants_beans(api_key: str, response_flags: fortnite_api.ResponseFlags):
    async with ClientHybrid(api_key=api_key, response_flags=response_flags) as client:
        beans_variants = await client.fetch_variants_beans()

    for bean in beans_variants:
        test_variant_bean(bean)


@pytest.mark.asyncio
async def test_fetch_cosmetics_tracks(api_key: str, response_flags: fortnite_api.ResponseFlags):
    async with ClientHybrid(api_key=api_key, response_flags=response_flags) as client:
        cosmetics_tracks = await client.fetch_cosmetics_tracks()

    for cosmetic in cosmetics_tracks:
        test_cosmetic_track(cosmetic)


@pytest.mark.asyncio
async def test_fetch_cosmetic_br(api_key: str, response_flags: fortnite_api.ResponseFlags):
    async with ClientHybrid(api_key=api_key, response_flags=response_flags) as client:
        with pytest.raises(fortnite_api.NotFound):
            await client.fetch_cosmetic_br(TEST_INVALID_COSMETIC_ID)
        cosmetic_br = await client.fetch_cosmetic_br(TEST_COSMETIC_ID)

    assert isinstance(cosmetic_br, fortnite_api.CosmeticBr)
    assert cosmetic_br.id == TEST_COSMETIC_ID


@pytest.mark.asyncio
async def test_fetch_cosmetics_new(api_key: str, response_flags: fortnite_api.ResponseFlags):
    async with ClientHybrid(api_key=api_key, response_flags=response_flags) as client:
        new_cosmetics = await client.fetch_cosmetics_new()

    assert isinstance(new_cosmetics, fortnite_api.NewCosmetics)

    assert new_cosmetics.global_hash
    assert new_cosmetics.date
    assert new_cosmetics.global_last_addition
    assert new_cosmetics.build
    assert new_cosmetics.previous_build

    assert isinstance(new_cosmetics.br, fortnite_api.NewCosmetic)
    assert isinstance(new_cosmetics.tracks, fortnite_api.NewCosmetic)
    assert isinstance(new_cosmetics.instruments, fortnite_api.NewCosmetic)
    assert isinstance(new_cosmetics.cars, fortnite_api.NewCosmetic)
    assert isinstance(new_cosmetics.lego, fortnite_api.NewCosmetic)
    assert isinstance(new_cosmetics.lego_kits, fortnite_api.NewCosmetic)


@pytest.mark.asyncio
async def test_fetch_cosmetics_all(api_key: str, response_flags: fortnite_api.ResponseFlags):
    async with ClientHybrid(api_key=api_key, response_flags=response_flags) as client:
        cosmetics_all = await client.fetch_cosmetics_all()

    assert isinstance(cosmetics_all, fortnite_api.CosmeticsAll)

    assert cosmetics_all.br
    assert cosmetics_all.tracks
    assert cosmetics_all.instruments
    assert cosmetics_all.cars
    assert cosmetics_all.lego
    assert cosmetics_all.lego_kits
    assert cosmetics_all.beans
    assert cosmetics_all.to_dict()

    # Ensure that you can iter over the cosmetics
    assert len(cosmetics_all) != 0
    for cosmetic in cosmetics_all:
        assert isinstance(cosmetic, fortnite_api.Cosmetic)


@pytest.mark.asyncio
async def test_search_cosmetics(api_key: str, response_flags: fortnite_api.ResponseFlags):
    async with ClientHybrid(api_key=api_key, response_flags=response_flags) as client:
        with pytest.raises(fortnite_api.NotFound):
            await client.search_br_cosmetics(id=TEST_INVALID_COSMETIC_ID)
        cosmetics_multiple_set = await client.search_br_cosmetics(multiple=True, has_set=True)
        cosmetic_single_set = await client.search_br_cosmetics(multiple=False, has_set=True)

    assert isinstance(cosmetics_multiple_set, list)
    for cosmetic in cosmetics_multiple_set:
        assert cosmetic.set is not None

    assert isinstance(cosmetic_single_set, fortnite_api.CosmeticBr)
    assert cosmetic_single_set.set is not None
