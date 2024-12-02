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

import enum
from typing import Tuple, Type

from typing_extensions import Self

__all__: Tuple[str, ...] = ('ResponseFlags',)


class ResponseFlags(enum.IntFlag):
    """
    .. attributetable:: fortnite_api.ResponseFlags

    Denotes a "response flag" in the Fortnite API. These are toggle-able
    options that denote how a response from the API should be formatted and which
    data should be included.

    Attributes
    ----------
    INCLUDE_NOTHING: :class:`int`
        Include nothing special in the response. This will only include standard
        data in all responses, ie, any data fields in this class prefixed
        with ``INCLUDE_``.
    INCLUDE_PATHS: :class:`int`
        Denotes if the response should include the ``paths`` field in the response,
        if the endpoint contains it.
    INCLUDE_GAMEPLAY_TAGS: :class:`int`
        Denotes if the response should include the ``gameplay_tags`` field in the response,
        if the endpoint contains it.
    INCLUDE_SHOP_HISTORY: :class:`int`
        Denotes if the response should include the ``shop_history`` field in the response,
        if the endpoint contains it.
    """

    INCLUDE_NOTHING = 0
    INCLUDE_PATHS = 1 << 0
    INCLUDE_GAMEPLAY_TAGS = 1 << 1
    INCLUDE_SHOP_HISTORY = 1 << 2

    @classmethod
    def all(cls: Type[Self]) -> Self:
        """:class:`ResponseFlags`: Returns a flag that includes all flags."""
        self = cls.INCLUDE_NOTHING
        for item in cls:
            # If this item is not already included in self, include it
            if not self & item:
                self |= item

        return self
