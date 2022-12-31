from datetime import datetime

from fortnite_api import Account


class BrPlayerStats:

    def __init__(self, data):
        self.user = Account(data.get('account')) if data.get('account') else None
        self.battle_pass = BrBattlePass(data['battlePass']) if data.get('battlePass') else None
        self.image_url = data.get('image')
        self.stats = BrInputs(data['stats']) if data.get('stats') else None
        self.raw_data = data


class BrBattlePass:

    def __init__(self, data):
        self.level = data.get('level')
        self.progress = data.get('progress')
        self.raw_data = data


class BrInputs:

    def __init__(self, data):
        self.all = BrInputStats(data.get('all')) if data.get('all') else None
        self.keyboard_mouse = BrInputStats(data.get('keyboardMouse')) if data.get('keyboardMouse') else None
        self.gamepad = BrInputStats(data.get('gamepad')) if data.get('gamepad') else None
        self.touch = BrInputStats(data.get('touch')) if data.get('touch') else None
        self.raw_data = data


class BrInputStats:

    def __init__(self, data):
        self.overall = BrGameModeStats(data.get('overall')) if data.get('overall') else None
        self.solo = BrGameModeStats(data.get('solo')) if data.get('solo') else None
        self.duo = BrGameModeStats(data.get('duo')) if data.get('duo') else None
        self.trio = BrGameModeStats(data.get('trio')) if data.get('trio') else None
        self.squad = BrGameModeStats(data.get('squad')) if data.get('squad') else None
        self.raw_data = data


class BrGameModeStats:

    def __init__(self, data):
        self.score = data.get('score')
        self.score_per_min = data.get('scorePerMin')
        self.scorePerMatch = data.get('scorePerMatch')
        self.top5 = data.get('top5')
        self.top12 = data.get('top12')
        self.kills = data.get('kills')
        self.kills_per_min = data.get('killsPerMin')
        self.kills_per_match = data.get('killsPerMatch')
        self.deaths = data.get('deaths')
        self.kd = data.get('kd')
        self.matches = data.get('matches')
        self.win_rate = data.get('winRate')
        self.minutes_played = data.get('minutesPlayed')
        self.players_outlived = data.get('playersOutlived')
        try:
            self.last_modified = datetime.strptime(data.get('lastModified'), '%Y-%m-%dT%H:%M:%S%z')
        except (ValueError, TypeError):
            self.updated = None
