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

from typing import Dict, Any, Tuple, List

__all__: Tuple[str, ...] = ('Map', 'POI', 'POILocation')


class Map:

    __slots__: Tuple[str, ...] = ('blank_image', 'poi_image', 'pois', 'raw_data')

    def __init__(self, data: Dict[Any, Any]) -> None:
        self.blank_image: str = data['images']['blank']
        self.poi_image: str = data['images']['pois']
        self.pois: List[POI] = [POI(x) for x in data['pois']]
        self.raw_data = data


class POI:

    __slots__: Tuple[str, ...] = ('id', 'name', 'location', 'raw_data')

    def __init__(self, data: Dict[Any, Any]) -> None:
        self.id = data['id']
        self.name = data['name']
        self.location = POILocation(data['location'])
        self.raw_data = data


class POILocation:

    __slots__: Tuple[str, ...] = ('x', 'y', 'z', 'raw_data')

    def __init__(self, data: Dict[Any, Any]) -> None:
        self.x: int = data['x']
        self.y: int = data['y']
        self.z: int = data['z']
        self.raw_data: Dict[Any, Any] = data
