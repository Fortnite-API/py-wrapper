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

from .utils import simple_repr

from .account import Account
from .enums import CreatorCodeStatus

__all__: Tuple[str, ...] = ('CreatorCode',)


@simple_repr
class CreatorCode:
    """
    .. attributetable:: fortnite_api.CreatorCode

    Represents a Creator Code.

    .. container:: operations

        .. describe:: repr(x)

            Returns a representation of the account in the form of a string.

    Attributes
    -----------
    code: :class:`str`
        The creator code.
    account: :class:`fortnite_api.Account`
        The account associated with the creator code. Ie, the account
        that owns the creator code.
    status: :class:`fortnite_api.CreatorCodeStatus`
        The current status of the creator code.
    verified: :class:`bool`
        Whether the creator code is verified.

        .. note::

            From internal testing, this seems to be always ``False``.
    raw_data: :class:`dict`
        The raw data of the creator code. This is the data received from the API.
    """

    __slots__: Tuple[str, ...] = ('code', 'account', 'verified', 'status', 'raw_data')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.code: str = data['code']
        self.account: Account = Account(data['account'])
        self.verified: bool = data['verified']
        self.status: CreatorCodeStatus = CreatorCodeStatus(data['status'].lower())
        self.raw_data = data

    @property
    def disabled(self) -> bool:
        """:class:`bool`: Whether the creator code is disabled."""
        return self.status is CreatorCodeStatus.DISABLED
