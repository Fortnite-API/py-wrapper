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

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

from .abc import IdComparable
from .utils import parse_time

if TYPE_CHECKING:
    import datetime


class Playlist(IdComparable):

    __slots__: Tuple[str, ...] = (
        'id',
        'name',
        'sub_name',
        'description',
        'game_type',
        'min_players',
        'max_players',
        'max_teams',
        'max_team_size',
        'max_squads',
        'max_squad_size',
        'is_default',
        'is_tournament',
        'is_limited_time_mode',
        'is_large_team_game',
        'accumulate_to_profile_stats',
        'showcase_image',
        'mission_icon',
        'gameplay_tags',
        'path',
        'added',
        'raw_data',
    )

    def __init__(self, data: Dict[str, Any]) -> None:
        self.id: str = data['id']
        self.name: str = data['name']
        self.sub_name: str = data['subName']
        self.description: str = data['description']
        self.game_type: str = data['gameType']
        self.min_players: int = data['minPlayers']
        self.max_players: int = data['maxPlayers']
        self.max_teams: int = data['maxTeams']
        self.max_team_size: int = data['maxTeamSize']
        self.max_squads: int = data['maxSquads']
        self.max_squad_size: int = data['maxSquadSize']

        self.is_default: bool = data['isDefault']
        self.is_tournament: bool = data['isTournament']
        self.is_limited_time_mode: bool = data['isLimitedTimeMode']
        self.is_large_team_game: bool = data['isLargeTeamGame']
        self.accumulate_to_profile_stats: Any = data['accumulateToProfileStats']  # Unknown for now

        images = data.get('images', {})
        self.showcase_image: Optional[str] = images.get('showcase')
        self.mission_icon: Optional[str] = images.get('missionIcon')

        self.gameplay_tags: List[str] = data.get('gameplayTags', [])
        self.path: str = data['path']

        self.added: datetime.datetime = parse_time(data['added'])
        self.raw_data: Dict[str, Any] = data
