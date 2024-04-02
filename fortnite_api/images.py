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

from typing import TYPE_CHECKING, Dict, Any, Optional, Tuple
from .asset import SyncAsset, Asset

if TYPE_CHECKING:
    from .http import HTTPClient, SyncHTTPClient

__all__: Tuple[str, ...] = ('Image', 'SyncImage')


class Image:
    """Represents image data passed from the API.

    Attributes
    ----------
    small_icon: Optional[:class:`Asset`]
        The small icon of the image.
    icon: Optional[:class:`Asset`]
        The icon of the image.
    """

    __slots__: Tuple[str, ...] = ('small_icon', 'icon')

    def __init__(self, http: HTTPClient, data: Dict[str, Any]) -> None:
        self.small_icon: Optional[Asset] = (small_icon := data.get('smallIcon')) and Asset(http, small_icon)
        self.icon: Optional[Asset] = (icon := data.get('icon')) and Asset(http, icon)


class SyncImage:
    """Represents image data passed from the API.

    Attributes
    ----------
    small_icon: Optional[:class:`SyncAsset`]
        The small icon of the image.
    icon: Optional[:class:`SyncAsset`]
        The icon of the image.
    """

    __slots__: Tuple[str, ...] = ('small_icon', 'icon')

    def __init__(self, http: SyncHTTPClient, data: Dict[str, Any]) -> None:
        self.small_icon: Optional[SyncAsset] = (small_icon := data.get('smallIcon')) and SyncAsset(http, small_icon)
        self.icon: Optional[SyncAsset] = (icon := data.get('icon')) and SyncAsset(http, icon)
