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

from typing import Tuple, Dict, Any

from .account import Account

__all__: Tuple[str, ...] = ('CreatorCode',)


class CreatorCode:
    """Represents a Creator Code.

    Attributes
    -----------
    user: :class:`User`
        The user of the creator code.
    disabled: :class:`bool`
        Whether the Creator Code is disabled or not.
    code: :class:`str`
        The slug of the Creator Code
    verified: :class:`bool`
        Whether the Creator Code is verified or not.
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    __slots__: Tuple[str, ...] = ('code', 'user', 'disabled', 'verified', 'raw_data')

    def __init__(self, data: Dict[str, Any]) -> None:
        self.code = data.get('code')
        self.user = Account(data.get('account')) if data.get('account') else None
        self.disabled = data.get('status', '').lower() == 'disabled'
        self.verified = data.get('verified', False)
        self.raw_data = data
