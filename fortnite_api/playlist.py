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
