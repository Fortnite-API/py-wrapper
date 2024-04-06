import datetime

import aiohttp
import pytest

import fortnite_api as fn_api

TEST_ACCOUNT_ID = "4735ce9132924caf8a5b17789b40f79c"
TEST_ACCOUNT_NAME = "Ninja"
TEST_CREATOR_CODE = "ninja"
TEST_COSMETIC_ID = "Backpack_BrakePedal"


@pytest.mark.asyncio
async def test_async_client_initialization():
    async with aiohttp.ClientSession() as session, fn_api.FortniteAPI(session=session) as client:
        assert client

    assert session.closed == True, "Session should be closed after client is closed"

    async with fn_api.FortniteAPI() as client:
        assert client

    client_session = client.http.session
    assert client_session and client_session.closed


@pytest.mark.asyncio
async def test_async_aes():
    async with fn_api.FortniteAPI() as client:
        aes = await client.fetch_aes()

        # Ensure that the AES can be fetched with BASE64
        aes_b64 = await client.fetch_aes(key_format=fn_api.KeyFormat.BASE64)

    assert isinstance(aes, fn_api.Aes)
    assert aes.main_key
    assert aes.build
    assert aes.version

    assert aes.updated
    assert isinstance(aes.updated, datetime.datetime)

    assert aes != None

    # Ensure that the AES can be fetched with BASE64
    assert aes_b64.build == aes.build
    assert aes_b64.version == aes.version

    # NOTE: Comparison functions will not account for separate key formats, if the two instances have different values they are deemed unequal. Maybe change this in the future.
    assert aes_b64 != aes


@pytest.mark.asyncio
async def test_async_banners():
    async with fn_api.FortniteAPI() as client:
        banners = await client.fetch_banners()

    for banner in banners:
        assert isinstance(banner, fn_api.Banner)

        assert banner.id
        assert banner.name
        assert banner.dev_name
        assert banner.description
        assert banner.category
        assert banner.full_usage_rights is not None
        # TODO: Banner images tests (not added because of pending Images class implementation)


@pytest.mark.asyncio
async def test_async_banner_colors():
    async with fn_api.FortniteAPI() as client:
        banner_colors = await client.fetch_banner_colors()

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


@pytest.mark.asyncio
async def test_async_creator_code():
    async with fn_api.FortniteAPI() as client:
        creator_code = await client.fetch_creator_code(name=TEST_CREATOR_CODE)

    assert isinstance(creator_code, fn_api.CreatorCode)
    assert creator_code.code == TEST_CREATOR_CODE

    mock_account_payload = dict(id=TEST_ACCOUNT_ID, name=TEST_ACCOUNT_NAME)
    assert creator_code.account == fn_api.Account(mock_account_payload)

    assert creator_code.status is fn_api.CreatorCodeStatus.ACTIVE
    assert creator_code.disabled is False
    assert creator_code.verified is False


@pytest.mark.asyncio
async def test_async_fetch_playlist():
    async with fn_api.FortniteAPI() as client:
        playlists = await client.fetch_playlists()
        playlists_en = await client.fetch_playlists()

    assert len(playlists), "Playlists should not be empty"

    first = playlists[0]
    assert first == first

    if len(playlists) >= 2:
        assert first != playlists[1]

    assert playlists == playlists_en


@pytest.mark.asyncio
async def test_async_fetch_cosmetics_br():
    async with fn_api.FortniteAPI() as client:
        cosmetics_br = await client.fetch_cosmetics_br()

    for cosmetic in cosmetics_br:
        assert isinstance(cosmetic, fn_api.CosmeticBr)


@pytest.mark.asyncio
async def test_async_fetch_cosmetics_cars():
    async with fn_api.FortniteAPI() as client:
        cosmetics_cars = await client.fetch_cosmetics_cars()

    for cosmetic in cosmetics_cars:
        assert isinstance(cosmetic, fn_api.CosmeticCar)


@pytest.mark.asyncio
async def test_async_fetch_cosmetics_instruments():
    async with fn_api.FortniteAPI() as client:
        cosmetics_instruments = await client.fetch_cosmetics_instruments()

    for cosmetic in cosmetics_instruments:
        assert isinstance(cosmetic, fn_api.CosmeticInstrument)


@pytest.mark.asyncio
async def test_async_fetch_cosmetics_lego_kits():
    async with fn_api.FortniteAPI() as client:
        lego_kits = await client.fetch_cosmetics_lego_kits()

    for kit in lego_kits:
        assert isinstance(kit, fn_api.CosmeticLegoKit)


@pytest.mark.asyncio
async def test_async_fetch_cosmetics_lego():
    async with fn_api.FortniteAPI() as client:
        lego = await client.fetch_cosmetics_lego()

    for lego in lego:
        assert isinstance(lego, fn_api.CosmeticLego)


@pytest.mark.asyncio
async def test_async_fetch_cosmetics_tracks():
    async with fn_api.FortniteAPI() as client:
        cosmetics_tracks = await client.fetch_cosmetics_tracks()

    for cosmetic in cosmetics_tracks:
        assert isinstance(cosmetic, fn_api.CosmeticTrack)


@pytest.mark.asyncio
async def test_async_fetch_cosmetic_br():
    async with fn_api.FortniteAPI() as client:
        cosmetic_br = await client.fetch_cosmetic_br(TEST_COSMETIC_ID)

    assert isinstance(cosmetic_br, fn_api.CosmeticBr)
    assert cosmetic_br.id == TEST_COSMETIC_ID


@pytest.mark.asyncio
async def test_async_fetch_cosmetics_br_new():
    async with fn_api.FortniteAPI() as client:
        new_cosmetics_br = await client.fetch_cosmetics_br_new()

    assert isinstance(new_cosmetics_br, fn_api.NewBrCosmetics)

    assert isinstance(new_cosmetics_br.date, datetime.datetime)
    assert new_cosmetics_br.build
    assert new_cosmetics_br.previous_build


@pytest.mark.asyncio
async def test_async_fetch_cosmetics_new():
    async with fn_api.FortniteAPI() as client:
        new_cosmetics = await client.fetch_cosmetics_new()

    assert isinstance(new_cosmetics, fn_api.NewCosmetics)

    assert new_cosmetics.global_hash
    assert new_cosmetics.date
    assert new_cosmetics.global_last_addition
    assert new_cosmetics.build
    assert new_cosmetics.previous_build

    assert isinstance(new_cosmetics.br, fn_api.NewCosmetic)
    assert isinstance(new_cosmetics.tracks, fn_api.NewCosmetic)
    assert isinstance(new_cosmetics.instruments, fn_api.NewCosmetic)
    assert isinstance(new_cosmetics.cars, fn_api.NewCosmetic)
    assert isinstance(new_cosmetics.lego, fn_api.NewCosmetic)
    assert isinstance(new_cosmetics.lego_kits, fn_api.NewCosmetic)


@pytest.mark.asyncio
async def test_async_fetch_cosmetics_all():
    async with fn_api.FortniteAPI() as client:
        cosmetics_all = await client.fetch_cosmetics_all()

    assert isinstance(cosmetics_all, fn_api.CosmeticsAll)

    assert cosmetics_all.br
    assert cosmetics_all.tracks
    assert cosmetics_all.instruments
    assert cosmetics_all.cars
    assert cosmetics_all.lego
    assert cosmetics_all.lego_kits
    assert cosmetics_all.raw_data
