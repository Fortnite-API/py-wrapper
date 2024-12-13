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
from collections.abc import Callable
from typing import Any

import pytest

import fortnite_api
from fortnite_api.http import HTTPClient

from .conftest import (
    TEST_ACCOUNT_ID,
    TEST_ACCOUNT_NAME,
    TEST_CREATOR_CODE,
    TEST_INVALID_CREATOR_CODE,
    TEST_INVALID_PLAYLIST_ID,
    TEST_PLAYLIST_ID,
)
from .cosmetics.cosmetic_utils import test_cosmetic_br, test_cosmetic_car, test_cosmetic_instrument, test_cosmetic_lego_kit
from .client.test_client_hybrid import ClientHybrid


@pytest.mark.asyncio
async def test_aes(api_key: str):
    async with ClientHybrid(api_key=api_key) as client:
        aes = await client.fetch_aes()

        # Ensure that the AES can be fetched with BASE64
        aes_b64 = await client.fetch_aes(key_format=fortnite_api.KeyFormat.BASE64)

    assert isinstance(aes, fortnite_api.Aes)
    assert aes.main_key
    assert aes.build
    assert aes.version

    assert aes.updated
    assert isinstance(aes.updated, datetime.datetime)

    assert aes is not None

    # Ensure that the AES can be fetched with BASE64
    assert aes_b64.build == aes.build
    assert aes_b64.version == aes.version

    # NOTE: Comparison functions will not account for separate key formats, if the two instances have different values they are deemed unequal. Maybe change this in the future.
    assert aes_b64 != aes


@pytest.mark.asyncio
async def test_banners(api_key: str):
    async with ClientHybrid(api_key=api_key) as client:
        banners = await client.fetch_banners()

    for banner in banners:
        assert isinstance(banner, fortnite_api.Banner)

        assert banner.id
        assert banner.name
        assert banner.dev_name
        assert banner.description
        assert banner.full_usage_rights is not None

        small = banner.images.small_icon
        if small is not None:
            assert small.url == banner.to_dict()['images']['smallIcon']

        icon = banner.images.icon
        if icon is not None:
            assert icon.url == banner.to_dict()['images']['icon']


@pytest.mark.asyncio
async def test_banner_colors(api_key: str):
    async with ClientHybrid(api_key=api_key) as client:
        banner_colors = await client.fetch_banner_colors()

    for color in banner_colors:
        assert isinstance(color, fortnite_api.BannerColor)

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
async def test_creator_code(api_key: str):
    async with ClientHybrid(api_key=api_key) as client:
        with pytest.raises(fortnite_api.NotFound):
            await client.fetch_creator_code(name=TEST_INVALID_CREATOR_CODE)
        creator_code = await client.fetch_creator_code(name=TEST_CREATOR_CODE)

    assert isinstance(creator_code, fortnite_api.CreatorCode)
    assert creator_code.code == TEST_CREATOR_CODE

    mock_account_payload = dict(id=TEST_ACCOUNT_ID, name=TEST_ACCOUNT_NAME)
    assert creator_code.account == fortnite_api.Account(data=mock_account_payload, http=HTTPClient())

    assert creator_code.status is fortnite_api.CreatorCodeStatus.ACTIVE
    assert creator_code.disabled is False
    assert creator_code.verified is False


@pytest.mark.asyncio
async def test_fetch_playlist(api_key: str):
    async with ClientHybrid(api_key=api_key) as client:
        playlists = await client.fetch_playlists()

    assert len(playlists), "Playlists should not be empty"

    first = playlists[0]
    assert first == first

    if len(playlists) >= 2:
        assert first != playlists[1]


@pytest.mark.asyncio
async def test_map(api_key: str):
    async with ClientHybrid(api_key=api_key) as client:
        _map = await client.fetch_map()

    assert isinstance(_map, fortnite_api.Map)
    assert isinstance(_map.images, fortnite_api.MapImages)

    assert _map.images.blank
    assert _map.images.pois

    assert _map.pois

    for poi in _map.pois:
        assert isinstance(poi, fortnite_api.POI)
        assert poi.id
        assert isinstance(poi.location, fortnite_api.POILocation)


