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

import datetime

import pytest

import fortnite_api as fn_api
from fortnite_api.http import SyncHTTPClient

from .conftest import TEST_ACCOUNT_ID, TEST_ACCOUNT_NAME, TEST_COSMETIC_ID, TEST_CREATOR_CODE, TEST_DEFAULT_PLAYLIST
from .test_async_methods import _test_game_mode_news, _test_playlist


def test_sync_aes(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        aes = client.fetch_aes()

        # Ensure that the AES can be fetched with BASE64
        aes_b64 = client.fetch_aes(key_format=fn_api.KeyFormat.BASE64)

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


def test_sync_banners(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        banners = client.fetch_banners()

    for banner in banners:
        assert isinstance(banner, fn_api.Banner)

        assert banner.id
        assert banner.name
        assert banner.dev_name
        assert banner.description
        assert banner.full_usage_rights is not None

        assert isinstance(banner.images, fn_api.Images)

        small = banner.images.small_icon
        if small is not None:
            assert small.url == banner.to_dict()['images']['smallIcon']

        icon = banner.images.icon
        if icon is not None:
            assert icon.url == banner.to_dict()['images']['icon']


def test_sync_banner_colors(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
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


def test_sync_creator_code(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        creator_code = client.fetch_creator_code(name=TEST_CREATOR_CODE)

    assert isinstance(creator_code, fn_api.CreatorCode)
    assert creator_code.code == TEST_CREATOR_CODE

    mock_account_payload = dict(id=TEST_ACCOUNT_ID, name=TEST_ACCOUNT_NAME)
    assert creator_code.account == fn_api.Account(data=mock_account_payload, http=SyncHTTPClient())

    assert creator_code.status is fn_api.CreatorCodeStatus.ACTIVE
    assert creator_code.disabled is False
    assert creator_code.verified is False


def test_sync_fetch_playlist(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        playlists = client.fetch_playlists()

    assert len(playlists), "Playlists should not be empty"

    first = playlists[0]
    assert first == first

    if len(playlists) >= 2:
        assert first != playlists[1]


def test_sync_fetch_cosmetics_cars(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        cosmetics_cars = client.fetch_cosmetics_cars()

    for cosmetic in cosmetics_cars:
        assert isinstance(cosmetic, fn_api.CosmeticCar)


def test_sync_fetch_cosmetics_instruments(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        cosmetics_instruments = client.fetch_cosmetics_instruments()

    for cosmetic in cosmetics_instruments:
        assert isinstance(cosmetic, fn_api.CosmeticInstrument)


def test_sync_fetch_cosmetics_lego_kits(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        lego_kits = client.fetch_cosmetics_lego_kits()

    for kit in lego_kits:
        assert isinstance(kit, fn_api.CosmeticLegoKit)


def test_sync_fetch_variants_lego(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        variants_lego = client.fetch_variants_lego()

    for variant in variants_lego:
        assert isinstance(variant, fn_api.VariantLego)


def test_sync_fetch_variants_beans(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        variants_beans = client.fetch_variants_beans()

    for variant in variants_beans:
        assert isinstance(variant, fn_api.VariantBean)


def test_sync_fetch_cosmetics_tracks(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        cosmetics_tracks = client.fetch_cosmetics_tracks()

    for cosmetic in cosmetics_tracks:
        assert isinstance(cosmetic, fn_api.CosmeticTrack)


def test_sync_fetch_cosmetics_br(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        cosmetics_br = client.fetch_cosmetics_br()

    for cosmetic in cosmetics_br:
        assert isinstance(cosmetic, fn_api.CosmeticBr)


def test_sync_fetch_cosmetic_br(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        cosmetic_br = client.fetch_cosmetic_br(TEST_COSMETIC_ID)

    assert isinstance(cosmetic_br, fn_api.CosmeticBr)
    assert cosmetic_br.id == TEST_COSMETIC_ID


def test_sync_fetch_cosmetics_new(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        new_cosmetics = client.fetch_cosmetics_new()

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


def test_sync_fetch_cosmetics_all(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        cosmetics_all = client.fetch_cosmetics_all()

    assert isinstance(cosmetics_all, fn_api.CosmeticsAll)

    assert cosmetics_all.br
    assert cosmetics_all.tracks
    assert cosmetics_all.instruments
    assert cosmetics_all.cars
    assert cosmetics_all.lego
    assert cosmetics_all.lego_kits
    assert cosmetics_all.to_dict()

    # Ensure that you can iter over the cosmetics
    assert len(cosmetics_all) != 0
    for cosmetic in cosmetics_all:
        assert isinstance(cosmetic, fn_api.Cosmetic)


def test_sync_map(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        map = client.fetch_map()

    assert isinstance(map, fn_api.Map)
    assert isinstance(map.images, fn_api.MapImages)

    assert map.images.blank
    assert map.images.pois

    assert map.pois

    for poi in map.pois:
        assert isinstance(poi, fn_api.POI)
        assert poi.id
        assert isinstance(poi.location, fn_api.POILocation)


def test_fetch_news(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        news = client.fetch_news()

    assert isinstance(news, fn_api.News)
    assert news.to_dict()


def test_fetch_news_methods(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        news_br = client.fetch_news_br()
        news_stw = client.fetch_news_stw()

    assert isinstance(news_stw, fn_api.GameModeNews)
    _test_game_mode_news(news_br)

    assert isinstance(news_stw, fn_api.GameModeNews)
    _test_game_mode_news(news_stw)


def test_sync_fetch_playlists(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        playlists = client.fetch_playlists()

    for playlist in playlists:
        _test_playlist(playlist)


def test_sync_fetch_playlist_by_id(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        playlist = client.fetch_playlist(TEST_DEFAULT_PLAYLIST)

    assert playlist.id == TEST_DEFAULT_PLAYLIST
    _test_playlist(playlist)


def test_sync_beta_fetch_material_instances(api_key: str):
    # Ensure you cannot call this without beta=True
    with pytest.raises(fn_api.BetaAccessNotEnabled):
        fn_api.SyncClient().beta_fetch_material_instances()

    with fn_api.SyncClient(beta=True, api_key=api_key) as client:
        material_instances = client.beta_fetch_material_instances()

    for instance in material_instances:
        assert isinstance(instance, fn_api.MaterialInstance)

        assert instance.id
        assert instance.primary_mode

        # Walk through all the images and ensure they are assets
        for name, asset in instance.images.items():
            assert isinstance(name, str)
            assert isinstance(asset, fn_api.Asset)

        assert instance == instance


def test_sync_fetch_shop(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        shop = client.fetch_shop()

    assert isinstance(shop, fn_api.Shop)

    if not shop.entries:
        return

    for entry in shop.entries:
        # Ensure len(entry) works
        assert isinstance(len(entry), int)

        # Ensure you can iterate over the entry
        for cosmetic in entry:
            assert cosmetic.id

        assert isinstance(entry, fn_api.ShopEntry)
        assert isinstance(entry.regular_price, int)
        assert isinstance(entry.final_price, int)
        assert entry.in_date
        assert entry.out_date

        tile_size = entry.tile_size
        assert isinstance(tile_size, fn_api.TileSize)
        assert tile_size.internal == f'Size_{tile_size.width}_x_{tile_size.height}'

        bundle = entry.bundle
        if bundle:
            assert isinstance(entry.bundle, fn_api.ShopEntryBundle)
            assert bundle.name
            assert bundle.info
            assert bundle.image

        banner = entry.banner
        if banner:
            assert banner.value
            assert banner.intensity
            assert banner.backend_value

        assert isinstance(entry.giftable, bool)
        assert isinstance(entry.refundable, bool)
        assert isinstance(entry.sort_priority, int)
        assert isinstance(entry.layout_id, str)

        layout = entry.layout
        if layout:
            assert isinstance(layout, fn_api.ShopEntryLayout)
            assert layout.id
            assert layout.name
            assert isinstance(layout.index, int)
            assert layout.show_ineligible_offers

        assert entry.dev_name
        assert entry.offer_id
        assert entry.tile_size

        new_display_asset = entry.new_display_asset
        if new_display_asset:
            assert isinstance(new_display_asset, fn_api.ShopEntryNewDisplayAsset)
            assert new_display_asset.id

            for material_instance in new_display_asset.material_instances:
                assert isinstance(material_instance, fn_api.MaterialInstance)

        for cosmetic in entry.br + entry.tracks + entry.instruments + entry.cars + entry.lego_kits:
            assert isinstance(cosmetic, fn_api.Cosmetic)


def test_sync_search_cosmetics(api_key: str):
    with fn_api.SyncClient(api_key=api_key) as client:
        cosmetics_multiple_set = client.search_br_cosmetics(multiple=True, has_set=True)
        cosmetic_single_set = client.search_br_cosmetics(multiple=False, has_set=True)

    assert isinstance(cosmetics_multiple_set, list)
    for cosmetic in cosmetics_multiple_set:
        assert cosmetic.set is not None

    assert isinstance(cosmetic_single_set, fn_api.CosmeticBr)
    assert cosmetic_single_set.set is not None
