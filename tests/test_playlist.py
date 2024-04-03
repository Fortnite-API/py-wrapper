from typing import Dict, Union, List
import pytest


from datetime import datetime, timezone
from fortnite_api.playlist import Playlist


@pytest.fixture
def sample_playlist_data():
    return {
        'id': '123',
        'name': 'Test Playlist',
        'subName': 'Test Subname',
        'description': 'Test Description',
        'gameType': 'Test Game Type',
        'minPlayers': 1,
        'maxPlayers': 100,
        'maxTeams': 10,
        'maxTeamSize': 4,
        'maxSquads': 20,
        'maxSquadSize': 2,
        'isDefault': True,
        'isTournament': False,
        'isLimitedTimeMode': True,
        'isLargeTeamGame': False,
        'accumulateToProfileStats': None,
        'images': {'showcase': 'showcase_image_url', 'missionIcon': 'mission_icon_url'},
        'gameplayTags': ['tag1', 'tag2'],
        'path': '/path/to/playlist',
        'added': '2022-01-01T00:00:00Z',
    }


def test_playlist_initialization(sample_playlist_data: Dict[str, Union[str, int, bool, List[str]]]):
    playlist = Playlist(sample_playlist_data)

    assert playlist.id == '123'
    assert playlist.name == 'Test Playlist'
    assert playlist.sub_name == 'Test Subname'
    assert playlist.description == 'Test Description'
    assert playlist.game_type == 'Test Game Type'
    assert playlist.min_players == 1
    assert playlist.max_players == 100
    assert playlist.max_teams == 10
    assert playlist.max_team_size == 4
    assert playlist.max_squads == 20
    assert playlist.max_squad_size == 2
    assert playlist.is_default is True
    assert playlist.is_tournament is False
    assert playlist.is_limited_time_mode is True
    assert playlist.is_large_team_game is False
    assert playlist.accumulate_to_profile_stats is None
    assert playlist.showcase_image == 'showcase_image_url'
    assert playlist.mission_icon == 'mission_icon_url'
    assert playlist.gameplay_tags == ['tag1', 'tag2']
    assert playlist.path == '/path/to/playlist'
    assert playlist.added == datetime(2022, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    assert playlist.raw_data == sample_playlist_data