@pytest.mark.asyncio
async def test_fetch_news(api_key: str):
    async with ClientHybrid(api_key=api_key) as client:
        news = await client.fetch_news()

    assert isinstance(news, fortnite_api.News)
    assert news.to_dict()


def _test_game_mode_news(news: fortnite_api.GameModeNews[Any]):
    assert news.hash
    assert news.date

    if news.image:
        assert isinstance(news.image, fortnite_api.Asset)

    for motd in news.motds:
        assert isinstance(motd, fortnite_api.NewsMotd)
        assert motd.id
        assert motd.title
        assert motd.tab_title
        assert motd.body

        assert motd.image
        assert isinstance(motd.image, fortnite_api.Asset)

        assert motd.title_image
        assert isinstance(motd.title_image, fortnite_api.Asset)

        assert motd.sorting_priority

    for message in news.messages:
        assert isinstance(message, fortnite_api.NewsMessage)
        assert message.title
        assert message.body

        assert isinstance(message.image, fortnite_api.Asset)


@pytest.mark.asyncio
async def test_fetch_news_methods(api_key: str):
    async with ClientHybrid(api_key=api_key) as client:
        try:
            news_br = await client.fetch_news_br()
            assert isinstance(news_br, fortnite_api.GameModeNews)
            _test_game_mode_news(news_br)
        except fortnite_api.NotFound:
            pass

        try:
            news_stw = await client.fetch_news_stw()
            assert isinstance(news_stw, fortnite_api.GameModeNews)
            _test_game_mode_news(news_stw)
        except fortnite_api.NotFound:
            pass


def _test_playlist(playlist: fortnite_api.Playlist[Any]):
    assert isinstance(playlist, fortnite_api.Playlist)
    assert playlist.name
    assert playlist.min_players
    assert playlist.max_players
    assert playlist.max_teams
    assert playlist.max_team_size
    assert playlist.max_squads
    assert playlist.max_squad_size
    assert isinstance(playlist.is_default, bool)
    assert isinstance(playlist.is_tournament, bool)
    assert isinstance(playlist.is_limited_time_mode, bool)
    assert isinstance(playlist.is_large_team_game, bool)
    assert isinstance(playlist.accumulate_to_profile_stats, bool)

    images = playlist.images
    if images:
        assert isinstance(images, fortnite_api.PlaylistImages)

    assert playlist.path
    assert playlist.added

    assert playlist == playlist


@pytest.mark.asyncio
async def test_fetch_playlists(api_key: str):
    async with ClientHybrid(api_key=api_key) as client:
        playlists = await client.fetch_playlists()

    for playlist in playlists:
        _test_playlist(playlist)


@pytest.mark.asyncio
async def test_fetch_playlist_by_id(api_key: str):
    async with ClientHybrid(api_key=api_key) as client:
        with pytest.raises(fortnite_api.NotFound):
            await client.fetch_playlist(TEST_INVALID_PLAYLIST_ID)
        playlist = await client.fetch_playlist(TEST_PLAYLIST_ID)

    assert playlist.id == TEST_PLAYLIST_ID
    _test_playlist(playlist)


@pytest.mark.asyncio
async def test_beta_fetch_new_display_assets(api_key: str):

    # Ensure you cannot call this without beta=True
    with pytest.raises(fortnite_api.BetaAccessNotEnabled):
        await ClientHybrid().beta_fetch_new_display_assets()

    async with ClientHybrid(beta=True, api_key=api_key) as client:
        new_display_assets = await client.beta_fetch_new_display_assets()

    for new_display_asset in new_display_assets:
        assert isinstance(new_display_asset, fortnite_api.NewDisplayAsset)

        assert new_display_asset.id

        for material_instance in new_display_asset.material_instances:
            assert isinstance(material_instance, fortnite_api.MaterialInstance)

        for render_image in new_display_asset.render_images:
            assert isinstance(render_image, fortnite_api.RenderImage)

            assert isinstance(render_image.product_tag, fortnite_api.ProductTag)
            assert render_image.file_name
            assert isinstance(render_image.image, fortnite_api.Asset)

        assert new_display_asset == new_display_asset


