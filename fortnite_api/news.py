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

from typing import TYPE_CHECKING, Any, Dict, Generic, List, Optional, Tuple

from .asset import Asset

from .http import HTTPClientT

from .abc import Hashable
from .utils import get_with_fallback, parse_time

if TYPE_CHECKING:
    import datetime

__all__: Tuple[str, ...] = ('News', 'GameModeNews', 'NewsMotd', 'NewsMessage')


class News(Generic[HTTPClientT]):
    """Represents Game News.

    Attributes
    -----------
    br: List[:class:`GameModeNews`]
        A list of Battle Royale news.
    stw: List[:class:`GameModeNews`]
        A list of Save the World news.
    creative: List[:class:`GameModeNews`]
        A list of Creative news.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    __slots__: Tuple[str, ...] = ('br', 'stw', 'creative', 'raw_data')

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        _br = data.get('br')
        self.br: Optional[GameModeNews[HTTPClientT]] = _br and GameModeNews(data=_br, http=http)

        _stw = data.get('stw')
        self.stw: Optional[GameModeNews[HTTPClientT]] = _stw and GameModeNews(data=_stw, http=http)

        _creative = data.get('creative')
        self.creative: Optional[GameModeNews[HTTPClientT]] = _creative and GameModeNews(data=_creative, http=http)

        self.raw_data: Dict[str, Any] = data


class GameModeNews(Generic[HTTPClientT]):
    """Represents News of a specific game mode.

    Attributes
    ----------
    hash: :class:`str`
        The hash of the news.
    date: :class:`datetime.datetime`
        The date when the news was published.
    image: Optional[:class:`Asset`]
        The display image of the news, if available.
    motds: List[:class:`NewsMotd`]
        A list of Message of the Day (MOTD) for the game mode.
    messages: List[:class:`NewsMessage`]
        A list of messages for the game mode.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    __slots__: Tuple[str, ...] = ('hash', 'date', 'image', 'motds', 'messages', 'raw_data')

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.hash: str = data['hash']
        self.date: datetime.datetime = parse_time(data['date'])

        _image = data.get('image')
        self.image: Optional[Asset[HTTPClientT]] = _image and Asset(http=http, url=_image)

        _motds = get_with_fallback(data, 'motds', list)
        self.motds: List[NewsMotd[HTTPClientT]] = [NewsMotd(data=motd, http=http) for motd in _motds]

        _messages = get_with_fallback(data, 'messages', list)
        self.messages: List[NewsMessage[HTTPClientT]] = [NewsMessage(data=message, http=http) for message in _messages]

        self.raw_data: Dict[str, Any] = data


class NewsMotd(Hashable, Generic[HTTPClientT]):
    """Represents News of a specific game mode.

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
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    __slots__: Tuple[str, ...] = (
        'id',
        'title',
        'tab_title',
        'body',
        'image',
        'tile_image',
        'sorting_priority',
        'hidden',
        'raw_data',
    )

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.id: str = data['id']
        self.title: str = data['title']
        self.tab_title: str = data['tabTitle']
        self.body: str = data['body']

        self.image: Asset[HTTPClientT] = Asset(http=http, url=data['image'])
        self.title_image: Asset[HTTPClientT] = Asset(http=http, url=data['tileImage'])

        self.sorting_priority: int = data['sortingPriority']
        self.hidden: bool = data['hidden']

        self.raw_data: Dict[str, Any] = data


class NewsMessage(Generic[HTTPClientT]):
    """Represents News of a specific game mode.

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

    __slots__: Tuple[str, ...] = ('title', 'body', 'image', 'adspace', 'raw_data')

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self.title: str = data['title']
        self.body: str = data['body']
        self.image: Asset[HTTPClientT] = Asset(http=http, url=data['image'])
        self.adspace: Optional[str] = data['adspace']
