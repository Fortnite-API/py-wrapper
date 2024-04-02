import requests
import datetime

import fortnite_api as fn_api
from fortnite_api.types.account import Account as AccountPayload

TEST_ACCOUNT_ID = "4735ce9132924caf8a5b17789b40f79c"
TEST_ACCOUNT_NAME = "Ninja"
TEST_CREATOR_CODE = "ninja"


def test_sync_client_initialization():
    with requests.Session() as session, fn_api.SyncFortniteAPI(session=session) as client:
        assert client

    with fn_api.SyncFortniteAPI() as client:
        assert client


def test_sync_aes():
    with fn_api.SyncFortniteAPI() as client:
        aes = client.fetch_aes()

        # Ensure that the AES can be fetched with BASE64
        aes_b64 = client.fetch_aes(key_format=fn_api.KeyFormat.BASE64)

    assert isinstance(aes, fn_api.Aes)
    assert aes.main_key
    assert aes.build
    assert aes.version

    assert aes.updated
    assert isinstance(aes.updated, datetime.datetime)

    assert aes == aes
    assert aes != None

    # Ensure that the AES can be fetched with BASE64
    assert aes_b64.build == aes.build
    assert aes_b64.version == aes.version

    # NOTE: Comparison functions will not account for separate key formats, if the two instances have different values they are deemed unequal. Maybe change this in the future.
    assert aes_b64 != aes


def test_sync_banners():
    with fn_api.SyncFortniteAPI() as client:
        banners = client.fetch_banners()

    for banner in banners:
        assert isinstance(banner, fn_api.Banner)

        assert banner.id
        assert banner.name
        assert banner.dev_name
        assert banner.description
        assert banner.category
        assert banner.full_usage_rights is not None
        # TODO: Banner images tests (not added because of pending Image class implementation)


def test_sync_banner_colors():
    with fn_api.SyncFortniteAPI() as client:
        banner_colors = client.fetch_banner_colors()

    for color in banner_colors:
        assert isinstance(color, fn_api.BannerColor)

        assert color.id
        assert color.color
        assert color.category
        assert color.sub_category_group is not None

    if banner_colors:
        first = banner_colors[0]
        assert first == first

        if len(banner_colors) >= 2:
            assert first != banner_colors[1]


def test_sync_creator_code():

    with fn_api.SyncFortniteAPI() as client:
        creator_code = client.fetch_creator_code(TEST_CREATOR_CODE)

    assert isinstance(creator_code, fn_api.CreatorCode)
    assert creator_code.code == TEST_CREATOR_CODE

    mock_account_payload = AccountPayload(id=TEST_ACCOUNT_ID, name=TEST_ACCOUNT_NAME)
    assert creator_code.account == fn_api.Account(mock_account_payload)

    assert creator_code.status is fn_api.CreatorCodeStatus.ACTIVE
    assert creator_code.disabled is False
    assert creator_code.verified is False
