from typing import Any, Dict

import pytest

from fortnite_api import Account


@pytest.fixture
def sample_account_data() -> Dict[str, Any]:
    return {
        'id': '123',
        'name': 'Test Account',
        'external_auths': {'auth1': 'data1', 'auth2': 'data2'},
    }


def test_account_initialization(sample_account_data: Dict[str, Any]):
    account = Account(sample_account_data)

    assert account.id == '123'
    assert account.name == 'Test Account'
    assert account.raw_data == sample_account_data
    assert account.external_auths == {'auth1': 'data1', 'auth2': 'data2'}


def test_account_str(sample_account_data: Dict[str, Any]):
    account = Account(sample_account_data)

    assert str(account) == 'Test Account'


def test_account_repr(sample_account_data: Dict[str, Any]):
    account = Account(sample_account_data)

    assert repr(account) == "<Account id=123 name=Test Account external_auths={'auth1': 'data1', 'auth2': 'data2'}>"