@pytest.mark.asyncio
async def test_beta_fetch_material_instances(api_key: str):

    # Ensure you cannot call this without beta=True
    with pytest.raises(fortnite_api.BetaAccessNotEnabled):
        await ClientHybrid().beta_fetch_material_instances()

    async with ClientHybrid(beta=True, api_key=api_key) as client:
        material_instances = await client.beta_fetch_material_instances()

    for instance in material_instances:
        assert isinstance(instance, fortnite_api.MaterialInstance)

        assert instance.id
        assert instance.primary_mode
        assert instance.product_tag

        # Walk through all the images and ensure they are assets
        for name, asset in instance.images.items():
            assert isinstance(name, str)
            assert isinstance(asset, fortnite_api.Asset)

        assert instance == instance


@pytest.mark.asyncio
async def test_fetch_shop(api_key: str):
    async with ClientHybrid(api_key=api_key) as client:
        shop = await client.fetch_shop()

    assert isinstance(shop, fortnite_api.Shop)

    if not shop.entries:
        return

    for entry in shop.entries:
        # Ensure len(entry) works
        assert isinstance(len(entry), int)

        # Ensure you can iterate over the entry
        for cosmetic in entry:
            assert cosmetic.id

        assert isinstance(entry, fortnite_api.ShopEntry)
        assert isinstance(entry.regular_price, int)
        assert isinstance(entry.final_price, int)
        assert entry.in_date
        assert entry.out_date

        offer_tag = entry.offer_tag
        if offer_tag:
            assert isinstance(offer_tag, fortnite_api.ShopEntryOfferTag)
            assert offer_tag.id
            assert offer_tag.text

        bundle = entry.bundle
        if bundle:
            assert isinstance(entry.bundle, fortnite_api.ShopEntryBundle)
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

        tile_size = entry.tile_size
        assert isinstance(tile_size, fortnite_api.TileSize)
        assert tile_size.internal == f'Size_{tile_size.width}_x_{tile_size.height}'

        layout = entry.layout
        if layout:
            assert isinstance(layout, fortnite_api.ShopEntryLayout)
            assert layout.id
            assert layout.name
            assert isinstance(layout.index, int)
            assert isinstance(layout.rank, int)
            assert layout.show_ineligible_offers

        assert entry.dev_name
        assert entry.offer_id
        assert entry.tile_size

        new_display_asset = entry.new_display_asset
        if new_display_asset:
            assert isinstance(new_display_asset, fortnite_api.NewDisplayAsset)
            assert new_display_asset.id

            for material_instance in new_display_asset.material_instances:
                assert isinstance(material_instance, fortnite_api.MaterialInstance)

        colors = entry.colors
        if colors:
            assert isinstance(colors, fortnite_api.ShopEntryColors)
            assert isinstance(colors.color1, str)
            assert isinstance(colors.color3, str)

        COSMETIC_TYPE_MAPPING: dict[type[fortnite_api.Cosmetic[Any]], Callable[..., Any]] = {
            fortnite_api.CosmeticBr: test_cosmetic_br,
            fortnite_api.CosmeticInstrument: test_cosmetic_instrument,
            fortnite_api.CosmeticCar: test_cosmetic_car,
            fortnite_api.CosmeticLegoKit: test_cosmetic_lego_kit,
        }

        for cosmetic in entry.br + entry.tracks + entry.instruments + entry.cars + entry.lego_kits:
            tester = COSMETIC_TYPE_MAPPING[type(cosmetic)]
            tester(cosmetic)
