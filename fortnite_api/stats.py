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

from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple

from .account import Account
from .utils import parse_time

if TYPE_CHECKING:
    import datetime


class BrPlayerStats:
    __slots__: Tuple[str, ...] = ('user', 'battle_pass', 'image_url', 'stats', 'raw_data')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.user: Optional[Account] = (account := data.get('account')) and Account(data=account)
        self.battle_pass: Optional[BrBattlePass] = (battle_pass := data.get('battlePass')) and BrBattlePass(data=battle_pass)
        self.image_url: str = data['image']
        self.stats: Optional[BrInputs] = (inputs := data.get('inputs')) and BrInputs(data=inputs)
        self.raw_data: Dict[str, Any] = data


class BrBattlePass:
    __slots__: Tuple[str, ...] = ('level', 'progress', 'raw_data')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.level = data.get('level')
        self.progress = data.get('progress')
        self.raw_data = data


class BrInputs:
    __slots__: Tuple[str, ...] = ('all', 'keyboard_mouse', 'gamepad', 'touch', 'raw_data')

    def __init__(self, data: Dict[str, Any]):

        _all = data.get('all')
        self.all = _all and BrInputStats(_all)

        _keyboard_mouse = data.get('keyboardMouse')
        self.keyboard_mouse = _keyboard_mouse and BrInputStats(_keyboard_mouse)

        _gamepad = data.get('gamepad')
        self.gamepad = _gamepad and BrInputStats(_gamepad)

        _touch = data.get('touch')
        self.touch = _touch and BrInputStats(_touch)
        self.raw_data = data


class BrInputStats:
    __slots__: Tuple[str, ...] = ('overall', 'solo', 'duo', 'trio', 'squad', 'raw_data')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.overall: Optional[BrGameModeStats] = (overall := data.get('overall')) and BrGameModeStats(data=overall)
        self.solo: Optional[BrGameModeStats] = (solo := data.get('solo')) and BrGameModeStats(data=solo)
        self.duo: Optional[BrGameModeStats] = (duo := data.get('duo')) and BrGameModeStats(data=duo)
        self.trio: Optional[BrGameModeStats] = (trio := data.get('trio')) and BrGameModeStats(data=trio)
        self.squad: Optional[BrGameModeStats] = (squad := data.get('squad')) and BrGameModeStats(data=squad)
        self.raw_data: Dict[str, Any] = data


class BrGameModeStats:
    __slots__: Tuple[str, ...] = (
        'score',
        'score_per_min',
        'score_per_match',
        'top5',
        'top12',
        'kills',
        'kills_per_min',
        'kills_per_match',
        'deaths',
        'kd',
        'matches',
        'win_rate',
        'minutes_played',
        'players_outlived',
        'last_modified',
        'raw_data',
    )

    def __init__(self, data: Dict[str, Any]) -> None:
        self.score: int = data['score']
        self.score_per_min: int = data['scorePerMin']
        self.score_per_match: int = data['scorePerMatch']
        self.top5: int = data['top5']
        self.top12: int = data['top12']
        self.kills: int = data['kills']
        self.kills_per_min: int = data['killsPerMin']
        self.kills_per_match: int = data['killsPerMatch']
        self.deaths: int = data['deaths']
        self.kd: int = data['kd']
        self.matches: int = data['matches']
        self.win_rate: int = data['winRate']
        self.minutes_played: int = data['minutesPlayed']
        self.players_outlived: int = data['playersOutlived']
        self.last_modified: datetime.datetime = parse_time(data['lastModified'])
