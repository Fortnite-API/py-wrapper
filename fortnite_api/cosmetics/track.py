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

import datetime
from typing import Any, Dict, List, Optional, Tuple

from ..asset import Asset
from ..http import HTTPClientT
from ..utils import get_with_fallback, parse_time
from .common import Cosmetic

__all__: Tuple[str, ...] = ('CosmeticTrackDifficulty', 'CosmeticTrack')


class CosmeticTrackDifficulty:
    """Represents the difficulty of a track cosmetic in Fortnite.

    Attributes
    ----------
    vocals: :class:`int`
        The vocals difficulty of the track.
    guitar: :class:`int`
        The guitar difficulty of the track.
    bass: :class:`int`
        The bass difficulty of the track.
    plastic_bass: :class:`int`
        The plastic bass difficulty of the track.
    drums: :class:`int`
        The drums difficulty of the track.
    plastic_drums: :class:`int`
        The plastic drums difficulty of the track.
    """

    __slots__: Tuple[str, ...] = ('vocals', 'guitar', 'bass', 'plastic_bass', 'drums', 'plastic_drums')

    def __init__(self, *, data: Dict[str, Any]) -> None:
        self.vocals: int = data['vocals']
        self.guitar: int = data['guitar']
        self.bass: int = data['bass']
        self.plastic_bass: int = data['plasticBass']
        self.drums: int = data['drums']
        self.plastic_drums: int = data['plasticDrums']


class CosmeticTrack(Cosmetic[HTTPClientT]):
    """Represents a track cosmetic in Fortnite.

    This class inherits from :class:`Cosmetic`.

    Attributes
    ----------
    dev_name: :class:`str`
        The developer name of the track.
    title: :class:`str`
        The title of the track.
    artist: :class:`str`
        The artist of the track.
    album: Optional[:class:`str`]
        The album of the track.
    release_year: :class:`int`
        The release year of the track.
    bpm: :class:`int`
        The BPM of the track.
    duration: :class:`int`
        The duration of the track, in seconds.
    difficulty: :class:`CosmeticTrackDifficulty`
        The difficulty of the track.
    gameplay_tags: List[:class:`str`]
        The gameplay tags of the track.
    genres: List[:class:`str`]
        The genres of the track.
    album_art: :class:`Asset`
        The album art of the track.
    shop_history: List[:class:`datetime.datetime`]
        The shop history of the track.
    """

    __slots__: Tuple[str, ...] = (
        'dev_name',
        'title',
        'artist',
        'album',
        'release_year',
        'bpm',
        'duration',
        'difficulty',
        'gameplay_tags',
        'genres',
        'album_art',
        'shop_history',
    )

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.dev_name: str = data['devName']
        self.title: str = data['title']
        self.artist: str = data['artist']
        self.album: Optional[str] = data.get('album')
        self.release_year: int = data['releaseYear']
        self.bpm: int = data['bpm']
        self.duration: int = data['duration']

        self.difficulty: CosmeticTrackDifficulty = CosmeticTrackDifficulty(data=data['difficulty'])
        self.gameplay_tags: List[str] = get_with_fallback(data, 'gameplayTags', list)
        self.genres: List[str] = get_with_fallback(data, 'genres', list)
        self.album_art: Asset[HTTPClientT] = Asset(http=http, url=data['albumArt'])

        self.shop_history: List[datetime.datetime] = [
            parse_time(time) for time in get_with_fallback(data, 'shopHistory', list)
        ]
