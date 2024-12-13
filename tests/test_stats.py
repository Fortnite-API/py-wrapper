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

import datetime
from typing import Any

import pytest

import fortnite_api

from .client.test_client_hybrid import ClientHybrid
from .conftest import (
    TEST_INVALID_STAT_ACCOUNT_ID,
    TEST_INVALID_STAT_ACCOUNT_NAME,
    TEST_STAT_ACCOUNT_ID,
    TEST_STAT_ACCOUNT_NAME,
)


def _test_stats(player_stats: fortnite_api.BrPlayerStats[Any]) -> None:
    assert player_stats.user

    if player_stats.battle_pass:
        assert isinstance(player_stats.battle_pass.level, int)
        assert isinstance(player_stats.battle_pass.progress, int)

    stats = player_stats.inputs
    overall_stats = stats and stats.all and stats.all.overall
    if not overall_stats:
        # Nothing we should be testing
        return

    assert isinstance(overall_stats, fortnite_api.BrGameModeStats)
    assert isinstance(overall_stats.score, int)
    assert isinstance(overall_stats.score_per_min, float)
    assert isinstance(overall_stats.score_per_match, float)
    assert isinstance(overall_stats.wins, int)

    # This is overall stats, so these topX should all be not None
    assert isinstance(overall_stats.top3, int)
    assert isinstance(overall_stats.top5, int)
    assert isinstance(overall_stats.top6, int)
    assert isinstance(overall_stats.top10, int)
    assert isinstance(overall_stats.top12, int)
    assert isinstance(overall_stats.top25, int)

    assert isinstance(overall_stats.kills, int)
    assert isinstance(overall_stats.kills_per_min, float)
    assert isinstance(overall_stats.kills_per_match, float)

    assert isinstance(overall_stats.deaths, int)
    assert isinstance(overall_stats.kd, float)
    assert isinstance(overall_stats.win_rate, float)
    assert isinstance(overall_stats.minutes_played, int)
    assert isinstance(overall_stats.players_outlived, int)
    assert isinstance(overall_stats.last_modified, datetime.datetime)


@pytest.mark.asyncio
async def test_fetch_br_stats_by_name(api_key: str):
    async with ClientHybrid(api_key=api_key) as client:
        with pytest.raises(fortnite_api.NotFound):
            await client.fetch_br_stats(name=TEST_INVALID_STAT_ACCOUNT_NAME)
        stats = await client.fetch_br_stats(name=TEST_STAT_ACCOUNT_NAME, image=fortnite_api.StatsImageType.ALL)

    assert stats is not None
    _test_stats(stats)


@pytest.mark.asyncio
async def test_fetch_br_stats_by_account_id(api_key: str):
    async with ClientHybrid(api_key=api_key) as client:
        with pytest.raises(fortnite_api.NotFound):
            await client.fetch_br_stats(name=TEST_INVALID_STAT_ACCOUNT_ID)
        stats = await client.fetch_br_stats(account_id=TEST_STAT_ACCOUNT_ID, image=fortnite_api.StatsImageType.ALL)

    assert stats is not None
    _test_stats(stats)
