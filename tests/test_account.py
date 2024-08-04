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

from typing import Any, Dict

import pytest

from fortnite_api import Account
from fortnite_api.http import HTTPClient


@pytest.fixture
def sample_account_data() -> Dict[str, Any]:
    return {
        'id': '123',
        'name': 'Test Account',
    }


def test_account_initialization(sample_account_data: Dict[str, Any]):
    account = Account(data=sample_account_data, http=HTTPClient())

    assert account.id == '123'
    assert account.name == 'Test Account'
    assert account.to_dict() == sample_account_data


def test_account_str(sample_account_data: Dict[str, Any]):
    account = Account(data=sample_account_data, http=HTTPClient())

    assert str(account) == 'Test Account'


def test_account_repr(sample_account_data: Dict[str, Any]):
    account = Account(data=sample_account_data, http=HTTPClient())

    assert repr(account) == "<Account id='123', name='Test Account'>"
