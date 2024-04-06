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
from typing import Any, Dict, List, Optional

from ..http import HTTPClientT
from ..utils import get_with_fallback, parse_time
from .common import Cosmetic


class CosmeticTrackDifficulty:
    def __init__(self, *, data: Dict[str, Any]) -> None:
        self.vocals: int = data['vocals']
        self.guitar: int = data['guitar']
        self.bass: int = data['bass']
        self.plastic_bass: int = data['plasticBass']
        self.drums: int = data['drums']
        self.plastic_drums: int = data['plasticDrums']


class CosmeticTrack(Cosmetic[HTTPClientT]):
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
        self.album_art: str = data['albumArt']

        self.shop_history: List[datetime.datetime] = [
            parse_time(time) for time in get_with_fallback(data, 'shopHistory', list)
        ]
