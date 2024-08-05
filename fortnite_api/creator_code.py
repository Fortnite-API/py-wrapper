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

from .abc import ReconstructAble
from .account import Account
from .enums import CreatorCodeStatus
from .http import HTTPClientT
from .utils import simple_repr

__all__: Tuple[str, ...] = ("CreatorCode",)


@simple_repr
class CreatorCode(ReconstructAble[Dict[str, Any], HTTPClientT]):
    """
    .. attributetable:: fortnite_api.CreatorCode

    Represents a Creator Code.

    This inherits from :class:`~fortnite_api.ReconstructAble`.

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
    """

    __slots__: Tuple[str, ...] = ("code", "account", "verified", "status")

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        super().__init__(data=data, http=http)

        self.code: str = data["code"]
        self.account: Account[HTTPClientT] = Account(data=data["account"], http=http)
        self.verified: bool = data["verified"]
        self.status: CreatorCodeStatus = CreatorCodeStatus(data["status"].lower())

    @property
    def disabled(self) -> bool:
        """:class:`bool`: Whether the creator code is disabled."""
        return self.status is CreatorCodeStatus.DISABLED
