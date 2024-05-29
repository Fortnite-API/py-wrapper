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

from typing import Any, Dict, Tuple

from .abc import Hashable
from .utils import simple_repr

__all__: Tuple[str, ...] = ('Account',)


@simple_repr
class Account(Hashable):
    """
    .. attributetable:: fortnite_api.Account

    Represents a Fortnite account.

    .. container:: operations

        .. describe:: str(x)

            Returns the account's name.

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

    Attributes
    ----------
    id: :class:`str`
        The id of the account.
    name: :class:`str`
        The display name of the account.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    __slots__: Tuple[str, ...] = (
        'id',
        'name',
        'raw_data',
    )

    def __init__(self, data: Dict[str, Any]) -> None:
        self.id: str = data['id']
        self.name: str = data['name']
        self.raw_data: Dict[str, Any] = data

    def __str__(self) -> str:
        return self.name
