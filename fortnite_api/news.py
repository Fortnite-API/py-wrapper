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

from typing import TYPE_CHECKING, Dict, Any, Optional, List, Tuple

from .utils import parse_time
from .abc import IdComparable

if TYPE_CHECKING:
    import datetime


class News:
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

    def __init__(self, data: Dict[Any, Any]) -> None:
        self.br: Optional[GameModeNews] = GameModeNews(entry) if (entry := data.get('br')) else None
        self.stw: Optional[GameModeNews] = GameModeNews(entry) if (entry := data.get('stw')) else None
        self.creative: Optional[GameModeNews] = GameModeNews(entry) if (entry := data.get('creative')) else None
        self.raw_data: Dict[Any, Any] = data


class GameModeNews:
    """Represents News of a specific game mode.

    Attributes
    -----------
    last_modified: :class:`datetime.datetime`
        The timestamp when the news where modified.
    entries: List[:class:`NewsEntry`]
        A list of news entries.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    __slots__: Tuple[str, ...] = ('hash', 'date', 'image', 'motds', 'messages', 'raw_data')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.hash = data.get('hash')

        self.date: Optional[datetime.datetime] = parse_time(date) if (date := data.get('date')) else None
        self.image: Optional[str] = data.get('image')
        self.motds: List[NewsMotd] = [NewsMotd(item_data) for item_data in data.get('motds', [])]
        self.messages: List[NewsMessage] = [NewsMessage(item_data) for item_data in data.get('messages', [])]
        self.raw_data: Dict[str, Any] = data


class NewsMotd(IdComparable):
    """Represents News of a specific game mode.

    Attributes
    -----------
    id: :class:`str`
        The id of the motd.
    title: :class:`str`
        The title of the motd.
    body: Optional[:class:`str`]
        The body of the motd.
    image_url: :class:`str`
        The url of the image in 1920x1080.
    tile_image_url: :class:`str`
        The url of the tile image in 1024x512.
    hidden: :class:`bool`
        Whether the motd is hidden.
    spotlight: :class:`bool`
        Whether the motd is in spotlight.
    type: :class:`str`
        The type of the entry.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    __slots__: Tuple[str, ...] = ('id', 'title', 'body', 'image_url', 'tile_image_url', 'sorting_priority', 'raw_data')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.id: str = data['id']
        self.title: str = data['title']
        self.body: str = data['body']
        self.image_url: str = data['image']
        self.tile_image_url: str = data['tileImage']
        self.sorting_priority: int = data['sortingPriority']
        self.raw_data: Dict[str, Any] = data


class NewsMessage:
    """Represents News of a specific game mode.

    Attributes
    -----------
    image_url: :class:`str`
        The url of the image.
    hidden: :class:`bool`
        Whether the entry is hidden.
    message_type: Optional[:class:`str`]
        The type of the message.
    type: :class:`str`
        The type of the entry.
    banner: :class:`str`
        The banner of the entry.
    title: :class:`str`
        The title of the entry.
    body: :class:`str`
        The body of the entry.
    spotlight: :class:`bool`
        Whether the entry is in spotlight.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    __slots__: Tuple[str, ...] = ('title', 'body', 'image_url', 'hidden', 'adspace', 'raw_data')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.title: str = data['title']
        self.body: str = data['body']
        self.image_url: str = data['image']
        self.adspace: str = data['adspace']
        self.raw_data: Dict[str, Any] = data
