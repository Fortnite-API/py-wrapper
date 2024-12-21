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

from typing import Any

import fortnite_api


def validate_cosmetic_type_info(type_info: fortnite_api.CosmeticTypeInfo[Any]):
    assert isinstance(type_info, fortnite_api.CosmeticTypeInfo)
    assert isinstance(type_info.value, fortnite_api.CosmeticType)
    assert type_info.raw_value
    assert type_info.display_value
    assert type_info.backend_value


def validate_cosmetic_rarity_info(rarity_info: fortnite_api.CosmeticRarityInfo[Any]):
    assert isinstance(rarity_info, fortnite_api.CosmeticRarityInfo)
    assert isinstance(rarity_info.value, fortnite_api.CosmeticRarity)
    assert rarity_info.display_value
    assert rarity_info.backend_value


def validate_cosmetic_series_info(series_info: fortnite_api.CosmeticSeriesInfo[Any]):
    assert isinstance(series_info, fortnite_api.CosmeticSeriesInfo)
    assert series_info.value
    assert series_info.backend_value
    assert series_info.colors


def validate_cosmetic_br(cosmetic: fortnite_api.CosmeticBr[Any]):
    assert isinstance(cosmetic, fortnite_api.CosmeticBr)
    assert cosmetic.name
    assert cosmetic.description

    type_info = cosmetic.type
    if type_info:
        validate_cosmetic_type_info(type_info)

    rarity_info = cosmetic.rarity
    if rarity_info:
        validate_cosmetic_rarity_info(rarity_info)

    series_info = cosmetic.series
    if series_info:
        validate_cosmetic_series_info(series_info)

    _set = cosmetic.set
    if _set:
        assert isinstance(_set, fortnite_api.CosmeticBrSet)
        assert _set.text
        assert _set.backend_value

    introduction = cosmetic.introduction
    if introduction:
        assert isinstance(introduction, fortnite_api.CosmeticBrIntroduction)
        assert introduction.chapter
        assert introduction.season
        assert introduction.text
        assert introduction.backend_value

    images = cosmetic.images
    if images:
        assert isinstance(images, fortnite_api.CosmeticImages)

    variants = cosmetic.variants
    for variant in variants:
        assert isinstance(variant, fortnite_api.CosmeticBrVariant)
        assert variant.channel

        options = variant.options
        for option in options:
            assert isinstance(option, fortnite_api.CosmeticBrVariantOption)
            assert option.tag
            assert isinstance(option.image, fortnite_api.Asset)

    assert isinstance(cosmetic.built_in_emote_ids, list)
    assert isinstance(cosmetic.search_tags, list)
    assert isinstance(cosmetic.meta_tags, list)


def validate_cosmetic_car(cosmetic: fortnite_api.CosmeticCar[Any]):
    assert isinstance(cosmetic, fortnite_api.CosmeticCar)
    assert cosmetic.vehicle_id
    assert cosmetic.name
    assert cosmetic.description

    type_info = cosmetic.type
    if type_info:
        validate_cosmetic_type_info(type_info)

    rarity_info = cosmetic.rarity
    if rarity_info:
        validate_cosmetic_rarity_info(rarity_info)

    images = cosmetic.images
    if images:
        assert isinstance(images, fortnite_api.CosmeticImages)

    series_info = cosmetic.series
    if series_info:
        validate_cosmetic_series_info(series_info)


def validate_cosmetic_instrument(cosmetic: fortnite_api.CosmeticInstrument[Any]):
    assert isinstance(cosmetic, fortnite_api.CosmeticInstrument)
    assert cosmetic.name
    assert cosmetic.description

    type_info = cosmetic.type
    if type_info:
        validate_cosmetic_type_info(type_info)

    rarity_info = cosmetic.rarity
    if rarity_info:
        validate_cosmetic_rarity_info(rarity_info)

    images = cosmetic.images
    if images:
        assert isinstance(images, fortnite_api.CosmeticImages)

    series_info = cosmetic.series
    if series_info:
        validate_cosmetic_series_info(series_info)


def validate_cosmetic_lego_kit(cosmetic: fortnite_api.CosmeticLegoKit[Any]):
    assert isinstance(cosmetic, fortnite_api.CosmeticLegoKit)
    assert cosmetic.name

    type_info = cosmetic.type
    if type_info:
        validate_cosmetic_type_info(type_info)

    series_info = cosmetic.series
    if series_info:
        validate_cosmetic_series_info(series_info)

    images = cosmetic.images
    if images:
        assert isinstance(images, fortnite_api.CosmeticImages)


def validate_variant_lego(variant: fortnite_api.VariantLego[Any]):
    assert isinstance(variant, fortnite_api.VariantLego)
    assert variant.cosmetic_id
    assert isinstance(variant.sound_library_tags, list)

    images = variant.images
    if images:
        assert isinstance(images, fortnite_api.CosmeticImages)


def validate_variant_bean(variant: fortnite_api.VariantBean[Any]):
    assert isinstance(variant, fortnite_api.VariantBean)
    assert variant.name

    if variant.gender:
        assert isinstance(variant.gender, fortnite_api.CustomGender)

    images = variant.images
    if images:
        assert isinstance(images, fortnite_api.CosmeticImages)


def validate_cosmetic_track(cosmetic: fortnite_api.CosmeticTrack[Any]):
    assert isinstance(cosmetic, fortnite_api.CosmeticTrack)
    assert cosmetic.dev_name
    assert cosmetic.title
    assert cosmetic.artist
    assert cosmetic.release_year
    assert cosmetic.bpm
    assert cosmetic.duration

    difficulty = cosmetic.difficulty
    assert isinstance(difficulty, fortnite_api.CosmeticTrackDifficulty)
    assert isinstance(difficulty.vocals, int)
    assert isinstance(difficulty.guitar, int)
    assert isinstance(difficulty.bass, int)
    assert isinstance(difficulty.plastic_bass, int)
    assert isinstance(difficulty.drums, int)
    assert isinstance(difficulty.plastic_drums, int)
    assert isinstance(cosmetic.genres, list)
    assert isinstance(cosmetic.album_art, fortnite_api.Asset)
