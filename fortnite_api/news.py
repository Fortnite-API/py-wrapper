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

from .abc import Hashable, ReconstructAble
from .asset import Asset
from .http import HTTPClientT
from .utils import get_with_fallback, parse_time, simple_repr

if TYPE_CHECKING:
    import datetime

__all__: Tuple[str, ...] = ("News", "GameModeNews", "NewsMotd", "NewsMessage")


@simple_repr
class News(ReconstructAble[Dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.News

    Represents Game News. This class inherits from :class:`~fortnite_api.ReconstructAble`.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

    Attributes
    -----------
    br: List[:class:`fortnite_api.GameModeNews`]
        A list of Battle Royale news.
    stw: List[:class:`fortnite_api.GameModeNews`]
        A list of Save the World news.
    """

    __slots__: Tuple[str, ...] = (
        "br",
        "stw",
    )

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        _br = data.get("br")
        self.br: Optional[GameModeNews[HTTPClientT]] = _br and GameModeNews(
            data=_br, http=http
        )

        _stw = data.get("stw")
        self.stw: Optional[GameModeNews[HTTPClientT]] = _stw and GameModeNews(
            data=_stw, http=http
        )


@simple_repr
class GameModeNews(ReconstructAble[Dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.GameModeNews

    Represents News of a specific game mode.

    This inherits from :class:`~fortnite_api.ReconstructAble`.

    .. container:: operations

        .. describe:: repr(x)

                Returns a representation of the account in the form of a string.

    Attributes
    ----------
    hash: :class:`str`
        The hash of the news.
    date: :class:`datetime.datetime`
        The date when the news was published.
    image: Optional[:class:`fortnite_api.Asset`]
        The display image of the news, if available.
    motds: List[:class:`fortnite_api.NewsMotd`]
        A list of Message of the Day (MOTD) for the game mode.
    messages: List[:class:`fortnite_api.NewsMessage`]
        A list of messages for the game mode.
    """

    __slots__: Tuple[str, ...] = ("hash", "date", "image", "motds", "messages")

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.hash: str = data["hash"]
        self.date: datetime.datetime = parse_time(data["date"])

        _image = data.get("image")
        self.image: Optional[Asset[HTTPClientT]] = _image and Asset(
            http=http, url=_image
        )

        _motds = get_with_fallback(data, "motds", list)
        self.motds: List[NewsMotd[HTTPClientT]] = [
            NewsMotd(data=motd, http=http) for motd in _motds
        ]

        _messages = get_with_fallback(data, "messages", list)
        self.messages: List[NewsMessage[HTTPClientT]] = [
            NewsMessage(data=message, http=http) for message in _messages
        ]


@simple_repr
class NewsMotd(Hashable, ReconstructAble[Dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.NewsMotd

    Represents News of a specific game mode.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

    Attributes
    -----------
    id: :class:`str`
        The id of the motd.
    title: :class:`str`
        The title of the motd.
    tab_title: :class:`str`
        The tab title of the motd.
    body: Optional[:class:`str`]
        The body of the motd.
    image: :class:`Asset`
        The asset of the image that represents this news.
    title_image: :class:`str`
        The asset of the title image that represents this news.
    hidden: :class:`bool`
        Whether the motd is hidden or not.
    """

    __slots__: Tuple[str, ...] = (
        "id",
        "title",
        "tab_title",
        "body",
        "image",
        "tile_image",
        "sorting_priority",
        "hidden",
    )

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.id: str = data["id"]
        self.title: str = data["title"]
        self.tab_title: str = data["tabTitle"]
        self.body: str = data["body"]

        self.image: Asset[HTTPClientT] = Asset(http=http, url=data["image"])
        self.title_image: Asset[HTTPClientT] = Asset(http=http, url=data["tileImage"])

        self.sorting_priority: int = data["sortingPriority"]
        self.hidden: bool = data["hidden"]


@simple_repr
class NewsMessage(ReconstructAble[Dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.NewsMessage

    Represents News of a specific game mode.

    This inherits from :class:`~fortnite_api.ReconstructAble`.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

    Attributes
    ----------
    title: :class:`str`
        The title of the message.
    body: :class:`str`
        The body contents of the message.
    image: :class:`Asset`
        An image that is associated with the message.
    adspace: Optional[:class:`str`]
        The adspace of the message.
    """

    __slots__: Tuple[str, ...] = ("title", "body", "image", "adspace")

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.title: str = data["title"]
        self.body: str = data["body"]
        self.image: Asset[HTTPClientT] = Asset(http=http, url=data["image"])
        self.adspace: Optional[str] = data.get("adspace")
