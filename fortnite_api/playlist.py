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

from datetime import datetime


class Playlist:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.sub_name = data['subName']
        self.description = data['description']
        self.game_type = data['gameType']
        self.rating_type = data['ratingType']
        self.min_players = data['minPlayers']
        self.max_players = data['maxPlayers']
        self.max_teams = data['maxTeams']
        self.max_team_size = data['maxTeamSize']
        self.max_squads = data['maxSquads']
        self.max_squad_size = data['maxSquadSize']

        self.is_default = data['isDefault']
        self.is_tournament = data['isTournament']
        self.is_limited_time_mode = data['isLimitedTimeMode']
        self.is_large_team_game = data['isLargeTeamGame']
        self.accumulate_to_profile_stats = data['accumulateToProfileStats']
        if data.get('images') is not None:
            images = data['images']
            self.showcase_image = images['showcase']
            self.mission_icon = images['missionIcon']
        else:
            self.showcase_image = None
            self.mission_icon = None
        self.gameplay_tags = [gameplay_tag for gameplay_tag in data.get('gameplayTags')] \
            if data.get('gameplayTags') is not None else None
        self.path = data['path']
        try:
            self.added = datetime.strptime(data.get('added'), '%Y-%m-%dT%H:%M:%S%z')
        except (ValueError, TypeError):
            self.added = None
        self.raw_data = data
