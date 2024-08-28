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

from typing import Any, Dict, Optional, Tuple

from .abc import ReconstructAble
from .asset import Asset
from .http import HTTPClientT
from .utils import simple_repr

__all__: Tuple[str, ...] = ('Images',)


@simple_repr
class Images(ReconstructAble[Dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.Images

    Represents image data passed from the API. This class is used to represent
    commonly provided assets for many API endpoints and object types.

    This inherits from :class:`~fortnite_api.ReconstructAble`.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

    Attributes
    ----------
    small_icon: Optional[:class:`fortnite_api.Asset`]
        A smaller icon asset. Typically, this is a smaller version of the main image.
    icon: Optional[:class:`fortnite_api.Asset`]
        An icon asset. Typically, this is the main image of the object.
    """

    __slots__: Tuple[str, ...] = ('small_icon', 'icon')

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        small_icon = data.get('smallIcon')
        self.small_icon: Optional[Asset[HTTPClientT]] = small_icon and Asset(http=http, url=small_icon)

        icon = data.get('icon')
        self.icon: Optional[Asset[HTTPClientT]] = icon and Asset(http=http, url=icon)
