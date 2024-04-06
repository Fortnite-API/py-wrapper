from datetime import datetime, timezone
from typing import Any, Dict

import pytest

from fortnite_api.aes import Aes, Version


@pytest.fixture
def sample_aes_data() -> Dict[str, Any]:
    return {
        'mainKey': 'test_main_key',
        'build': '++Fortnite+Release-29.10-CL-32567225-Windows',
        'updated': '2022-01-01T00:00:00Z',
        'dynamicKeys': [
            {
                'pakFilename': 'pak1',
                'pakGuid': 'guid1',
                'key': 'key1',
            }
        ],
    }


def test_aes_initialization(sample_aes_data: Dict[str, Any]):
    aes = Aes(sample_aes_data)

    assert aes.main_key == 'test_main_key'
    assert aes.build == '++Fortnite+Release-29.10-CL-32567225-Windows'
    assert aes.version == Version(29, 10)
    assert aes.updated == datetime(2022, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    assert len(aes.dynamic_keys) == 1
    assert aes.dynamic_keys[0].pak_filename == 'pak1'
    assert aes.dynamic_keys[0].pak_guid == 'guid1'
    assert aes.dynamic_keys[0].key == 'key1'
    assert aes.raw_data == sample_aes_data


def test_aes_equality(sample_aes_data: Dict[str, Any]):
    aes1 = Aes(sample_aes_data)
    aes2 = Aes(sample_aes_data)

    assert aes1 == aes2


def test_aes_inequality(sample_aes_data: Dict[str, Any]):
    aes1 = Aes(sample_aes_data)
    aes2 = Aes(sample_aes_data)
    aes2.main_key = 'different_main_key'

    assert aes1 != aes2
