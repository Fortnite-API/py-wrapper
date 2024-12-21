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

import logging
from collections.abc import Callable, Coroutine, Iterable
from typing import Any, TypeVar
from typing_extensions import ParamSpec, TypeAlias

import pytest

import fortnite_api

from ..client.test_client_hybrid import ClientHybrid
from ..conftest import TEST_COSMETIC_ID, TEST_INVALID_COSMETIC_ID
from .cosmetic_utils import (
    validate_cosmetic_br,
    validate_cosmetic_car,
    validate_cosmetic_instrument,
    validate_cosmetic_lego_kit,
    validate_cosmetic_track,
    validate_variant_bean,
    validate_variant_lego,
)

P = ParamSpec('P')
T = TypeVar('T')
AnyCosmetic: TypeAlias = fortnite_api.Cosmetic[Any, Any]
CoroFunc = Callable[P, Coroutine[Any, Any, T]]

log = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_fetch_cosmetic_types(api_key: str, response_flags: fortnite_api.ResponseFlags) -> None:
    # A lot of the cosmetic fetching methods on the client all return TransformerListProxy[CosmeticT].
    # To encompass all these in a single test, we're going to create a mapping of cosmetic fetcher
    # to validator function. To give some extra error information, if needed, we'll catch any exceptions
    # raised from these functions, log them for the report, then re-raise them for pytest to catch.

    async with ClientHybrid(api_key=api_key, response_flags=response_flags) as client:
        # Pyright can't seem to narrow CosmeticBr[Any] to fortnite_api.Cosmetic[Any, Any], but
        # Callable[[Any], None] is actually requesting that an instance of AnyCosmetic is passed.
        FETCHER_VALIDATOR_MAPPING: dict[CoroFunc[..., Iterable[AnyCosmetic]], Callable[[Any], None]] = {
            client.fetch_cosmetics_br: validate_cosmetic_br,
            client.fetch_cosmetics_cars: validate_cosmetic_car,
            client.fetch_cosmetics_instruments: validate_cosmetic_instrument,
            client.fetch_cosmetics_lego_kits: validate_cosmetic_lego_kit,
            client.fetch_variants_lego: validate_variant_lego,
            client.fetch_variants_beans: validate_variant_bean,
            client.fetch_cosmetics_tracks: validate_cosmetic_track,
        }

        for cosmetic_fetcher, validator in FETCHER_VALIDATOR_MAPPING.items():
            try:
                cosmetics = await cosmetic_fetcher()
            except Exception:
                # For some reason, fetching this has failed. This is most likely an API issue
                # or something incorrect with the client, as the actual transformation of
                # DictT to cosmetic object is done in the for loop below.
                log.error('Failed to fetch cosmetics from method %s.', cosmetic_fetcher.__name__)
                raise

            try:
                # This is wrapped in a try block due to the actual object transformation, as discussed
                # above. If it's going to, the initialization of an object is going to fail here. We want
                # to ensure that this is picked up, if so.
                for cosmetic in cosmetics:
                    try:
                        validator(cosmetic)
                    except AssertionError:
                        # We know that the object is initialized okay, but this validator function has failed.
                        # Ensure that some relevant information is logged alongside this.
                        log.error(
                            'Validation for cosmetic %s has failed from fetcher %s.',
                            cosmetic.__class__.__name__,
                            cosmetic_fetcher.__name__,
                        )
                        raise
            except AssertionError:
                # Handled inside the loop already. Simply want to bring this up the flag pole.
                raise
            except Exception:
                # A cosmetic has failed to initialize or the validator function has thrown some sort of exception.
                # Either way, this is something that is not expected behavior.
                log.error('Error related to fetcher method %s', cosmetic_fetcher.__name__)
                raise


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

    # Ensure that the response from the API is not 0 cosmetics. If it is, it is likely an
    # API issue that needs to be addressed.
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
