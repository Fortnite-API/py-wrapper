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

from typing import TYPE_CHECKING, Any, Optional

from .abc import ReconstructAble
from .account import Account
from .asset import Asset
from .http import HTTPClientT
from .utils import parse_time

if TYPE_CHECKING:
    import datetime

__all__: tuple[str, ...] = (
    "BrPlayerStats",
    "BrBattlePass",
    "BrInputs",
    "BrInputStats",
    "BrGameModeStats",
)


class BrBattlePass(ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.BrBattlePass

    Represents a Fortnite Battle Royale player's battle pass level and progress.
    This class inherits from :class:`~fortnite_api.ReconstructAble`.

    Attributes
    ----------
    level: :class:`int`
        The player's battle pass level.
    progress: :class:`int`
        The progress through the current battle pass.
    """

    __slots__: tuple[str, ...] = ("level", "progress")

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.level: int = data["level"]
        self.progress: Optional[int] = data["progress"]


class BrGameModeStats(ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.BrGameModeStats

    Represents the specific stats for a Fortnite player in a
    specific game mode on a specific input type. This class inherits
    from :class:`~fortnite_api.ReconstructAble`.

    Attributes
    ----------
    score: :class:`int`
        The total score for the stats for a specific game mode.
    score_per_min: :class:`float`
        The score per minute for the stats for a specific game mode. This is the score divided by the minutes played.
    score_per_match: :class:`float`
        The score per match for the stats for a specific game mode. This is the score divided by the matches played.
    wins: :class:`int`
        The total number of wins in this specific game mode.
    top3: Optional[:class:`int`]
        The number of times the player has placed in the top 3 (10 players left remaining)
        in this specific game mode. This is only available when the game mode for these
        stats is a :attr:`fortnite_api.BrInputStats.squad` game mode or :attr:`fortnite_api.BrInputStats.overall`.
    top5: Optional[:class:`int`]
        The number of times the player has placed in the top 5 (10 players left remaining)
        in this specific game mode. This is only available when the game mode
        for these stats is a :attr:`fortnite_api.BrInputStats.duo` game mode or :attr:`fortnite_api.BrInputStats.overall`.
    top6: Optional[:class:`int`]
        The number of times the player has placed in the top 6 (25 players left remaining)
        in this specific game mode. This is only available when the game mode
        for these stats is a :attr:`fortnite_api.BrInputStats.squad` game mode or :attr:`fortnite_api.BrInputStats.overall`.
    top10: Optional[:class:`int`]
        The number of times the player has placed in the top 10 (10 players left remaining) in
        this specific game mode. This is only available when the game mode for these
        stats is a :attr:`fortnite_api.BrInputStats.solo` game mode or :attr:`fortnite_api.BrInputStats.overall`.
    top12: Optional[:class:`int`]
        The number of times the player has placed in the top 12 (25 players left remaining)
        in this specific game mode. This is only available when the game mode
        for these stats is a :attr:`fortnite_api.BrInputStats.duo` game mode or :attr:`fortnite_api.BrInputStats.overall`.
    top25: Optional[:class:`int`]
        The number of times the player has placed in the top 25 (25 players left remaining)
        in this specific game mode. This is only available when the game mode for
        these stats is a :attr:`fortnite_api.BrInputStats.solo` game mode or :attr:`fortnite_api.BrInputStats.overall`.
    kills: :class:`int`
        The total number of kills in this specific game mode.
    kills_per_min: :class:`float`
        The kills per minute for the stats for a specific game mode. This is the kills divided by the minutes played.
    kills_per_match: :class:`float`
        The kills per match for the stats for a specific game mode. This is the kills divided by the matches played.
    deaths: :class:`int`
        The total number of deaths in this specific game mode.
    kd: :class:`float`
        The kill/death ratio for this specific game mode. This is the kills divided by the deaths.
    matches: :class:`int`
        The total number of matches played in this specific game mode.
    win_rate: :class:`float`
        The win rate for this specific game mode. This is the wins divided by the matches played.
    minutes_played: :class:`int`
        The total number of minutes played in this specific game mode.
    players_outlived: :class:`int`
        The total number of players outlived in this specific game mode.
    last_modified: :class:`datetime.datetime`
        The date when this stat data was last updated within the Epic Games API.
    """

    __slots__: tuple[str, ...] = (
        "score",
        "score_per_min",
        "score_per_match",
        "wins",
        "top3",
        "top5",
        "top6",
        "top10",
        "top12",
        "top25",
        "kills",
        "kills_per_min",
        "kills_per_match",
        "deaths",
        "kd",
        "matches",
        "win_rate",
        "minutes_played",
        "players_outlived",
        "last_modified",
    )

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.score: int = data["score"]
        self.score_per_min: float = data["scorePerMin"]
        self.score_per_match: float = data["scorePerMatch"]
        self.wins: int = data["wins"]

        self.top3: Optional[int] = data.get("top3")
        self.top5: Optional[int] = data.get("top5")
        self.top6: Optional[int] = data.get("top6")
        self.top10: Optional[int] = data.get("top10")
        self.top12: Optional[int] = data.get("top12")
        self.top25: Optional[int] = data.get("top25")

        self.kills: int = data["kills"]
        self.kills_per_min: float = data["killsPerMin"]
        self.kills_per_match: float = data["killsPerMatch"]

        self.deaths: int = data["deaths"]
        self.kd: float = data["kd"]
        self.matches: int = data["matches"]
        self.win_rate: float = data["winRate"]
        self.minutes_played: int = data["minutesPlayed"]
        self.players_outlived: int = data["playersOutlived"]
        self.last_modified: datetime.datetime = parse_time(data["lastModified"])


class BrInputStats(ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.BrInputStats

    Represents a specific Fortnite player's stats for a specific input type.
    This class inherits from :class:`~fortnite_api.ReconstructAble`.

    Attributes
    ----------
    overall: Optional[:class:`BrGameModeStats`]
        The overall stats for the player. This is ``None`` if the overall stats are not available.
    solo: Optional[:class:`BrGameModeStats`]
        The player's stats for solo game modes. This is ``None`` if the player has no stats for solo game modes.
    duo: Optional[:class:`BrGameModeStats`]
        The player's stats for duo game modes. This is ``None`` if the player has no stats for duo game modes.
    squad: Optional[:class:`BrGameModeStats`]
        The player's stats for squad game modes. This is ``None`` if the player has no stats for squad game modes.
    """

    __slots__: tuple[str, ...] = ("overall", "solo", "duo", "squad")

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        _overall = data.get("overall")
        self.overall: Optional[BrGameModeStats[HTTPClientT]] = _overall and BrGameModeStats(data=_overall, http=http)

        _solo = data.get("solo")
        self.solo: Optional[BrGameModeStats[HTTPClientT]] = _solo and BrGameModeStats(data=_solo, http=http)

        _duo = data.get("duo")
        self.duo: Optional[BrGameModeStats[HTTPClientT]] = _duo and BrGameModeStats(data=_duo, http=http)

        _squad = data.get("squad")
        self.squad: Optional[BrGameModeStats[HTTPClientT]] = _squad and BrGameModeStats(data=_squad, http=http)


class BrInputs(ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.BrInputs

    Represents a Fortnite player's stats for all input types. This class inherits
    from :class:`~fortnite_api.ReconstructAble`.

    Each input type has its own stats, which can be accessed through the attributes. Additionally,
    there is an ``all`` attribute which represents the player's stats for all inputs. If the player
    has no stats for a specific input type, the attribute will be ``None``. If the player has no stats
    at all, the ``all`` attribute will be ``None``.

    Attributes
    ----------
    all: Optional[:class:`BrInputStats`]
        The player's stats for all input types. This is ``None`` if the player has no stats.
    keyboard_mouse: Optional[:class:`BrInputStats`]
        The player's stats for keyboard and mouse input. This is ``None`` if the player has no stats.
    gamepad: Optional[:class:`BrInputStats`]
        The player's stats for gamepad input. This is ``None`` if the player has no stats.
    touch: Optional[:class:`BrInputStats`]
        The player's stats for touch input. This is ``None`` if the player has no stats.
    """

    __slots__: tuple[str, ...] = ("all", "keyboard_mouse", "gamepad", "touch")

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        _all = data.get("all")
        self.all: Optional[BrInputStats[HTTPClientT]] = _all and BrInputStats(data=_all, http=http)

        _keyboard_mouse = data.get("keyboardMouse")
        self.keyboard_mouse: Optional[BrInputStats[HTTPClientT]] = _keyboard_mouse and BrInputStats(
            data=_keyboard_mouse, http=http
        )

        _gamepad = data.get("gamepad")
        self.gamepad: Optional[BrInputStats[HTTPClientT]] = _gamepad and BrInputStats(data=_gamepad, http=http)

        _touch = data.get("touch")
        self.touch: Optional[BrInputStats[HTTPClientT]] = _touch and BrInputStats(data=_touch, http=http)


class BrPlayerStats(ReconstructAble[dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.BrPlayerStats

    Represents a Fortnite Battle Royale player's stats. This class
    inherits from :class:`~fortnite_api.ReconstructAble`.


    Examples
    --------
    .. code-block:: python3
        :caption: Fetching a player's total wins in the solo game mode across all input types.

        # It's helpful to compute the data in a helper function, as many attributes
        # will be ``None`` if the player has no stats in a given game mode or input type.
        def get_total_wins(stats: fortnite_api.BrPlayerStats) -> int:
            # Get the stats for all input types.
            all_inputs = stats.inputs and stats.inputs.all
            if all_inputs is None:
                # This player has no stats.
                return 0

            # Get the stats for the solo game mode.
            solo = all_inputs.solo
            if solo is None:
                # This player has never played solos.
                return 0

            # Return the total number of wins in the solo game mode.
            return solo.wins

        # Fetch the player's stats.
        stats = await fortnite_api_client.fetch_br_stats(name="<username>")

        # Compute the total wins.
        total_wins = get_total_wins(stats)

        # And print out the result.
        print(f'{stats.user.name} has {total_wins} total wins in the solo game mode across all platforms.')

    Attributes
    ----------
    user: :class:`fortnite_api.Account`
        The account of the player whose stats are being represented.
    battle_pass: Optional[:class:`fortnite_api.BrBattlePass`]
        The player's battle pass level and progress, if available.
    image: Optional[:class:`fortnite_api.Asset`]
        The requested statistics image, if requested.
    inputs: Optional[:class:`fortnite_api.BrInputs`]
        The player's stats for all input types. This is ``None`` if the player has no stats.
    """

    __slots__: tuple[str, ...] = ("user", "battle_pass", "image", "inputs")

    def __init__(self, *, data: dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        _user = data["account"]
        self.user: Account[HTTPClientT] = Account(data=_user, http=http)

        _battle_pass = data.get("battlePass")
        self.battle_pass: Optional[BrBattlePass[HTTPClientT]] = _battle_pass and BrBattlePass(
            data=_battle_pass, http=http
        )

        _image = data.get("image")
        self.image: Optional[Asset[HTTPClientT]] = _image and Asset(http=http, url=_image)

        _inputs = data.get("stats")
        self.inputs: Optional[BrInputs[HTTPClientT]] = _inputs and BrInputs(data=_inputs, http=http)
