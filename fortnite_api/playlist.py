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

from typing import TYPE_CHECKING, Any

from .abc import Hashable, ReconstructAble
from .asset import Asset
from .http import HTTPClientT
from .utils import get_with_fallback, parse_time

if TYPE_CHECKING:
    import datetime


__all__: tuple[str, ...] = ('PlaylistImages', 'Playlist')


class PlaylistImages(ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.PlaylistImages

    Represents images that are associated with a Fortnite Playlist. This
    class inherits from :class:`~fortnite_api.ReconstructAble`.

    Attributes
    ------------
    showcase: Optional[:class:`fortnite_api.Asset`]
        A showcase image for the playlist, if any.
    mission_icon: Optional[:class:`fortnite_api.Asset`]
        A mission icon for the playlist, if any.
    """

    __slots__: tuple[str, ...] = ('showcase', 'mission_icon')

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        _showcase = data.get('showcase')
        self.showcase: Asset[HTTPClientT] | None = _showcase and Asset(url=_showcase, http=http)

        _mission_icon = data.get('missionIcon')
        self.mission_icon: Asset[HTTPClientT] | None = _mission_icon and Asset(url=_mission_icon, http=http)


class Playlist(Hashable, ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.Playlist

    Represents a Fortnite Playlist. This class inherits from :class:`~fortnite_api.Hashable` and :class:`~fortnite_api.ReconstructAble`.

    Attributes
    -----------
    id: :class:`str`
        The ID of the playlist.
    name: :class:`str`
        The playlist's name.
    sub_name: Optional[:class:`str`]
        The playlist's sub name, if any.
    description: Optional[:class:`str`]
        A description of the playlist.
    game_type: Optional[:class:`str`]
        The type of game the playlist is, if any.
    rating_type: Optional[:class:`str`]
        The rating type of the playlist, if any.
    min_players: :class:`int`
        The minimum amount of players required. Will be ``-1`` if there is no limit.
    max_players: :class:`int`
        The maximum amount of players allowed. Will be ``-1`` if there is no limit.
    max_teams: :class:`int`
        The maximum amount of teams allowed. Will be ``-1`` if there is no limit.
    max_team_size: :class:`int`
        The maximum amount of players per team. Will be ``-1`` if there is no limit.
    max_squads: :class:`int`
        The maximum amount of squads allowed. Will be ``-1`` if there is no limit.
    max_squad_size: :class:`int`
        The maximum amount of players per squad. Will be ``-1`` if there is no limit.
    is_default: :class:`bool`
        Whether the playlist is the default one.
    is_tournament: :class:`bool`
        Whether this playlist is a tournament.
    is_limited_time_mode: :class:`bool`
        Whether this playlist is a limited time mode.
    is_large_team_game: :class:`bool`
        Whether this playlist is a large team game.
    accumulate_to_profile_stats: :class:`bool`
        Whether this playlist accumulates to profile stats.
    images: Optional[:class:`fortnite_api.PlaylistImages`]
        The images associated with the playlist.
    gameplay_tags: List[:class:`str`]
        The gameplay tags for the playlist.
    path: :class:`str`
        The path of the playlist.
    added: :class:`datetime.datetime`
        The time the playlist was added.
    """

    __slots__: tuple[str, ...] = (
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
        'images',
        'gameplay_tags',
        'path',
        'added',
    )

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)
        self.id: str = data['id']
        self.name: str = data['name']
        self.sub_name: str | None = data.get('subName')
        self.description: str | None = data.get('description')

        self.game_type: str | None = data.get('gameType')  # TODO: Make this into an enum
        self.rating_type: str | None = data.get('ratingType')

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
        self.accumulate_to_profile_stats: bool = data['accumulateToProfileStats']

        _images = data.get('images')
        self.images: PlaylistImages[HTTPClientT] | None = _images and PlaylistImages(data=_images, http=http)

        self.gameplay_tags: list[str] = get_with_fallback(data, 'gameplayTags', list)
        self.path: str = data['path']

        self.added: datetime.datetime = parse_time(data['added'])
